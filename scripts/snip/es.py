#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from logger import logger
import urllib
import json
import pycurl
import StringIO
import mimetypes
encoding = sys.getdefaultencoding()

class Curl(object):
    result = ""
    func = ""
    def __init__(self, url="", x="", d=""):
        self.url = url
        if not isinstance(url, str):
            self.url = url.encode(encoding, "replace")
        self.data = d
        if not isinstance(d, str):
            self.data = d.encode(encoding, "replace")
        if x == "PUT":
            self.func = self.put
        elif x == "GET":
            self.func = self.get
        elif x == "POST":
            self.func = self.post

    def perform(self):
        if self.func:
            self.func()
        return self

    def str(self, data):
        if not isinstance(data, str):
            return
        return data

    def get(self):
        c = pycurl.Curl()
        buf = StringIO.StringIO()
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.CONNECTTIMEOUT, 30)
        c.setopt(pycurl.TIMEOUT, 300)
        c.setopt(pycurl.NOSIGNAL, 1)
        c.setopt(pycurl.WRITEFUNCTION, buf.write)
        c.setopt(pycurl.URL, self.url)
        c.perform()
        self.result = buf.getvalue()
        buf.close()
        del buf
        return self

    def put(self):
        c = pycurl.Curl()
        tmp = os.tmpfile()
        tmp.write(self.data)
        c.setopt(pycurl.URL, self.url)
        c.setopt(pycurl.PUT, 1)
        c.setopt(pycurl.INFILE, tmp)
        c.setopt(pycurl.INFILESIZE, len(self.data))
        c.perform()
        del tmp
        return self

    def post(self):
        c = pycurl.Curl()
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.URL, self.url)
        c.setopt(pycurl.POSTFIELDS, self.data)
        c.setopt(pycurl.POSTFIELDSIZE, -1)
        c.perform()
        return self

class ElasticSearch(object):
    host = "localhost"
    port = "9200"

    def __init__(self, index, doctype):
        self.index = index
        self.type = doctype

    def put(self, dic={}):
        dicstr = u""
        for key, value in dic.items():
            dicstr += u'"%s":"%s", ' % (key, value)
        if not dicstr:
            return False
        url = u"http://%s:%s/%s/%s" % (self.host, self.port, self.index, self.type)
        data = u"{%s}" % dicstr[:-2]
        Curl(url, x="POST", d=data).perform()

    def get(self, dic={}):
        dicstr = ""
        for key, value in dic.items():
            dicstr += '%s:%s&' % (urllib.quote(key), urllib.quote(value))
        if not dicstr:
            return False
        url = u"http://%s:%s/%s/%s/_search?q=%s" % (self.host, self.port, self.index, self.type, dicstr[:-1])
        curl = Curl(url, x="GET", d="").perform()
        res = json.loads(curl.result)
        print res


#path = "/Users/murakami/Sites/jglobal_2013"
path = "/Users/murakami/svns/nishitetsu_kensetsu"
#path = "/Users/murakami/git/jukebox/"
#path = "/Users/murakami/virtualenv/py2.7/lib"
#path = "/Users/murakami/hoge/"
targets = []
excludes = [".git", ".svn"]

for root, dirs, files in os.walk(path, topdown=True):
    dirs[:] = [d for d in dirs if d not in excludes]
    for f in files:
        if ".min." in f:
            continue
        targets.append(os.path.join(root, f))

for name in targets:
    guess = mimetypes.guess_type(name)
    if not guess[0]:
        continue
    mime = guess[0].split("/")
    if mime[0] == "text":
        f = open(name)
        text = ""
        for line in f.readlines():
            text += line.decode("utf-8", "replace")
        es = ElasticSearch(u"murakami", mime[1])
        #print name
        text = urllib.quote(text.encode("utf-8", "replace"))
        data = {
            u"name": u"%s" % name.decode("utf-8", "replace"),
            u"text": u"%s" % text.decode("utf-8", "replace")
        }
        es.put(data)
        print
        f.close()

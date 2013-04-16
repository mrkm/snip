#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import urllib
import json
import mimetypes
import StringIO
import pycurl

encoding = sys.getdefaultencoding()

class Curl(object):
    result = u''
    func = u''
    def __init__(self, url='', x='', d=''):
        if isinstance(url, str):
            self.url = url
        else:
            self.url = url.encode(encoding, u'replace')
        if isinstance(d, str):
            self.data = d
        else:
            self.data = d.encode(encoding, u'replace')
        if x == u'PUT':
            self.func = self.put
        elif x == u'GET':
            self.func = self.get
        elif x == u'POST':
            self.func = self.post

    def perform(self):
        if self.func:
            self.func()
        return self

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
    host = u'localhost'
    port = u'9200'

    def __init__(self, index, doctype):
        self.index = index
        self.type = doctype

    def put(self, dic={}):
        dump = {}
        for k, v in dic.items():
            key = k.encode(u'utf-8', u'replace')
            value = urllib.quote(v.encode(u'utf-8', u'replace'))
            dump[key] = value
        url = u'http://%s:%s/%s/%s' % (self.host, self.port, self.index, self.type)
        data = json.dumps(dump)
        #print data
        Curl(url, x=u'POST', d=data).perform()

    def get(self, fields=[], dic={}):
        dump = {}
        for k, v in dic.items():
            key = k.encode(u'utf-8', u'replace')
            value = urllib.quote_plus(v.encode(u'utf-8', u'replace'))
            dump[k] = v
        url = u'http://%s:%s/%s/%s/_search' % (self.host, self.port, self.index, self.type)
        if fields:
            url += u"?fields="
            for i, field in enumerate(fields):
                if i > 0:
                    url += ","
                url += field

        data = json.dumps(dump)
        curl = Curl(url, x='GET', d=data).perform()
        res = json.loads(curl.result)
        total = res['hits']['total']
        max_score = res['hits']['max_score']
        texts = res['hits']['hits']
        name = res['hits']['hits'][0]['fields']['name']
        hits = []
        while texts:
            text = texts.pop(0)
            hits.append({'name':name,
                         'text':urllib.unquote(text['fields']['text'])
                         })
        return {"hits":hits, "total":total}
    
# path = '/Users/murakami/Sites/jglobal_2013'
# path = '/Users/murakami/svns/nishitetsu_kensetsu'
# path = '/Users/murakami/git/jukebox/'
# path = '/Users/murakami/virtualenv/py2.7/lib'
# path = '/Users/murakami/hoge/'
# targets = []
# excludes = ['.git', '.svn']
# for root, dirs, files in os.walk(path, topdown=True):
#     dirs[:] = [d for d in dirs if d not in excludes]
#     for f in files:
#         if '.min.' in f:
#             continue
#         targets.append(os.path.join(root, f))
# for name in targets:
#     #continue
#     guess = mimetypes.guess_type(name)
#     if not guess[0]:
#         continue
#     mime = guess[0].split('/')
#     if mime[0] == 'text':
#         f = open(name)
#         text = ''
#         #text = f.readline()
#         for line in f.readlines():
#             text += line.decode('utf-8', 'replace')
#         es = ElasticSearch(u'murakami', mime[1])
#         data = {
#             u'name': u'%s' % name.decode('utf-8', 'replace'),
#             u'text': u'%s' % text
#         }
#         es.put(data)
#         print
#         f.close()
# ElasticSearch(u'murakami', u'css').get(fields=["text"])
# f = open('/Users/murakami/Sites/snip/esdata')
# for line in f.readlines():
#     text = line.decode('utf-8', 'replace')
#     res = json.loads(text)
#     print res['text']
# f.close()


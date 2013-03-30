#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from logger import logger
import urllib
import json
import pycurl

encoding = sys.getdefaultencoding()

class Curl():
    c = pycurl.Curl()
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.CONNECTTIMEOUT, 30)
    c.setopt(pycurl.TIMEOUT, 300)
    c.setopt(pycurl.NOSIGNAL, 1)

    def __init__(self):
        self.c.setopt(pycurl.WRITEFUNCTION, self.body_callback)
        self.result = ""

    def get(self, url):
        self.c.setopt(pycurl.URL, url.encode(encoding, "replace"))
        self.c.perform()
        return self.c.result

    def body_callback(self, buf):
        self.result = buf
        print self.result
        return self


class ElasticSearch(object):
    host = "localhost"
    port = "9200"

    def __init__(self, index, doctype):
        self.index = index
        self.type = doctype

    def put(self, dic={}):
        """
        curl -XPUT ‘http://192.168.11.201:9200/twitter/tweet/100’ –d ‘{
        “user”: “murakami”,
        “message”: “ElasticSearch supports multi-tenancy.”
        }’
        """
        dicstr = ""
        for key, value in dic.items():
            dicstr += '"%s":"%s", ' % (key, value)
        if not dicstr:
            return False
        cmd = u"curl -XPUT 'http://%s:%s/%s/%s' -d '{%s}'" % (self.host, self.port, self.index, self.type, dicstr[:-2])
        logger.info(cmd)
        #os.system(cmd)

    def get(self, dic={}):
        """
        curl -XGET ‘http://192.168.11.201:9200/apache/access/_search?q=status:500’
        """
        dicstr = ""
        for key, value in dic.items():
            dicstr += '%s:%s&' % (urllib.quote(key), urllib.quote(value))
        if not dicstr:
            return False
        url = u"http://%s:%s/%s/%s/_search?q=%s" % (self.host, self.port, self.index, self.type, dicstr[:-1])
        print Curl().get(url)

        #print json.loads(result)
        #logger.info(cmd)
        #result = do_exec(cmd)
        #logger.info(result)
        #os.system(cmd)

db = ElasticSearch(index="murakami", doctype="css")
db.put({"user":"murakami", "message":"ElasticSearch supports multi-tenancy."})
db.get({"user":"murakami", "message":"ElasticSearch supports multi-tenancy."})

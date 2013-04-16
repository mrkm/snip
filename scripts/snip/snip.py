#!/usr/bin/python
# -*- coding: utf-8 -*-
import optparse
import settings
import sys
from es import ElasticSearch

separater = "=" * 20

class CommandError(Exception):
    pass

class SimpleParser(object):
    """
    あまり頑張らない解析で文書を
    スニペットに分割する
    """
    def __init__(self):
        pass

    def parse(self, string, exp):
        snips = []
        comment = False
        target = -1
        snippet = ""
        for num, s in enumerate(string.split("\n")):
            sep = False
            # コメント判定
            if exp in s:
                target = len(snips) - 1
            if u"/*" in s:
                comment = True
            if u"*/" in s:
                comment = False
            if comment:
                # コメント中はスニペット終端判定を行わない
                snippet += "%s\n" % s
                continue
            s = s.strip("\s")
            if not s:
                continue
            if "}" in s:
                # スニペット終端判定
                sep = True
            snippet += "%s\n" % s
            if sep:
                # ひとつのスニペット単位終了
                snips.append(snippet.strip("\s").strip("\r\n"))
                snippet = ""
                sep = False
        if snippet:
            snips.append(snippet)
        return snips, target

class Snip(object):
    settings = settings
    hoge = settings.HOGE
    db = ElasticSearch(u'murakami', u'css')
    parser = SimpleParser
    def __init__(self):
        self.artists = {}
        self.parse = self.parser().parse

def __main__():
    # parser = optparse.OptionParser()
    # parser.add_option('-l', '--lists', action='store_true', dest='lists', default=False, help='show artists')
    # (options, args) = parser.parse_args(sys.argv)
    try:
        exp = sys.argv[1]
    except:
        raise CommandError(u"argument error")
    snip = Snip()
    res = snip.db.get(fields=["text", "name"], dic={"text":exp})        
    for hit in res["hits"]:
        snippets, target = snip.parse(hit["text"], exp)
        if target > 0:
            print '[32m%s[m' % hit["name"]
            print snippets[target]
        #break # ファイルひとつだけ解析
    return 0

usg = """usage: snip exp"""

try:
    __main__()
except CommandError, e:
    print '[31m%s[m' % e
    print usg
    exit(1)

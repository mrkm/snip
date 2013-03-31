#!/Users/murakami/virtualenv/py2.7/bin/python
# -*- coding: utf-8 -*-
from scripts.snip.es import ElasticSearch
db = ElasticSearch(index="murakami", doctype="css")
data = db.get({"user": "murakami", "message": "ElasticSearch supports multi-tenancy."})
import cgi
#print cgi.test()
print "Content-Type: text/html"
print
print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="content-type" content="text/html;charset=utf-8" />
		<meta name="generator" content="Adobe GoLive" />
		<title>search [snip]</title>
        <!-- js -->
        <script language="javascript" type="text/javascript" src="js/jquery-1.7.2.min.js" charset="utf-8"></script>
        <script language="javascript" type="text/javascript" src="bootstrap/js/bootstrap.min.js" charset="utf-8"></script>

        <!-- css -->
        <link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.min.css" media="screen">
        <link rel="stylesheet" type="text/css" href="css/base.css" media="screen">
    </head>
    <body class="top">
"""
print """
    <div class="container">
        <!--<div class="hero-unit search">-->
        <div class="search">
            <div>
                <h1 class="title">Snip</h1>
                <h4>search yourself</h4>
                <form class="form-search" action="search.cgi">
                    <div class="input-append">
                        <input class="span5 search-query" type="text" placeholder="clearfix">
                        <button class="btn" type="submit">&nbsp;<i class="icon-search"></i>&nbsp;</button>
                    </div>
                </form>
            </div>
        </div>
    </body>
</html>
"""
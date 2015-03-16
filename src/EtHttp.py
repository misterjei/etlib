#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Taken from https://gist.github.com/rduplain/1265409 with permission (by Ron DuPlain).
@author: Jeremiah Blanchard
@since: 08/20/2014
@summary: HTTP lib
'''

import cookielib
import urllib
import urllib2
  
class Client(object):
    def __init__(self, cookieFile = None):
        if cookieFile != None:
            self.cookie_jar = cookielib.MozillaCookieJar()
            self.cookie_jar.load(cookieFile)
            for cookie in self.cookie_jar:
                print cookie
        else:
            self.cookie_jar = cookielib.CookieJar()
        
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar))
        urllib2.install_opener(self.opener)
 
    def addCookie(self, cookie):
        self.cookie_jar.set_cookie(cookie)        
    
    def get(self, url, headers={}):
        request = urllib2.Request(url, headers=headers)
        return self.execute_request(request)
    
    def post(self, url, data=None, headers={}):
        if data is None:
            postdata = None
        else:
            postdata = urllib.urlencode(data)
        request = urllib2.Request(url, postdata, headers)
        return self.execute_request(request)
    
    def execute_request(self, request):
        response = self.opener.open(request)
        response.status_code = response.getcode()
        response.data = response.read()
        return response

#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Download cnbeta newest article in index.
'''

import os
import requests
import time
from lxml import html
import sys

#make sure coding is unicode
reload(sys)
sys.setdefaultencoding('utf-8')

def get_response(url):
    '''
    Take a url, return a response base on the url
    '''
    headers = {
        "headers" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"
    }
    
    response = requests.get(url, headers = headers)
    return response
    
def get_article_urls():
    '''
    store the urls of the article in a list
    '''
    start_url = "http://www.cnbeta.com"
    response = get_response(start_url)
    parsed_body = html.fromstring(response.text)
    
    
    article_urls = parsed_body.xpath('//div[@class="content_body all_news_wildlist"]/div/div/dl/dt/a/@href')
    
    print("get_urls done.")
    
    return article_urls
    
def get_article(article_urls):
    '''
    Take a list of urls, store the article in ~/cnbeta/
    '''    
    count = 0
    start_url = "http://www.cnbeta.com"
    article_dir = os.getcwd()+'/cnbeta/'
    print("There are %s articles" %len(article_urls))
    if not os.path.exists(article_dir):
        os.mkdir(article_dir)
    
    for url in article_urls:
        response = get_response(start_url + url)
        parsed_body = html.fromstring(response.text)
        
        keywords = parsed_body.xpath('//meta[@name="keywords"]/@content')
        title = parsed_body.xpath('//section[@class="main_content"]/section/article/div/header/h2/text()')
        content = parsed_body.xpath('//section[@class="main_content"]/section/article/div/section/div/p/text()')
        f = open(article_dir+'%s.txt'%count, 'wb')
        for each in title:
            f.write(each.encode('raw_unicode_escape'))
        f.write('\n')
        for each in content:
            f.write(each.encode('raw_unicode_escape'))
            
        f.close()            
        print("have saved %s article, url: %s" %(count, url))
        count += 1        
    
if __name__ == '__main__':
    get_article(get_article_urls())

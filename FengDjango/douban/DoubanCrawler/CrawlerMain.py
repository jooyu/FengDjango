# -*- coding: UTF-8 -*-
import urllib2
import io
import sys
import re
import thread
import Queue
import time
import threading
import string

class CrawlerMain:

    # URL_DOUBAN = 'https://www.douban.com/group/baoanzufang/discussion?start=0'
    # URL_DOUBAN = 'https://www.douban.com/group/nanshanzufang/discussion?start=0'

    def __init__(self):
        print '实例化'

    def getHtmlCode(self,url):
        # 读取页面的源码
        print (url)
        data = None
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
        request = urllib2.Request(url,data,headers)
        respose = urllib2.urlopen(request)
        content = respose.read()
        # content = re.sub(r'\n','{huanhangfu}',content)
        return content

    def getTopicUrlList(self,content,tag):
        # 读取源码中的url列表
        content = re.sub(r'\n','{hhf}',content)
        # 1.获取url table部分
        pattern1 = re.compile('table class="olt".*paginator')
        mainContentObj = re.findall(pattern1,content)
        mainContent = mainContentObj[0]
        # 2.获取有url的那一段
        pattern2 = re.compile('<td class="title">.*?<td nowrap="nowrap">')
        lists = re.findall(pattern2,mainContent)
        # 3.获取其中的url和标题
        pattern3 = re.compile('<a href="(.*?)" title="(.*?)"')
        i = 0
        topicUrlList = ['-1']
        for list in lists:
            if(i==0):
                urlObj = re.findall(pattern3,list)
                urlObjUrl = urlObj[0]
                topicUrlList[0] = urlObjUrl[tag]
            else:
                urlObj = re.findall(pattern3,list)
                urlObjUrl = urlObj[0]
                topicUrlList.insert(i,urlObjUrl[tag])
            i += 1
        return topicUrlList

    def getPrice(self,content):
        content = re.sub(r'\n','{hhf}',content)
        # 获取价钱
        # 1.获取正文
        pattern1 = re.compile('topic-doc.*?sns-bar')
        text = re.findall(pattern1,content)
        pattern2 = re.compile('<p>.*</p>')
        if text:
            text = re.findall(pattern2,text[0])
            if text:
                text = text[0]
            else:
                text = ''
        else:
            text = ''
        # 2.获取标题
        pattern3 = re.compile('<h1>.*?</h1>')
        title = re.findall(pattern3,content)
        if title:
            title = title[0]
        else:
            title = ''
        # 3.获取价钱
        titleAndText = title + ' ' + text
        pattern4 = re.compile('[0-9]+')
        prices = re.findall(pattern4,titleAndText)
        # 4.去除不对的数字
        returnPrices = []
        for price in prices:
            priceLength = len(price)
            if 4 <= priceLength <= 5:
                returnPrices.append(price)
        return returnPrices



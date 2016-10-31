# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import DoubanCrawler.CrawlerMain
import DoubanCrawler.CrawlerTool
import models
import sqlite3
import urllib2
import string

# def index(request):
#     URL_DOUBAN = 'https://www.douban.com/group/nanshanzufang/discussion?start=0'
#     crawler = DoubanCrawler.CrawlerMain.CrawlerMain()
#     mainContent = crawler.getHtmlCode(URL_DOUBAN)
#     # 获取话题url
#     topicUrls = crawler.getTopicUrlList(mainContent)
#     # for topicUrl in topicUrls:
#     #     # 获取话题源码
#     #     content = crawler.getHtmlCode(topicUrl)
#     #     print topicUrl
#     #     # 获取价钱
#     #     price = crawler.getPrice(content)
#     #     print price
#     return HttpResponse(crawler.getHtmlCode(topicUrls[0]))
def readed(request):
    print ("readed feng")
    index = request.GET.get('index')
    return render(request,'temp.html')

def index(request):
    conn = sqlite3.connect('douban.db')
    count = request.GET.get('count')
    if count == None or count == "":
        count = '1'
    doubanUrl = request.GET.get('doubanurl')
    if doubanUrl == None:
        doubanUrl = 'http://'
    doubanUrl = urllib2.unquote(doubanUrl)
    print (doubanUrl)
    click = request.GET.get('click')
    if click == '1':
        models.edit(conn, doubanUrl, 1)
        return render(request,'index.html')
    title = '豆瓣找房小助手'
    crawlerTool = DoubanCrawler.CrawlerTool.CrawlerTool()
    crawlerTool.initContents(string.atoi(count))
    topicTitles = crawlerTool.getTitles()
    topicUrls = crawlerTool.getUrls()
    for topicUrl in topicUrls:
        models.insertUrl(conn,topicUrl, 0)
    models.edit(conn, doubanUrl, 1)
    isReadeds = []
    for topicUrl in topicUrls:
        if models.isReaded(conn,topicUrl):
            isReadeds.append(1)
        else:
            isReadeds.append(0)
    pricesFromDb = []
    for topicUrl in topicUrls:
        priceFromDb = models.getPrice(conn, topicUrl)
        if not priceFromDb == None:
            pricesFromDb.append(priceFromDb)
        else:
            pricesFromDb.append(-1)
    pricess = crawlerTool.getMoney(topicUrls,isReadeds,pricesFromDb)
    minPrices = []
    for prices in pricess:
        # 找出最小的价钱
        temp = 10000
        for price in prices:
            intPrice = string.atoi(price)
            if intPrice <= temp:
                temp = intPrice
        if temp == 10000:
            minPrices.append(0)
        else:
            minPrices.append(temp)
    # 将价钱不对的设为已读
    # 不再设为已读，而是暂时不显示
    for index in range(len(minPrices)):
        if minPrices[index] > 1751:
            # models.edit(conn,topicUrls[index],1)
            # isReadeds[index] = 1
            # 将所有价钱都存在数据库中
            models.setPrice(conn,topicUrls[index],minPrices[index])
        else:
            # isReadeds[index] = 0
            # models.setPrice(conn,topicUrls[index],minPrices[index])
            # 将所有价钱都存在数据库中
            models.setPrice(conn,topicUrls[index],minPrices[index])

    return render(request, 'index.html',
                  {'title': title, 'topicTitles': topicTitles, 'topicUrls': topicUrls, 'minPrices': minPrices, 'doubanUrl': doubanUrl,
                   'isReadeds': isReadeds})

# -*- coding: UTF-8 -*-
import CrawlerMain
class Singleton(object):
    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

class CrawlerTool(Singleton):
    URL_DOUBAN = 'https://www.douban.com/group/nanshanzufang/discussion?start=' # 0、25、50、75
    # URL_DOUBAN = 'https://www.douban.com/group/baoanzufang/discussion?start='
    urls = []
    titles = []
    contents = []
    pages = 0

    def initContents(self,pages):
        # 获取内容
        crawler = CrawlerMain.CrawlerMain()
        num = 0
        CrawlerTool.pages = 0
        CrawlerTool.contents = []
        for index in range(0,pages):
            homeUrl = CrawlerTool.URL_DOUBAN + str(num)
            content = crawler.getHtmlCode(homeUrl)
            CrawlerTool.contents.append(content)
            num += 25
            CrawlerTool.pages += 1

    def getUrls(self):
        # 获取标题
        crawler = CrawlerMain.CrawlerMain()
        CrawlerTool.urls = []
        for index in range(0,CrawlerTool.pages):
            url = crawler.getTopicUrlList(CrawlerTool.contents[index],0)
            CrawlerTool.urls.extend(url)
        return CrawlerTool.urls

    def getTitles(self):
        # 获取url
        crawler = CrawlerMain.CrawlerMain()
        CrawlerTool.titles = []
        for index in range(0,CrawlerTool.pages):
            title = crawler.getTopicUrlList(CrawlerTool.contents[index], 1)
            CrawlerTool.titles.extend(title)
        return CrawlerTool.titles

    def getMoney(self,urls,isReadeds,pricesFromDb):
        crawler = CrawlerMain.CrawlerMain()
        moneys = []
        lenght = len(urls)
        for index in range(len(urls)):
            if not pricesFromDb[index] == -1:
                money = ['%d' % pricesFromDb[index]]
                moneys.append(money)
                print '已有价格'
            else:
                if isReadeds[index] == 0:
                    print ('loading')
                    content = crawler.getHtmlCode(urls[index])
                    money = crawler.getPrice(content)
                    moneys.append(money)
                else:
                    money = ['10000']
                    moneys.append(money)
            print ("%d / %d\n" % (index,lenght))
        return moneys
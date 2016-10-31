# -*- coding:UTF-8 -*-
from __future__ import unicode_literals
import sqlite3
from django.db import models


# Create your models here.

conn = sqlite3.connect('douban.db')

def createTable():
    # 创建表
    conn = sqlite3.connect('douban.db')
    print '连接douban.db'
    conn.execute('''CREATE TABLE readed(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    isreaded INTEGER NOT NULL,
                    price INTEGER);''')
    conn.close()


def insertUrl(conn, url, status):
    # 插入数据库
    print '插入数据库:' + url
    if not isHadUrl(conn, url):
        conn.execute('insert into readed(url,isreaded,user_id)\
                  values("%s",%d,%d);' % (url, 0, 1))  #我自己是1
        conn.commit()
        print 'success'
    else:
        print 'error 已存在于数据库中'
    # conn.close()


def edit(conn, url, status):
    # 修改状态
    # conn = sqlite3.connect('douban.db')
    print '修改状态'
    conn.execute("update readed set isreaded = %d where url = '%s'" % (status, url))
    conn.commit()
    # conn.close()
def setPrice(conn,url,price):
    print '添加价格'
    conn.execute("update readed set price = %d where url = '%s'" % (price,url))
    conn.commit()
def getPrice(conn,url):
    print '获取价格'
    cursor = conn.execute("select id,price from readed where url ='%s'" % url)
    for row in cursor:
        if not row[1] == None:
            return row[1]
        else:
            return None
def isHadUrl(conn, url):
    # 查是否存在此url
    # conn = sqlite3.connect('douban.db')
    print '查是否存在此url'
    cursor = conn.execute("select * from readed where url='%s'" % url)
    result = False
    for row in cursor:
        result = True
    print result
    return result


def isReaded(conn, url):
    # 查状态
    # conn = sqlite3.connect('douban.db')
    print '查询状态'
    cursor = conn.execute("select id,url,isreaded from readed where url='%s'" % url)
    result = False
    for row in cursor:
        if row[2] == 1:
            result = True
        else:
            result = False
    # conn.close()
    print result
    return result


def dropTable():
    # 删除表
    conn = sqlite3.connect('douban.db')
    print '删除表'
    conn.execute('DROP TABLE readed;')
    # conn.commit()
    conn.close()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Author:         Xu Ziming
    Filename:       WebSpider.py
    Last modified:  2015-9-28
    可用于下载网页源码中包含的pdf文件
    目前仅支持对百度学术的pdf文献下载
    使用时用百度学术搜索结果中非第一页的网址替换主程序中的网址即可
    本程序学习修改自：http://www.jikexueyuan.com/course/821.html
"""

import requests
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spider(object):
    def __init__(self):
        print u'开始爬取内容……'

#getsource用来获取网页源代码
    def getsource(self,url):
        html = requests.get(url)
        return html.text

#changepage用来生产不同页数的链接
    def changepage(self,url,total_page):
        now_page = int(re.search('pn=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page):
            link = re.sub('pn=\d+','pn=%s'%(i*10),url,re.S)
            page_group.append(link)
        return page_group

#geteveryclass用来抓取每个课程块的信息
    def geteveryclass(self,source):
        everyclass = re.findall(ur'相关文章</a><a href="http://.*?pdf',source,re.S)
        return everyclass

#getinfo用来从每个课程块中提取出我们需要的信息
    def getinfo(self,eachclass):
        info = {}
        if re.search('http\:.*?\.pdf',eachclass,re.S) >= 0:
            info['adress'] = re.search('http\:.*?\.pdf',eachclass,re.S).group(0)
        else:
            info['adress']='NULL'
        return info

#saveinfo用来保存结果到info.txt文件中
    def saveinfo(self,classinfo):
        f = open('info.txt','w')
        i=0
        for each in classinfo:
            f.writelines('adress:' + each['adress'] + '\n')
            if each['adress'] != 'NULL':
                r = requests.get(each['adress'])
                i=i+1
                with open("%s.pdf"%i, "wb") as code:
                    code.write(r.content)
        f.close()

if __name__ == '__main__':
    classinfo = []
    url = 'http://xueshu.baidu.com/s?wd=mav&pn=00&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&filter=sc_year%3D%7B2015%2C%2B%7D&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&bcp=2&sc_hit=1'
    baiduxueshu = spider()
    all_links = baiduxueshu.changepage(url,20)
    for link in all_links:
        print u'正在处理页面：' + link
        html = baiduxueshu.getsource(link)
        everyclass = baiduxueshu.geteveryclass(html)
        for each in everyclass:
            info = baiduxueshu.getinfo(each)
            classinfo.append(info)
    baiduxueshu.saveinfo(classinfo)



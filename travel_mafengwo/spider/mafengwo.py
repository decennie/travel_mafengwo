#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "decennie"
__date__ = "2019/3/17 "
import requests
import re
from lxml import etree
from db.mongodb import mongo

"""
1. 准备URL列表
2. 遍历URL列表, 发送请求, 获取响应数据
3. 解析数据
4. 保存数据
"""

class MafengwoSpider(object):
    def __init__(self,city):
        """初始化的数据"""
        self.city =  city
        # 准备URL模板
        self.url_pattern = "http://www.mafengwo.cn/search/s.php?q="+city+"&p={}&t=poi&kt=1"
        # 准备请求头
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }

    def get_url_list(self):
        """获取URL列表"""
        #获取前20个页面的URL
        #定义列表，用于存储URL
        url_list = []
        for i in range(1,21):
            url = self.url_pattern.format(i)
            url_list.append(url)
        return url_list

    def get_page_from_url(self,url):
        """根据URL，发送请求，获取页面数据"""
        response = requests.get(url,headers=self.headers)
        # 返回响应的字符串数据
        return response.content.decode()


    def get_datas_from_page(self, page):
        """解析页面数据"""
        # 把页面转换为Element对象, Element对象上, 就可以使用XPATH提取数据了
        element = etree.HTML(page)
        # 1. 获取包含景点信息的标签列表
        # xpath: 返回一个list对象
        lis = element.xpath('//*[@id="_j_search_result_left"]/div/div/ul/li')
        # 2. 遍历标签列表, 提取需要数据
        # 定义列表, 用于存储需要的数据
        data_list = []
        for li in lis:
            # 定义字典, 用于存储数据
            item = {}
            # 获取名称
            name = ''.join(li.xpath('./div/div[2]/h3/a//text()'))
            # print(name)
            # 如果标题中, 没有景点就过滤掉
            if name.find('景点') == -1:
                # 跳过本次循环, 后面的代码, 继续下一次循环
                continue
            # print(name)
            # 去掉标题中的景点
            item['name'] = name.replace('景点 - ', '')
            # print(item)
            # 提取地址
            item['address'] = li.xpath('./div/div[2]/ul/li[1]/a//text()')[0]
            # 获取点评数量
            # 点评(489)
            comments_num = li.xpath('./div/div[2]/ul/li[2]/a/text()')[0]
            # 提取点评中的数据
            item['comments_num'] = int(re.findall('点评\((\d+)\)', comments_num)[0])

            # 获取游记数量
            # 游记(23)
            travel_notes_num = li.xpath('./div/div[2]/ul/li[3]/a//text()')[0]
            item['travel_notes_num'] = int(re.findall('游记\((\d+)\)', travel_notes_num)[0])
            # 记录当前景点的城市
            item['city'] = self.city
            print(item)
            data_list.append(item)

        return data_list

    def save_data(self,datas):
        """保存数据"""
        for data in datas:
            # 把景点名称，指定未MongoDB的逐渐
            data['_id'] = data['name']
            # 把数据保存到MongoDB中
            mongo.save(data)


    def run(self):
        """程序入口，核心逻辑"""
        # 1. 准备URL列表
        url_list = self.get_url_list()
        print(url_list)
        # 2. 遍历URL列表, 发送请求, 获取响应数据
        for url in url_list:
            #发送请求, 获取响应数据
            page = self.get_page_from_url(url)
            # 3. 解析数据
            datas = self.get_datas_from_page(page)
            # 4. 保存数据
            self.save_data(datas)


if __name__ == "__main__":
    ms = MafengwoSpider("广州")
    ms.run()

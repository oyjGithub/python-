#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import random

global ip_num
ip_num = 0
base_url = "http://www.ip3366.net/?stype=1&page="
header1 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37"}
header2 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}# http://www.ip3366.net/?stype=1&page=1 去这找一个好使的IP地址
# http://www.ip3366.net/?stype=1&page=1 去这找一个好使的IP地址
proxies={'https':'42.177.142.233:9999'}

def proxies_switch(url):
    print("正在进行ip的切换...")
    global ip_num
    stutas = False
    while stutas ==False: #找到合适的ip——post地址
        print("正在验证第%s个ip地址"%(ip_num))
        with open('./IP.txt','r',encoding="utf-8") as text:
            rows = text.readlines()
        print(len(rows))
        if ip_num*5+4 > len(rows):
            print("没有合适的IP地址")
            break
        ip = rows[ip_num*5][:-1]
        post = rows[ip_num*5+1][:-1]
        type = rows[ip_num * 5 + 3][:-1].lower()
        ip_post = ip+":"+post
        response = requests.get(url, headers=header1 if random.random()>0.5 else header2, proxies={type:ip_post})
        stutas = response.ok
        ip_num = ip_num+1
    proxies['https'] = ip_post
    print("第%d个ip地址测试成功"%(ip_num))
    time.sleep(0.5) #切换成功之后sleep一秒 防止新的ip_post被封

def reptile_ip(url):
    list = []
    html = requests.get(url,headers=header1 if random.random()>0.5 else header2, proxies=proxies)
    print("连接情况为",html.ok)
    if html.ok == False:
        proxies_switch(url)
        html = requests.get(url, headers=header1 if random.random()>0.5 else header2, proxies=proxies)
    try:
        soup = BeautifulSoup(html.content,"html.parser")
        items = soup.find("tbody").find_all("tr")
        if len(items)<1:
            return []
        items =items[1:]
        for i in items:
            book = {}
            book["ip"] = i.find_all("td")[0].text
            book["post"] = i.find_all("td")[1].text
            book["type"] = i.find_all("td")[3].text
            book["place"] = i.find_all("td")[5].text
            book["response_time"] = i.find_all("td")[6].text
            list.append(book)
        return list
    except:
        return []

def main():
    url = base_url
    with open('./IP.txt','w+',encoding='utf-8') as text:
        for i in range(1,11):
            print(i)
            lists = reptile_ip(url + (str(i)))
            if len(lists) < 1:
                continue
            for list in lists:
                print(str(list["ip"])+"has been keeped")
                text.write(list["ip"]+'\n')
                text.write(list["post"]+'\n')
                text.write(list["type"]+'\n')
                text.write(list["place"]+'\n')
                text.write(list["response_time"]+'\n')
    text.close()

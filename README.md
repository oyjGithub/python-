# python-
my project about Reptile

1. add get_IP.py that Auto crawl proxy IP address
Store the crawled IP address in the TXT text. When the set proxy IP fails, it will automatically switch the available IP in the text to continue crawling data;

*****IP change function*****

```
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
```

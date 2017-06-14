# coding:utf-8
import urllib
import socket

# 设置全局超时时间为3s，也就是说，如果一个请求3s内还没有响应，就结束访问，并返回timeout（超时）
socket.setdefaulttimeout(3)
f = open("../IP_Proxy/proxy")
lines = f.readlines()
proxys = []
for i in range(0,len(lines)):
    # .ip = lines[i].strip("\n").split("\t")这个是去掉每行末尾的换行符（也就是"\n"）, 然后以制表符（也就是"\t"）分割字符串为字符串数组
    ip = lines[i].strip("\n").split("\t")
    proxy_host = "http://"+ip[0]+":"+ip[1]
    # http代表代理的类型，除了http之外还有https，socket等这里就以http为例
    proxy_temp = {"http":proxy_host}
    proxys.append(proxy_temp)
url = "http://ip.chinaz.com/getip.aspx"
for proxy in proxys:
    try:
        # 其中proxies就是代理。以代理模式访问目标网址
        res = urllib.urlopen(url,proxies=proxy).read()
        print res
    except Exception,e:
        print proxy
        print e
        continue
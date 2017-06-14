# coding:utf-8
import requests
# http://cuiqingcai.com/2556.html
r = requests.get('http://cuiqingcai.com')
print type(r)
print r.status_code
print r.encoding
# print r.text
print r.cookies


 # https 开头的网站，Requests可以为HTTPS请求验证SSL证书，就像web浏览器一样。要想检查某个主机的SSL证书，你可以使用 verify 参数
r = requests.get('https://kyfw.12306.cn/otn/', verify=False)
print r.text

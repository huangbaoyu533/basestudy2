
# coding:utf-8
import urllib2
import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

url = 'http://www.xicidaili.com/nn/1'
req = urllib2.Request(url,headers=header)
res = urllib2.urlopen(req).read()
soup = BeautifulSoup.BeautifulSoup(res)
ips = soup.findAll('tr')
# print "ips:",ips
f = open("../IP_Proxy/proxy","w")

for x in range(1,len(ips)):
    ip = ips[x]
    tds = ip.findAll("td")
    # print "tds:", tds
    ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]+"\n"
    # print tds[1].contents[0]+"\t"+tds[2].contents[0]
    f.write(ip_temp)
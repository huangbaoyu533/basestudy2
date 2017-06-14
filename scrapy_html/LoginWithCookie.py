# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib,re
# 本代码参照http://blog.csdn.net/pleasecallmewhy/article/details/9305229
# 登录南财查看自己的成绩

# 初始化一个CookieJar来处理Cookie的信息#
cookie = cookielib.CookieJar()

# 创建一个新的opener来使用我们的CookieJar#
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

# 需要POST的数据 通过hpptfox的postdata查看,快捷键ctrl+shift+f2打开httpfox
postdata = urllib.urlencode({
    '__VIEWSTATE':	'dDwyMTQxMjc4NDIxOztsPF9jdGwwOkltYWdlQnV0dG9uMTtfY3RsMDpJbWFnZUJ1dHRvbjI7Pj7Az6iIm5Vv7V9KOT8wZn/qRbNehQ==',
    '_ctl0:txtusername':'1120160678',
    '_ctl0:ImageButton1.x':'46',
    '_ctl0:ImageButton1.y':'35',
    '_ctl0:txtpassword':'1120160678'

})

# 自定义一个请求#
req = urllib2.Request(
    url='http://yjsc.njue.edu.cn:8080/pyxx/login.aspx',
    data=postdata
)

# 访问该链接#
result = opener.open(req)

# 打印返回的内容#
# print result.read()

# 打印cookie的值
# for item in cookie:
#     print 'Cookie：Name = ' + item.name
#     print 'Cookie：Value = ' + item.value

# 访问跳转该链接#
result = opener.open('http://yjsc.njue.edu.cn:8080/pyxx/grgl/xskccjcx.aspx')

# 打印返回的内容#
print result.read()

myItems = re.findall('<tr><tb><table><tboy><tr nowrap="nowrap"><td><font .*?>(.*?)</font></td><td><font .*?>(.*?)</font></td><td><font .*?>1</font></td><td><font .*?>(.*?)</font></td></tr></tbody></table></tb></tr>', result.read(),re.S)  # 获取到学分
print 'myitems:',myItems


# 将内容从页面代码中抠出来,没抠成功,源码结构复杂,xpath写的不完整



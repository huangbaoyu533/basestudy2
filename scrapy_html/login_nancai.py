# -*- coding: utf-8 -*-
import urllib
import urllib2

import cookielib
# 本代码参照http://blog.csdn.net/pleasecallmewhy/article/details/9305229
# 登录南财查看自己的成绩

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

# 需要POST的数据#
postdata = urllib.urlencode({
    '__VIEWSTATE': 'dDwyMTQxMjc4NDIxOztsPF9jdGwwOkltYWdlQnV0dG9uMTtfY3RsMDpJbWFnZUJ1dHRvbjI7Pj7Az6iIm5Vv7V9KOT8wZn/qRbNehQ==',
    '_ctl0:txtusername': '1120160678',
    '_ctl0:ImageButton1.x': '46',
    '_ctl0:ImageButton1.y': '35',
    '_ctl0:txtpassword': '1120160678'
})

# 自定义一个请求#
req = urllib2.Request(
    url='http://yjsc.njue.edu.cn:8080/pyxx/login.aspx',
    data=postdata
)

# 访问该链接#
result = opener.open(req)

# 打印返回的内容#
print result.read()





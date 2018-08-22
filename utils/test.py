#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re

m = re.finditer(u"[\u4e00-\u9fa5]+", u'扫描字符串寻找一个位置，addfa在此正则表达式产生的匹配，ddee并返回相应的作法实例。')
list=[(i.span(), i.string) for i in m]

print str(m)
print type(m)
print list

for item in list:
    print item[1][item[0][0]:item[0][1]]


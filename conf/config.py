#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import platform

home_path = None

sys_str = platform.system()
if sys_str == 'Windows':
    home_path = os.environ['USERPROFILE']
else:
    home_path = os.environ['HOME']

# 以下是主要的配置
# BASE_PATH = unicode('/Users/huangiris/WBworkplace/lattice-mai-front-copy/src/')  # 基础路径，需要提取文件的路径
BASE_PATH = unicode(home_path + os.sep + 'trans')  # 基础路径，需要提取文件的路径

OUTPUT_PATH = unicode(home_path + os.sep + 'trans_output')  # json输出路径，不要和上面的路径重合了

# 支持 java vm js jsx
SUFFIX = ['js', 'jsx']  # 要翻译文件后缀名

# PATTERN = u"[\u4e00-\u9fa5]+"  # 匹配模式，连续中文
# PATTERN = u"[\u4e00-\u9fa5][a-zA-Z0-9\u4e00-\u9fa5]*[\u4e00-\u9fa5]"  # 匹配模式，连续中文
PATTERN = u"[\"\'']" \
          u"[\sa-zA-Z0-9:;,\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]*" \
          u"[\u4e00-\u9fa5]+" \
          u"[\sa-zA-Z0-9:;,\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]*" \
          u"[\"\'']"  # 匹配模式

PATTERNPLUS = u"[\u4e00-\u9fa5][a-zA-Z0-9\u4e00-\u9fa5]*[\u4e00-\u9fa5]"  # 连续中文 

if __name__ == '__main__':
    print BASE_PATH


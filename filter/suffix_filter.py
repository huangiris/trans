#!/usr/bin/env python
# -*- coding:utf-8 -*-

from filter import Filter


# 后缀名过滤器 获得特定后缀名的文件
class SuffixFilter(Filter):
    def __init__(self, suffixes):
        """
        :type suffixes: list
        """
        Filter.__init__(self)
        self.suffixes = suffixes

    def filter(self, file_name):
        # type: (str) -> bool
        flag = False
        for suffix in self.suffixes:
            if file_name.endswith(suffix):
                flag = True
                break
        return flag

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from conf.config import BASE_PATH
from filter.suffix_filter import SuffixFilter

# 文件遍历，找到需要的文件
class FileTraverse:
    def __init__(self, file_filter):
        """
        :type file_filter: filter.filter.Filter
        """
        self.filter = file_filter

    def traverse(self, base_folder):
        ret = []
        for root, dirs, files in os.walk(base_folder):
            for file_name in files:
                if self.filter.filter(file_name):
                    ret.append(os.path.join(root, file_name))
        return ret


if __name__ == '__main__':
    t = FileTraverse(SuffixFilter(['txt']))
    print t.traverse(BASE_PATH)

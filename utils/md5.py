#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import os


#  计算文件的md5
def get_file_md5(filename):
    if not os.path.isfile(filename):
        return
    file_hash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        file_hash.update(b)
    f.close()
    return file_hash.hexdigest()

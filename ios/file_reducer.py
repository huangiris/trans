#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import shutil

from conf.config import OUTPUT_PATH
from utils.md5 import get_file_md5


class FileReducer:
    def __init__(self, output_path):
        self.output_path = output_path

    # 根据json写回源程序代码 单个json
    def patch(self, json_file):
        with open(json_file) as json_data:
            d = json.load(json_data)
        if u'file_name' not in d:
            return
        file_name = d[u'file_name']
        path = d[u'path']
        encoding = d[u'encoding']
        data = d[u'data']
        # type: data
        md5 = d[u'md5']
        print file_name
        print path
        print encoding
        print data
        if not os.path.exists(path):
            print 'Error: 找不到源文件！！'
            return
        file_md5 = get_file_md5(path)
        if md5 != file_md5:
            print 'Error: 源文件已经被篡改，不能覆盖！！'
            return
        print '=>验证通过，开始回填数据'
        backup = path + '.backup'
        # shutil.copy(path, backup)  # 备份文件
        with open(path) as f:
            lines = f.readlines()
        unicode_lines = map(lambda s: s.decode(encoding), lines)
        print '======'
        print unicode_lines
        for (k, v) in data.items():
            v.sort(reverse=True, key=lambda x: x['start'])
            for item in v:
                line = unicode_lines[int(k)]
                start = item['start']
                end = item['end']
                trans = item['trans']
                # print start, end, '|', origin, '|', trans
                new_line = line[:start] + trans + line[end:]
                unicode_lines[int(k)] = new_line
        print unicode_lines
        lines = map(lambda s: s.encode(encoding), unicode_lines)
        f = open(path, 'w')
        f.writelines(lines)
        f.close()
        print '<=回填结束'
        print ''

    # 把所有的json都写回去
    def patchAll(self):
        if os.path.exists(self.output_path):
            for root, dirs, files in os.walk(self.output_path):
                for file_path in files:
                    if file_path.endswith('json'):
                        self.patch(os.path.join(self.output_path, file_path))


# if __name__ == '__main__':
#     json_file = '/Users/huangiris/trans_output/t.txt-output.json'
#     reducer = FileReducer(OUTPUT_PATH)
#     reducer.patchAll()

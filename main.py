#!/usr/bin/env python
# -*- coding:utf-8 -*-

from conf.config import BASE_PATH, OUTPUT_PATH, SUFFIX
from filter.suffix_filter import SuffixFilter
from ios.file_reducer import FileReducer
from ios.file_traverse import FileTraverse
import os
import codecs
import json

from ios.resolver_factory import ResolverFactory


def export_json():
    """
      从特定文件夹里提取中文导出json文件
    """
    t = FileTraverse(SuffixFilter(SUFFIX))
    file_list = t.traverse(BASE_PATH)
    dict_map = {}

    for file_path in file_list:
        resolve = ResolverFactory.create_resolver(file_path)
        if resolve:
            ret = resolve.resolve()
            if ret:
                dict_map.update(ret)
    print dict_map
    f = codecs.open(os.path.join(OUTPUT_PATH, 'lang-output.js'), 'w',
                    encoding="utf-8")
    f.write(json.dumps(dict_map, encoding='utf-8', ensure_ascii=False, indent=4))
    f.close()


def patch_file():
    """
      翻译的json文件写回源文件
    """
    reducer = FileReducer(OUTPUT_PATH)
    reducer.patchAll()


def clean_backup():
    """
      将备份文件清理
    """
    for root, dirs, files in os.walk(BASE_PATH):
        for file_name in files:
            if file_name.endswith('backup'):
                os.remove(os.path.join(root, file_name))
    print('清理完成')


if __name__ == '__main__':
    print '程序开始'
    export_json()
    # patch_file()
    # clean_backup()
    print '程序结束'

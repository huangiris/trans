#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ios.resolver import Resolver
import chardet
import json
import codecs
from collections import OrderedDict
import hashlib

import os
import re
from utils.md5 import get_file_md5


class JavaScriptResolver(Resolver):
    def __init__(self, file_path, output_path, pattern, pattern_plus):
        super(JavaScriptResolver, self).__init__()
        self.path = file_path
        self.output_path = output_path
        self.pattern = pattern
        self.pattern_plus = pattern_plus

    def transform_simple(self, origin):
        return '{trans[\'' + origin + '\']}'

    # 从原始的文字转换成要的语言串
    def transform(self, origin, text, start, end, lines, seq):
        st = start - 1
        ch = text[start - 1]
        flag = self.is_in_tag(origin, text, start, end, lines, seq)
        st = start - 1
        while True:
            if st <= -1:
                break
            ch = text[st]
            if ch != ' ':
                break
            else:
                st = st - 1

        if '=' == ch and flag:
            if st - 1 > 0 and text[st - 1] == '=':
                return 'trans[\'' + origin[1:-1] + '\']'
            else:
                return '{trans[\'' + origin[1:-1] + '\']}'
        else:
            return 'trans[\'' + origin[1:-1] + '\']'

    # 找到的字符串是否在标签内
    def is_in_tag(self, origin, text, start, end, lines, seq):
        flag = False
        c_seq = seq
        c_index = end
        while True:
            if c_seq >= len(lines):
                break
            c_line = lines[c_seq]
            if c_index >= len(c_line):
                c_index = 0
                c_seq += 1
                continue
            ch = c_line[c_index]
            if ch == '>':
                if c_index - 1 >= 0 and c_line[c_index - 1] == '=':
                    pass
                else:
                    flag = True
                    break
            if ch == '<':
                break
            c_index += 1
        if flag:
            return flag
        c_seq = seq
        c_index = start - 1
        while True:
            if c_seq < 0:
                break
            c_line = lines[c_seq]
            if c_index < 0:
                c_seq -= 1
                if c_seq >= 0:
                    c_index = len(lines[c_seq]) - 1
                continue
            ch = c_line[c_index]
            if ch == '<':
                flag = True
                break
            if ch == '>':
                break
            c_index -= 1

        return flag

    # 该行是否是注释
    def is_comment(self, text):
        t_text = text.strip()
        if t_text.startswith('*') or t_text.startswith('//'):
            return True
        return False

    # 解析器，将源文件解析成json
    def resolve(self):
        file_name = unicode(os.path.basename(self.path))
        f = open(self.path)
        code = chardet.detect(f.read())
        f.seek(0, 0)
        lines = f.readlines()
        f.close()
        try:
            unicode_lines = map(lambda s: s.decode(code['encoding']), lines)
        except UnicodeDecodeError as e:
            print('fail to decode file: ', file_name)
            print('except: ', e)
            return
        data = {}
        # dict_map 保存找到的中文串
        dict_map = {}
        sort_order_data = ['text', 'start', 'end', 'origin', 'trans', 'auto']

        for seq in xrange(len(unicode_lines)):
            if self.is_comment(unicode_lines[seq]):
                continue
            # 匹配第一个正则表达式
            m = re.finditer(self.pattern, unicode_lines[seq])
            m_list = [i.span() for i in m]
            if len(m_list) > 0:
                data[seq] = []
                for item in m_list:
                    item_data = {
                        'text': unicode_lines[seq],
                        'start': item[0],
                        'end': item[1],
                        'origin': unicode_lines[seq][item[0]:item[1]],
                        'trans': self.transform((unicode_lines[seq][item[0]:item[1]]), unicode_lines[seq], item[0],
                                                item[1], unicode_lines, seq),
                        'auto': ''
                    }
                    # 保存中文串
                    dict_map[unicode_lines[seq][item[0]:item[1]][1:-1]] = unicode_lines[seq][item[0]:item[1]][1:-1];
                    # 排序字典
                    data_ordered = OrderedDict(
                        sorted(item_data.iteritems(), key=lambda (k, v): sort_order_data.index(k)))
                    data[seq].append(data_ordered)

            # 匹配第二个正则表达式
            # print 'second'
            m = re.finditer(self.pattern_plus, unicode_lines[seq])
            m_list = [i.span() for i in m]
            if len(m_list) > 0:
                if seq not in data:
                    data[seq] = []
                for item in m_list:
                    start = item[0]
                    end = item[1]
                    if not self.is_item_include(start, end, data[seq]):
                        # print item
                        # print unicode_lines[seq][item[0]:item[1]]
                        item_data = {
                            'text': unicode_lines[seq],
                            'start': item[0],
                            'end': item[1],
                            'origin': unicode_lines[seq][item[0]:item[1]],
                            'trans': self.transform_simple((unicode_lines[seq][item[0]:item[1]])),
                            'auto': ''
                        }
                        # 保存中文串
                        dict_map[unicode_lines[seq][item[0]:item[1]][1:-1]] = unicode_lines[seq][item[0]:item[1]][1:-1];
                        # 排序字典
                        data_ordered = OrderedDict(
                            sorted(item_data.iteritems(), key=lambda (k, v): sort_order_data.index(k)))
                        data[seq].append(data_ordered)

        ret = {
            'path': unicode(self.path),
            'file_name': file_name,
            'md5': get_file_md5(self.path),
            'encoding': code['encoding'],
            'data': data,
        }
        sort_order = ['file_name', 'md5', 'path', 'encoding', 'data']
        ret_ordered = OrderedDict(sorted(ret.iteritems(), key=lambda (k, v): sort_order.index(k)))

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        if len(data) <= 0:
            return

        f = codecs.open(
            os.path.join(self.output_path, file_name + '-' + hashlib.md5(self.path).hexdigest() + '-output.json'), 'w',
            encoding="utf-8")
        f.write(json.dumps(ret_ordered, encoding='utf-8', ensure_ascii=False, indent=4))
        f.close()
        return dict_map

    def is_item_include(self, start, end, data_list):
        for item in data_list:
            i_start = item['start']
            i_end = item['end']
            if i_start <= start <= i_end or i_start <= end <= i_end:
                return True
        return False


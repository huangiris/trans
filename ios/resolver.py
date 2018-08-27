#!/usr/bin/env python
# -*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod


# 解析器
class Resolver:
    __metaclass__ = ABCMeta

    def __init__(self): pass

    # 解析器，将源文件解析成json
    @abstractmethod
    def resolve(self): pass

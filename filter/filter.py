#!/usr/bin/env python
# -*- coding:utf-8 -*-
# abc 用于实现抽象类
from abc import ABCMeta, abstractmethod

# 过滤器
class Filter:
    __metaclass__ = ABCMeta

    def __init__(self): pass

    @abstractmethod
    def filter(self, file_name): pass

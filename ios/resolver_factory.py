#!/usr/bin/env python
# -*- coding:utf-8 -*-
from conf.config import OUTPUT_PATH, PATTERN, PATTERNPLUS
from ios.java_resolver import JavaResolver
from ios.javascript_resolver import JavaScriptResolver
from ios.velocity_resolver import VelocityResolver


class ResolverFactory:
    """
    解析器工厂
    """

    def __init__(self):
        pass

    @staticmethod
    def create_resolver(path):
        resolver = None
        if path.endswith('js') or path.endswith('jsx'):
            resolver = JavaScriptResolver(path, OUTPUT_PATH, PATTERN, PATTERNPLUS)
        elif path.endswith('java'):
            resolver = JavaResolver(path, OUTPUT_PATH, PATTERN, PATTERNPLUS)
        elif path.endswith('vm'):
            resolver = VelocityResolver(path, OUTPUT_PATH, PATTERN, PATTERNPLUS)
        return resolver



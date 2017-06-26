#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://blog.thekondor.net/2011/11/python-make-configparser-aware-of.html
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

class SpaceAwareConfigParser(ConfigParser.ConfigParser):
    def __init__(self, *args, **kwargs):
        self.__keep_spaces = True
        ConfigParser.ConfigParser.__init__(self, *args, **kwargs)

    def get(self, section, option, raw=False, vars=None, fallback=None):
        value = ConfigParser.ConfigParser.get(self, section, option, raw=raw, vars=vars, fallback=fallback)
        if self.__keep_spaces:
            value = self._unwrap_quotes(value)

        return value

    def set(self, section, option, value):
        if self.__keep_spaces:
            value = self._wrap_to_quotes(value)
        ConfigParser.ConfigParser.set(self, section, option, value)

    @staticmethod
    def _unwrap_quotes(src):
        QUOTE_SYMBOLS = ('"', "'")
        for quote in QUOTE_SYMBOLS:
            if src.startswith(quote) and src.endswith(quote):
                return src.strip(quote)
        return src

    @staticmethod
    def _wrap_to_quotes(src):
        if src and src[0].isspace():
            return '"%s"' % src
        return src

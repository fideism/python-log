#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Date    : 2017-06-29 10:25:40
# @Author  : hyc

import os

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

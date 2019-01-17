#!/usr/bin/env python3.5
#coding:utf-8

import os
import sys
import logging
import logging.handlers
import time

class LogBase(object):
    def __init__(self, message, level = 'info'):
        """
            init params
        """
        fback = sys._getframe().f_back
        self.message = '[%s-%s] - %s' % (fback.f_code.co_filename, fback.f_lineno, message)
        self.level = level.upper()
        self.path_file = 'log/runtime'
        self.__writeLog()

    def __writeLog(self):
        """
            set log
        """
        handler = self.__getLogHandler()
        logger = logging.getLogger()  
        logger.addHandler(handler) 
        logger.setLevel('NOTSET')

        if self.level == 'CRITICAL':  
            logger.critical(self.message)
        elif self.level == 'ERROR':   
            logger.error(self.message)   
        elif self.level == 'WARNING': 
            logger.warning(self.message) 
        elif self.level == 'INFO':    
            logger.info(self.message)    
        elif self.level == 'DEBUG':   
            logger.debug(self.message)   
        elif self.level == 'NOTSET':  
            logger.debug(self.message)   

    def __getLogHandler(self):
        """
            get log handler
        """
        filename = self.path_file + '-' + time.strftime("%Y-%m-%d", time.localtime(int(time.time()))) + '.log'
        handler = logging.handlers.RotatingFileHandler(filename, maxBytes = 1024*1024, backupCount = 5) 
        #fmt = '%(asctime)s - [%(levelname)s] - [%(pathname)s/%(module)s/%(funcName)s] - [%(filename)s:%(lineno)s] - %(message)s'
        fmt = '%(asctime)s - [%(levelname)s] - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        return handler

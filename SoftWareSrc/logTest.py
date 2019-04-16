# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 15:26:18 2019

@author: xwl99
"""

import logging
logger = logging.getLogger() #定义对应的程序模块名name，默认是root
#logger.setLevel(logging.DEBUG) #指定最低的日志级别
ch = logging.StreamHandler() #日志输出到屏幕控制台
ch.setLevel(logging.WARNING) #设置日志等级
#formatter = logging.Formatter('%(asctime)s %(name)s- %(levelname)s - %(message)s') #定义日志输出格式
fh = logging.FileHandler('access.log')#向文件access.log输出日志信息
fh.setLevel(logging.INFO) #设置输出到文件最低日志级别
#fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info('tset')
logger.debug('tsetD')
logger.error('tsetE')
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 20:25:47 2019

@author: xwl99
"""

import struct

s='dsfsdf'.encode()
a=struct.pack('i',len(s))

l,d=struct.unpack('is',a)
print(d)
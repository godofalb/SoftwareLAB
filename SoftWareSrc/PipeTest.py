# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:42:49 2019

@author: xwl99
"""

import subprocess

f=open('oo.test', 'w') 
f2=open('oo.test', 'r') 
f.write('fsdfsdf\n')
f.flush()
filec=f2.read()
print(filec)
f.write('fsdffffff\n')
f.flush()
filec=f2.read()
print(filec)



    

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:15:49 2019

@author: xwl99
"""

import re

testPacakge="[username,pwd]dir"
pattern=r"\[(.*?),(.*?)\].*"#
r=re.match(pattern,testPacakge)
print (r,r[2])
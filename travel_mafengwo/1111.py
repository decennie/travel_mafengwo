#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "decennie"
__date__ = "2019/3/18 "

a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
c=""
for i in a:
    c += str(i)
    ",".join(c)
print(",".join(c))

s = ','.join([i for i in a])
print(s)

print(",".join(a))


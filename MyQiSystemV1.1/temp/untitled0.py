# -*- coding: utf-8 -*-
"""
Created on Tue May 28 19:57:04 2019

@author: Administrator
"""

from multiprocessing import Pool


def f(x,y=9):
    print(x*y)

if __name__ == '__main__':
    with Pool(5) as p:
        p.map(f,(1,2,3),(2,3,4))
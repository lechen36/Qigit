#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 20:42:58 2019

@author: mac
"""

import pandas as pd
all_return_info=pd.DataFrame(columns=['ts_code','num','return_final','return_average'])
all_return_info['ts_code']=['101','102','103','104']
all_return_info.set_index('ts_code',inplace=True)
all_return_info['num']=[102,13,2,23]
a1=all_return_info['num'].max()

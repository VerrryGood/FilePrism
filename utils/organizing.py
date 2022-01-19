# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 16:21:04 2021

@author: python
"""

import os
import datetime as dt
import pandas as pd

class organizing():
    def __init__(self, dirname):
        self.dirname = dirname
        self.fullname_list = list()
        
        self.get_rawlist(self.dirname)
        self.df_fullname = pd.DataFrame(self.fullname_list, columns=['Directory',
                                                                     'Filename',
                                                                     'Extension',
                                                                     'Filesize',
                                                                     'Recent_year',
                                                                     'Recent_month'])
        
    def get_rawlist(self, dirname):
        try:
            for_long_path = "\\\\?\\"
            file_or_folder = os.listdir(dirname)
            for x in file_or_folder:
                if len(os.path.join(dirname, x)) >= 260:
                    full_filename = for_long_path + os.path.join(dirname, x)
                else:
                    full_filename = os.path.join(dirname, x)
                if os.path.isdir(full_filename):
                    self.get_rawlist(full_filename)
                else:
                    filename = os.path.splitext(x)[0]
                    ext = os.path.splitext(full_filename)[-1]
                    size_of_file = round(os.path.getsize(full_filename)/1024)
                    rc_year = dt.date.fromtimestamp(os.path.getmtime(full_filename)).year
                    rc_month = dt.date.fromtimestamp(os.path.getmtime(full_filename)).month
                    self.fullname_list.append([dirname,
                                                    filename,
                                                    ext,
                                                    size_of_file,
                                                    rc_year,
                                                    rc_month])
        except PermissionError:
            pass
            
            
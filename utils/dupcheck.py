# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 10:55:06 2021

@author: python
"""

import os

class Dupcheck():
    def __init__(self, df_filelist):
        self.checking(df_filelist)
        
    def checking(self, df_filelist):
        dup_file = df_filelist.loc[:, ['Filename', 'Extension']].value_counts()
        for i in range(len(dup_file)):
            if dup_file[i] >= 2:
                self.changing(df_filelist, dup_file, i)
    
    def changing(self, df_filelist, dup_file, index_number):
        dup_count = 1
        temp = df_filelist[(df_filelist['Filename'] == dup_file.index[index_number][0]) & (df_filelist['Extension'] == dup_file.index[index_number][1])]
        for j in range(1, len(temp)):
            old_name = os.path.join(df_filelist['Directory'][temp.index[j]],
                                    df_filelist['Filename'][temp.index[j]]) + df_filelist['Extension'][temp.index[j]]
            new_name = os.path.join(df_filelist['Directory'][temp.index[j]],
                                    df_filelist['Filename'][temp.index[j]] + "_same%02d" % dup_count) + df_filelist['Extension'][temp.index[j]]
            os.rename(old_name, new_name)
            dup_count += 1
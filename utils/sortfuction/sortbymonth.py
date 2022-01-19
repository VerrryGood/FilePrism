# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 17:38:40 2021

@author: python
"""

import os
import shutil

class Sortbymonth():
    def __init__(self, working_dir, complete_dir, df_filelist):
        self.working_dir = working_dir
        self.complete_dir = complete_dir
        if self.working_dir == self.complete_dir:
            print("정리할 폴더 경로와 정리 후 폴더 경로가 같습니다.")
        else:
            self.sorting(df_filelist)
            
    def sorting(self, df_filelist):
        temp = df_filelist['Recent_month'].value_counts()
        if not os.path.exists(self.complete_dir):
            os.makedirs(self.complete_dir)
            
        for i in range(len(temp)):
            month_dir = temp.index[i]
            month_folder = os.path.join(self.complete_dir, "%02d" % month_dir + "월")
            
            self.moving(month_folder, self.working_dir, df_filelist, month_dir)
                
        self.deleting(df_filelist, self.working_dir)
                
    def moving(self, month_folder, working_dir, df_filelist, month_dir):
        if not os.path.exists(month_folder):
            os.makedirs(month_folder)
        
        temp_df = df_filelist.loc[df_filelist['Recent_month'] == month_dir].copy()
        
        for x in temp_df.itertuples():
            try:
                shutil.move(os.path.join(x[1], x[2]) + x[3], month_folder)
            except:
                pass
                
                
    def deleting(self, df_filelist, working_dir):
        for d in df_filelist['Directory'].value_counts().index:
            if d == working_dir:
                pass
            else:
                if os.path.exists(d):
                    try:
                        os.rmdir(d)
                    except OSError:
                        pass
        
        
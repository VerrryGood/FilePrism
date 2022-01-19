# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 17:38:40 2021

@author: python
"""

import os
import shutil

class Sortbyext():
    def __init__(self, working_dir, complete_dir, df_filelist):
        self.working_dir = working_dir
        self.complete_dir = complete_dir
        if self.working_dir == self.complete_dir:
            print("정리할 폴더 경로와 정리 후 폴더 경로가 같습니다.")
        else:
            self.sorting(df_filelist)
    
    def sorting(self, df_filelist):
        temp = df_filelist['Extension'].value_counts()
        if not os.path.exists(self.complete_dir):
            os.makedirs(self.complete_dir)
            
        for i in range(len(temp)):
            if temp.values[i] >= 2:
                ext_dir = temp.index[i].replace(".", "").upper()
                ext_folder = os.path.join(self.complete_dir, ext_dir)
                
                self.moving(ext_folder, self.working_dir, df_filelist, temp, i)
                
            else:
                ext_folder = os.path.join(self.complete_dir, "기타")
                
                self.moving(ext_folder, self.working_dir, df_filelist, temp, i)
                
        self.deleting(df_filelist, self.working_dir)
                
    def moving(self, ext_folder, working_dir, df_filelist, temp, index_number):
        if not os.path.exists(ext_folder):
            os.makedirs(ext_folder)
        
        condition = df_filelist['Extension'].str.contains(temp.index[index_number])
        temp_df = df_filelist.loc[condition].copy()
        
        for x in temp_df.itertuples():
            try:
                shutil.move(os.path.join(x[1], x[2]) + x[3], ext_folder)
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
                    
        
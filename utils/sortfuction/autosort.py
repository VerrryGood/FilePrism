# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 14:23:46 2021

@author: python
"""

import os
import shutil
import re
import operator
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.tag import pos_tag

class Autosort():
    def __init__(self, working_dir, complete_dir, df_filelist):
        self.working_dir = working_dir
        self.complete_dir = complete_dir
        if self.working_dir == self.complete_dir:
            print("정리할 폴더 경로와 정리 후 폴더 경로가 같습니다.")
        else:
            self.tagging(df_filelist)
            self.sorting(df_filelist)
            
    def tagging(self, df_filelist):
        tag_list = list()
        tag_count = {}
        retokenize = RegexpTokenizer("[\w]+")
        
        for f in df_filelist['Filename']:
            refining = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'_…》]', ' ', re.sub(r'[0-9]+', '', f))
            temp = pos_tag(retokenize.tokenize(refining))
            noun_refining = [n[0] for n in temp if "NN" in n[1]]
            for n in noun_refining:
                if len(n)==1:
                    noun_refining.remove(n)
            for i in range(len(noun_refining)):
                noun_refining[i] = noun_refining[i].lower()
                if noun_refining[i] not in tag_count:
                    tag_count[noun_refining[i]] = 0
                tag_count[noun_refining[i]] += 1
            tag_list.append(noun_refining)
            
        tag_count_sort = sorted(tag_count.items(), key=operator.itemgetter(1), reverse=True)
        sel_tag_list = ["" for i in range(len(df_filelist))]
        
        for i in range(len(tag_count_sort)):
            for j in range(len(tag_list)):
                if tag_count_sort[i][0] in tag_list[j]:
                    if sel_tag_list[j] == "":
                        sel_tag_list[j] = tag_count_sort[i][0]
                    else:
                        pass
                    
        for i in range(len(sel_tag_list)):
            if sel_tag_list[i] == "":
                sel_tag_list[i] = "기타"
                
        df_filelist['Tag'] = pd.Series(sel_tag_list)
        
    def sorting(self, df_filelist):
        temp = df_filelist['Tag'].value_counts()
        if not os.path.exists(self.complete_dir):
            os.makedirs(self.complete_dir)
            
        for i in range(len(temp)):
            auto_dir = temp.index[i].capitalize()
            auto_folder = os.path.join(self.complete_dir, auto_dir)
            
            self.moving(auto_folder, self.working_dir, df_filelist, temp, i)
            
        self.deleting(df_filelist, self.working_dir)
            
    def moving(self, auto_folder, working_dir, df_filelist, temp, index_number):
        if not os.path.exists(auto_folder):
            os.makedirs(auto_folder)
            
        temp_df = df_filelist[df_filelist['Tag'] == temp.index[index_number]].copy()
        
        for x in temp_df.itertuples():
            try:
                shutil.move(os.path.join(x[1], x[2]) + x[3], auto_folder)
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
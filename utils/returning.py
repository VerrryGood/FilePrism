# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 18:12:41 2021

@author: python
"""

import os
import shutil
import pandas as pd

class returning():
    def __init__(self, working_dir, job_done, df_filelist, df_origin):
        self.working_dir = working_dir
        self.df_join = pd.merge(df_filelist, df_origin, on=['Filename', 'Extension'])
        self.commencing(self.df_join)
        
    def commencing(self, df_join):
        for i in range(len(df_join)):
            if not os.path.exists(df_join.loc[:, 'Directory_y'][i]):
                os.makedirs(df_join.loc[:, 'Directory_y'][i])
            shutil.move(os.path.join(df_join.loc[:, 'Directory_x'][i],
                                     df_join.loc[:, 'Filename'][i]) +
                        df_join.loc[:, 'Extension'][i],
                        df_join.loc[:, 'Directory_y'][i])
            
        temp_del = df_join['Directory_x'].value_counts().index
        
        for d in temp_del:
            if d == self.working_dir:
                pass
            else:
                if os.path.exists(d):
                    try:
                        os.rmdir(d)
                    except OSError:
                        pass
                    
                    
                    

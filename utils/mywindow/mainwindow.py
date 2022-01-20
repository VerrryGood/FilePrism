# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 14:05:46 2022

@author: python
"""

import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from utils.mywindow import upperwindow as upw

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initWindow()
        
    def initWindow(self):
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)
        
        self.setWindowTitle('File Prism')
        self.setWindowIcon(QIcon('Icon.png'))
        self.setMinimumSize(900, 900)
        self.move_to_center()
        self.show()
    
    def move_to_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
class MainWidget(QWidget):
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.canvas_clear = False
        self.zero_file = False
        
        self.fig = plt.Figure(figsize=(10, 7))
        self.fig.tight_layout()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.initUI()
        
    def initUI(self):
        self.upper = upw.UpperWindow(self).upper
        self.lower_window()
        
        self.main_vbox = QVBoxLayout()
        self.main_vbox.addLayout(self.upper)
        self.main_vbox.addWidget(self.lower)
        
        self.setLayout(self.main_vbox)
        
        
    def lower_window(self):
        self.lower = QGroupBox('폴더 용량 분석')
        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.canvas)
        self.lower.setLayout(self.vbox2)
        self.canvas.draw()
        
    def pie_chart(self, dirname, df_filelist):
        self.refining(df_filelist)
        
        if self.canvas_clear:
            self.clearing()
            
        self.labels = self.ref_df.index
        self.explode = [0.01 for i in range(len(self.labels))]
        self.wedgeprops = {'width' : 0.7, 'edgecolor' : 'w', 'linewidth' : 1}
        self.colors = sns.color_palette('deep')
        self.colors[1], self.colors[2] = self.colors[2], self.colors[1]
        
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('\'' + dirname + '\'' + '의 폴더별 용량 크기', fontdict={'fontsize':15, 'fontweight':'bold'}, pad=30)
        
        self.wedges, self.texts, self.pcts = self.ax.pie(self.ref_df, explode=self.explode, autopct=lambda pct: self.polishing(pct, self.ref_df), pctdistance=0.8,
                                                         wedgeprops=self.wedgeprops, startangle=90, radius=0.8, colors=self.colors)
        
        self.kw = dict(arrowprops=dict(arrowstyle="-"), zorder=0, va="center")
        
        for i, p in enumerate(self.wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            yc = np.arcsin(y) / (np.pi / 2)
            horizontalalignment = {-1: "right", 1:"left"}[int(np.sign(x))]
            connectionstyle = f'angle,angleA=0,angleB={ang}'
            self.kw["arrowprops"].update({"connectionstyle": connectionstyle})
            self.ax.annotate(self.labels[i], xy=(0.8 * x, 0.8 * y), xytext=((1.0 + (i % 2) * 0.4) * np.sign(x), 1.4 * yc),
                             horizontalalignment=horizontalalignment, fontsize=9, **self.kw)
            
        for t in self.pcts:
            t.set_fontsize(9)
            
        self.canvas.draw()
            
        self.canvas_clear = True
        
    def polishing(self, pct, allvals):
        absolute = np.round(np.round(pct/100.*np.sum(allvals))/1024, 1)
        if absolute > 1024:
            final_val = np.round(absolute/1024, 1)
            return "{:.1f}%\n({:.1f}GB)".format(pct, final_val)
        else:
            final_val = absolute
            return "{:.1f}%\n({:.1f}MB)".format(pct, final_val)
        
    def clearing(self):
        self.ax.figure.clear()
        
    def refining(self, df_filelist):
        self.grouped_df = df_filelist['Filesize'].groupby(df_filelist['Directory']).sum()
        del_list = list()
        rest_value = 0
        
        for i in range(len(self.grouped_df)):
            if round(self.grouped_df[i]/self.grouped_df.sum()*100, 1) < 2:
                del_list.append(self.grouped_df.index[i])
                rest_value += self.grouped_df[i]
             
        if len(del_list) == 0 or len(del_list) == 1:
            self.ref_df = self.grouped_df.sort_values()
        else:
            self.ref_df = self.grouped_df.drop(del_list).copy()
            self.ref_df['기타'] = rest_value
            self.ref_df = self.ref_df.sort_values()
        

        
        

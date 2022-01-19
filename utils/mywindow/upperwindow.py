# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 12:13:01 2022

@author: python
"""

import re
import pandas as pd
import time as t

from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtCore import *

from utils import organizing as org, dupcheck as dup, returning as ret
from utils.sortfuction import sortbyext as stext, sortbyyear as styear, sortbymonth as stmonth, autosort as atsort

class UpperWindow(QWidget):
    def __init__(self, parent=None):
        super(UpperWindow, self).__init__(parent)
        self.working_dir = ""
        self.jobdone_dir = ""
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
        
        self.groupbox1 = QGroupBox()
        
        self.title = QLabel('파일 프리즘', self)
        self.title.setAlignment(Qt.AlignCenter)
        self.setting_font(self.title, 18)
        
        self.working_text = QLineEdit()
        self.working_text.setToolTip('수동으로 수정한 경우엔 반드시 Enter키를 입력해주세요.')
        self.working_text.returnPressed.connect(self.setting_working_dir)
        
        self.jobdone_text = QLineEdit()
        self.jobdone_text.setToolTip('수동으로 수정한 경우엔 반드시 Enter키를 입력해주세요.')
        self.jobdone_text.returnPressed.connect(self.setting_jobdone_dir)
        
        self.working_btn = QPushButton('작업 폴더 열기', self)
        self.working_btn.setToolTip('작업할 폴더를 선택해주세요.')
        self.working_btn.clicked.connect(self.open_working_dir)
        
        self.jobdone_btn = QPushButton('작업 완료 폴더 열기', self)
        self.jobdone_btn.setToolTip('정리된 파일들이 저장될 폴더를 선택해주세요.')
        self.jobdone_btn.clicked.connect(self.open_jobdone_dir)
        
        self.grid = QGridLayout()
        self.grid.addWidget(self.working_btn, 0, 0)
        self.grid.addWidget(self.working_text, 0, 1)
        self.grid.addWidget(self.jobdone_btn, 1, 0)
        self.grid.addWidget(self.jobdone_text, 1, 1)
        self.groupbox1.setLayout(self.grid)
        
        self.groupbox2 = QGroupBox('원하는 정리 방식 선택')
        self.groupbox2.setEnabled(False)
        
        self.stext = QRadioButton('확장자별')
        self.stext.setToolTip('파일을 확장자별로 정리해줍니다.')
        self.stext.setChecked(True)
        self.styear = QRadioButton('년도별')
        self.styear.setToolTip('파일을 년도별로 정리해줍니다.')
        self.stmonth = QRadioButton('월별')
        self.stmonth.setToolTip('파일을 월별로 정리해줍니다.')
        self.atsort = QRadioButton('자동')
        self.atsort.setToolTip('파일을 자동으로 정리해줍니다.')
        
        self.explanation = QLabel('※ 프로그램을 종료하면 \'되돌리기\' 버튼으로 원 상태로 되돌릴 수 없습니다.\n 프로그램을 종료하시기 전에 결과물을 확인해보시고 종료해주세요.')
        self.explanation.setAlignment(Qt.AlignCenter)
        self.setting_font(self.explanation, 11)
        
        self.sort_rightnow = QPushButton('정리 시작', self)
        self.sort_rightnow.setToolTip('정리를 시작합니다.')
        self.sort_rightnow.clicked.connect(self.sorting)
        
        self.return_to_origin = QPushButton('되돌리기', self)
        self.return_to_origin.setToolTip('원 상태로 되돌립니다.')
        self.return_to_origin.setEnabled(False)
        self.return_to_origin.clicked.connect(self.returning)
        
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.stext)
        self.hbox1.addWidget(self.styear)
        self.hbox1.addWidget(self.stmonth)
        self.hbox1.addWidget(self.atsort)
        
        self.hbox2 = QHBoxLayout()
        self.hbox2.addStretch(1)
        self.hbox2.addWidget(self.sort_rightnow)
        self.hbox2.addWidget(self.return_to_origin)
        self.hbox2.addStretch(1)
        
        self.vbox1 = QVBoxLayout()
        self.vbox1.addLayout(self.hbox1)
        self.vbox1.addSpacing(5)
        self.vbox1.addWidget(self.explanation)
        self.vbox1.addSpacing(5)
        self.vbox1.addLayout(self.hbox2)
        self.groupbox2.setLayout(self.vbox1)
        
        self.upper = QFormLayout()
        self.upper.addRow(self.title)
        self.upper.addRow(self.groupbox1)
        self.upper.setVerticalSpacing(15)
        self.upper.addRow(self.groupbox2)
        
    def setting_font(self, label, font_size):
        font = label.font()
        font.setPointSize(font_size)
        font.setFamily('Malgun Gothic')
        font.setBold(True)
        label.setFont(font)
        
    def open_working_dir(self):
        dirname = QFileDialog.getExistingDirectory(self, '폴더 선택')
        
        if "Program Files" in dirname:
            self.declining("Program Files")
        elif "Program Files (x86)" in dirname:
            self.declining("Program Files (x86)")
        elif "Windows" in dirname:
            self.declining("Windows")
        else:
            self.working_text.setText(dirname)
            self.setting_working_dir()
        pass
    
    def open_jobdone_dir(self):
        dirname = QFileDialog.getExistingDirectory(self, '폴더 선택')
        
        self.jobdone_text.setText(dirname)
        self.setting_jobdone_dir()
    
    def setting_working_dir(self):
        text = self.working_text.text()
        self.working_dir = re.sub('/', '\\\\', text)
        
        if self.working_dir == "" and self.jobdone_dir == "":
            pass
        elif self.working_dir == self.jobdone_dir:
            self.warningmessage()
            self.working_text.clear()
            self.working_dir = ""
        else:
            self.organize_and_draw()
            self.setting_on()
        
    def setting_jobdone_dir(self):
        text = self.jobdone_text.text()
        self.jobdone_dir = re.sub('/', '\\\\', text)
        
        if self.working_dir == "" and self.jobdone_dir == "":
            pass
        elif self.jobdone_dir == self.working_dir:
            self.warningmessage()
            self.jobdone_text.clear()
            self.jobdone_dir = ""
        else:
            self.setting_on()
                
    def setting_on(self):
        if self.working_dir != "" and self.jobdone_dir != "":
            self.groupbox2.setEnabled(True)
        elif self.working_dir == "" or self.jobdone_dir == "":
            self.groupbox2.setEnabled(False)
                
    def organize_and_draw(self):
        self.df_current = org.organizing(self.working_dir).df_fullname.copy()
        
        if len(self.df_current) == 0:
            self.zeromessage(self.working_dir)
            self.parent.clearing()
        else:
            self.parent.pie_chart(self.working_dir, self.df_current)
            
    def jobdone_and_draw(self):
        self.df_current = org.organizing(self.jobdone_dir).df_fullname.copy()
        
        if len(self.df_current) == 0:
            self.zeromessage(self.jobdone_dir)
            self.parent.clearing()
        else:
            self.parent.pie_chart(self.jobdone_dir, self.df_current)
                
    def sorting(self):
        dup.Dupcheck(self.df_current)
        self.df_current = org.organizing(self.working_dir).df_fullname.copy()
        self.df_origin = pd.DataFrame.copy(self.df_current.loc[:, ["Directory", "Filename", "Extension"]])
        
        if self.stext.isChecked():
            stext.Sortbyext(self.working_dir, self.jobdone_dir, self.df_current)
        elif self.styear.isChecked():
            styear.Sortbyyear(self.working_dir, self.jobdone_dir, self.df_current)
        elif self.stmonth.isChecked():
            stmonth.Sortbymonth(self.working_dir, self.jobdone_dir, self.df_current)
        elif self.atsort.isChecked():
            atsort.Autosort(self.working_dir, self.jobdone_dir, self.df_current)
            
        self.jobdone_and_draw()
        
        self.sort_rightnow.setEnabled(False)
        self.return_to_origin.setEnabled(True)
        
    def declining(self, flname):
        QMessageBox.information(self, '주의', flname+"이(가) 포함되지 않아야 합니다.")
        
    def warningmessage(self):
        QMessageBox.information(self, '주의', "정리할 폴더와 정리 후 폴더가 같습니다.")
        
    def zeromessage(self, flname):
        QMessageBox.information(self, '확인', flname+"이(가) 비었습니다.")
        
    def returning(self):
        ret.returning(self.working_dir, self.jobdone_dir, self.df_current, self.df_origin)
        self.organize_and_draw()
        self.sort_rightnow.setEnabled(True)
        self.return_to_origin.setEnabled(False)
    

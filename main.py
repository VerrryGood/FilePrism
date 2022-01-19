# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 16:19:23 2021

@author: python
"""

import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from utils.mywindow import mainwindow as mw

if __name__ == "__main__":
    plt.rc('font', family='Malgun Gothic')    
    app = QApplication(sys.argv)
    window = mw.MyApp()
    sys.exit(app.exec_())
    

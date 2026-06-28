#BlackCode
#Github: https://github.com/nullBlackCode

#Graphical and Colors Modules 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import (
    QSettings, QFile, QDir
)

#Color terminal
from colorama import Fore

#Netword Modules 
import requests

#System Modules
import time
import os
import sys
from subprocess import getoutput

#---------------------------------

#Main window
class Windows:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window_main = QWidget()

    def MainWindow(self):
        #Main window
        self.window_main.setWindowTitle("BlackCode | AutoVule")
        self.window_main.resize(990, 600)
        self.window_main.show()
        
        

        sys.exit(self.app.exec_())


if __name__ == "__main__":
    window_main = Windows()
    window_main.MainWindow()


    
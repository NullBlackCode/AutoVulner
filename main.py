#BlackCode
#Github: https://github.com/nullBlackCode

#Graphical and Colors Modules 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import (
    QSettings
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
    app = QApplication(sys.argv)
    window_main = QWidget()
    window_main.setWindowTitle("BlackCode | AutoVule")
    window_main.resize(990, 600)
    window_main.setBackgroundRole

    window_main.show()

    sys.exit(app.exec_())
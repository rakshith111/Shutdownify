import sys
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from qtmainui import Ui_Dialog


app = QtWidgets.QApplication(sys.argv)
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()
sys.exit(app.exec_())

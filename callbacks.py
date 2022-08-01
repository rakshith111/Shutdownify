import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel

from functools import partial
from PyQt5.QtCore import pyqtSlot


class callback():
    def main():
        pass

    def submit(self, hours, minuits, seconds):
        print(hours, minuits, seconds)
        self.hrs = int(hours)
        self.min = int(minuits)
        self.sec = int(seconds)
        self.final = self.hrs*3600+self.min*60+self.sec
        print(self.final)
        subprocess.run(["shutdown", "-s", "-t", f"{self.final}"],  shell=True,
                       stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # def extend():
    #     subprocess.run(["shutdown", "-a"],  shell=True, stdout=subprocess.PIPE,
    #                    stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #     functions.submit()

    def cancel(self):
        # if you want to cancel
        subprocess.run(["shutdown", "-a"],  shell=True, stdout=subprocess.PIPE,
                       stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled.ui', self)
     
        self.show()
        self.pushButton.clicked.connect(self.pushButton_handler)

    def pushButton_handler(self):
        print("hhdvcjhsvjvjsj")
        self.open_dialog_box()

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        path= filename[0]
        print(filename)
        print("connect ml here ")
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

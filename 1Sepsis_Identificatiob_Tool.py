# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Sepsis_Identificatiob_Tool.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4

width, height = letter

def draw(c , x , y , s):
    c.drawString(x*width , y*height , s)

def createPDF(name , age , sepsis , heartRate , bp , wbc):
    c = canvas.Canvas("Report.pdf")
    width, height = letter
    header = "-"*200
    c.drawString(0.0*width,0.95*height,header)
    c.drawString(0.1*width,0.9*height,"Name:")
    c.drawString(0.2*width,0.9*height, name)
    c.drawString(0.1*width,0.85*height,"Age:")
    c.drawString(0.2*width,0.85*height, age)
    c.drawString(0,0.8*height,header)
    c.drawString(0.1*width , 0.75*height , "Heart Rate")
    draw(c , 0.8 , 0.75 , heartRate)
    c.drawString(0.1*width , 0.7*height , "Blood Pressure")
    draw(c , 0.8 , 0.7, bp)
    c.drawString(0.1*width , 0.65*height , "WBC count")
    draw(c , 0.8 , 0.65 , wbc)
    #Cheange values
    c.drawString(0.1*width , 0.45*height , "Condition")
    draw(c , 0.12 , 0.4 , "Sepsis: ")
    draw(c , 0.8 , 0.45 , "Status")
    
    draw(c , 0.8 , 0.40 , sepsis)
    draw(c , 0.78 , 0.38 , "(>0.2 // Positive)")
    draw(c , 0.78 , 0.36 , "(<0.2 // Negative)")
    c.drawString(0.1*width , 0.3*height , "Remarks")
    c.drawString(0.1*width , 0.28*height , "The patient has sepsis. Suggested to admit in hospital as soon as possible.")
    c.showPage()
    c.save()
    # c.drawString(0.1*width,0.9*height,"Hello World")
    # c.drawString(0.1*width,0.89*height,"Hello World")
import json
import os
import math
import pandas as pd
import numpy as np
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import model_from_json

FileName = ""




#Loads Model
def loadModel():
    with open('model.json','r') as f:
        model_json = json.load(f)
    model = model_from_json(json.dumps(model_json))
    model.load_weights('model.h5')
    return model


#Return Array for input of LSTM
def clean(fileName):
    params=[]
    # y=[]
    data = pd.read_csv(fileName , sep='|')
    data.drop(['EtCO2','Fibrinogen', 'Unit1', 'Unit2', 'BaseExcess', 'DBP', 'Hct', 'Hgb', 'PTT', 'WBC', 'pH','HCO3','FiO2', 'PaCO2', 'Platelets', 'Magnesium',  'Phosphate',  'Potassium', 'Bilirubin_total',  'TroponinI','SaO2', 'AST','BUN', 'Alkalinephos', 'Bilirubin_direct','Glucose','Lactate', 'Calcium',  'Chloride', 'Creatinine' ],axis = 1,inplace = True)

    data.dropna(thresh=data.shape[1]*0.40,how='all',inplace = True)
    # La_1 = data['SepsisLabel'].sum()
    # if La_1:
    #     y.append(1)
    # else:
    #     y.append(0)
    data.drop(['SepsisLabel'],axis = 1,inplace = True)
    data = data.apply(lambda x: x.fillna(x.median()),axis=0)
    data = data.fillna(0)
    if len(data) < 40:
        Pad = pd.DataFrame({'HR':0.0 ,'O2Sat':0.0, 'Temp':0.0 , 'SBP':0.0, 'MAP':0.0, 'Resp':0.0, 'Age':0.0, 'Gender': 0 ,'HospAdmTime':0.0, 'ICULOS':0}, index =[item for item in range(0,40-len(data))])
        data = pd.concat([Pad, data]).reset_index(drop = True)
    elif len(data) >40:
        data = data[len(data)-40::1]
    data = data.values
    params.append(data)
    return params

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(688, 550)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(-1, -1, 281, 551))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(-40, -70, 351, 521))
        self.label.setStyleSheet("image:url(hospital.png)")
        self.label.setText("")
        self.label.setObjectName("label")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(280, 0, 411, 311))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 71, 41))
        self.label_2.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit.setGeometry(QtCore.QRect(132, 101, 181, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(140, 160, 91, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(142, 237, 91, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.frame_3 = QtWidgets.QFrame(Dialog)
        self.frame_3.setGeometry(QtCore.QRect(280, 310, 401, 241))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(130, 40, 161, 51))
        self.label_3.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_3.setGeometry(QtCore.QRect(110, 130, 171, 41))
        self.pushButton_3.setStyleSheet("font: 9pt \"MS Shell Dlg 2\";")
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sepsis_Identification_Tool"))
        self.label_2.setText(_translate("Dialog", "Name :"))
        self.pushButton.setText(_translate("Dialog", "Upload File"))
        self.pushButton.clicked.connect(self.pushButton_handler)
        self.pushButton_2.setText(_translate("Dialog", "Detect"))
        self.pushButton_2.clicked.connect(self.pushButton2_handler)
        self.label_3.setText(_translate("Dialog", "Sepsis : None"))
        self.pushButton_3.setText(_translate("Dialog", "Download Receipt"))
        self.pushButton_3.clicked.connect(self.pushButton3_handler)
    
    def pushButton_handler(self):
        print("hhdvcjhsvjvjsj")
        self.open_dialog_box()

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        FileName = filename[0]
        print(FileName)
        
    
    def pushButton2_handler(self):
        print("Has Been Detecting")
        Model = loadModel()
        self.label_3.setText("Sepsis : Positive")
        print("Model Loaded")
        X_test = clean(FileName)
        print("OK")
        print(X_test)

        X_test = np.reshape(X_test,(1,40,10))

        y_pred = Model.predict(X_test)
        #print(y_pred)
        
        if (y_pred <= 0.2):
            print("no Sepsis")
            self.label_3.setText("Sepsis : Negative")
        else:
            print("Sepsis Go to Hospital")
        self.label_3.setText("Sepsis : Positive")
    
    def pushButton3_handler(self):
        createPDF(name , age , detect , heartRate , bp , wbc)
        
        
import source_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'P2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
import csv

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def searchClicked(self):

        self.textBrowser.clear()
        self.recordBrowser.clear()
        queriedPerson = self.searchBox.toPlainText()
        workerID = 9999
        found = False

        print("searchClicked success")


        with open("exampleDB.csv", "r") as workerList:

            if queriedPerson.isnumeric() == True:
                for line in csv.reader(workerList):
                    if queriedPerson == line[0]:
                        workerID = line[0]
                        self.textBrowser.setText("Worker ID: " + line[0] +
                                                 "\nFirst Name: " + line[1] +
                                                 "\nLast Name: " + line[2] +
                                                 "\nAccess level: " + line[3])
                        found = True
                        self.populateRecords(workerID)

                        break

                    else:
                        found = False

            elif queriedPerson.isnumeric() == False:
                for line in csv.reader(workerList):
                    if queriedPerson == line[1]:
                        workerID = line[0]
                        self.textBrowser.setText("Worker ID: " + line[0] +
                                                 "\nFirst Name: " + line[1] +
                                                 "\nLast Name: " + line[2] +
                                                 "\nAccess level: " + line[3])
                        found = True
                        self.populateRecords(workerID)
                        break

                    elif queriedPerson == line[2]:
                        workerID = line[0]
                        self.textBrowser.setText("Worker ID: " + line[0] +
                                                 "\nFirst Name: " + line[1] +
                                                 "\nLast Name: " + line[2] +
                                                 "\nAccess level: " + line[3])
                        found = True
                        self.populateRecords(workerID)
                        break

                    else:
                        found = False

        if found != True:
            self.textBrowser.clear()
            self.recordBrowser.clear()





    def populateRecords(self, workerID):
        try:
            with open(str(workerID) + ".csv", "r") as workerRecords:
                for line in csv.reader(workerRecords):
                    self.recordBrowser.append(line[0] + "  " + line[1] + "  " + line[2])
        except:
            self.recordBrowser.setText("FAILED TO LOAD")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1149, 906)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(390, 10, 181, 51))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(self.searchClicked)
        self.searchBox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.searchBox.setGeometry(QtCore.QRect(10, 10, 371, 51))
        self.searchBox.setObjectName("searchBox")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 70, 561, 301))
        self.textBrowser.setObjectName("textBrowser")
        self.analysisOut = QtWidgets.QTextBrowser(self.centralwidget)
        self.analysisOut.setGeometry(QtCore.QRect(10, 380, 561, 481))
        self.analysisOut.setObjectName("analysisOut")
        self.recordBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.recordBrowser.setGeometry(QtCore.QRect(580, 10, 551, 851))
        self.recordBrowser.setObjectName("recordBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1149, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.searchButton.setText(_translate("MainWindow", "Search"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

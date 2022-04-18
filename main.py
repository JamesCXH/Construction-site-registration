import os
import csv

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):  # Main window where user queries

    def searchClicked(self):

        self.personInfo.clear()
        self.recordBrowser.clear()
        queriedPerson = self.searchBox.toPlainText()
        workerIDs = []
        workerIDs.clear()

        print("searchClicked success")

        with open("exampleDB.csv", "r") as workerList:

            if queriedPerson.isnumeric():
                for line in csv.reader(workerList):
                    if queriedPerson == line[0]:
                        workerIDs.append(line[0])
                        self.populatePersonDetails(line[0])

            elif not queriedPerson.isnumeric():

                for line in csv.reader(workerList):

                    if queriedPerson == line[1]:
                        workerIDs.append(line[0])

                    elif queriedPerson == line[2]:
                        workerIDs.append(line[0])

                    elif queriedPerson == str(line[1] + " " + line[2]):
                        workerIDs.append(line[0])

        if len(workerIDs) == 1:
            self.populatePersonDetails(workerIDs[0])
            self.populateRecords(workerIDs[0])

        else:
            pass  # Need to deal with multiple search results

    def populatePersonDetails(self, workerID):  # Adds person information to the browsing area for user to easily view and read
        try:
            with open("exampleDB.csv", "r") as workersDatabase:
                for line in csv.reader(workersDatabase):
                    if line[0] == workerID:
                        self.personInfo.setText("Worker ID: " + line[0] +
                                                "\nFirst Name: " + line[1] +
                                                "\nLast Name: " + line[2] +
                                                "\nAccess level: " + line[3])
        except:
            self.personInfo.setText("PERSON DOES NOT EXIST")

    def populateRecords(self, workerID):
        try:
            with open(str(workerID) + ".csv", "r") as workerRecords:
                for line in csv.reader(workerRecords):
                    self.recordBrowser.append(line[0] + "  " + line[1] + "  " + line[2])
        except:
            self.recordBrowser.setText("FAILED TO LOAD")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 1200)
        self.MainWindow = QtWidgets.QWidget(MainWindow)
        self.MainWindow.setObjectName("MainWindow")
        self.searchButton = QtWidgets.QPushButton(self.MainWindow)
        self.searchButton.setGeometry(QtCore.QRect(390, 10, 181, 51))
        self.searchButton.setObjectName("searchButton")
        self.searchBox = QtWidgets.QPlainTextEdit(self.MainWindow)
        self.searchBox.setGeometry(QtCore.QRect(20, 10, 361, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.searchBox.setFont(font)
        self.searchBox.setObjectName("searchBox")
        self.personInfo = QtWidgets.QTextBrowser(self.MainWindow)
        self.personInfo.setGeometry(QtCore.QRect(20, 100, 551, 381))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.personInfo.setFont(font)
        self.personInfo.setObjectName("personInfo")
        self.analysisOut = QtWidgets.QTextBrowser(self.MainWindow)
        self.analysisOut.setGeometry(QtCore.QRect(20, 520, 551, 631))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.analysisOut.setFont(font)
        self.analysisOut.setObjectName("analysisOut")
        self.recordBrowser = QtWidgets.QTextBrowser(self.MainWindow)
        self.recordBrowser.setGeometry(QtCore.QRect(590, 60, 581, 1091))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.recordBrowser.setFont(font)
        self.recordBrowser.setObjectName("recordBrowser")
        self.recordBrowserLabel = QtWidgets.QLabel(self.MainWindow)
        self.recordBrowserLabel.setGeometry(QtCore.QRect(590, 10, 500, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.recordBrowserLabel.setFont(font)
        self.recordBrowserLabel.setObjectName("recordBrowserLabel")
        self.personInfoLabel = QtWidgets.QLabel(self.MainWindow)
        self.personInfoLabel.setGeometry(QtCore.QRect(20, 60, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.personInfoLabel.setFont(font)
        self.personInfoLabel.setObjectName("personInfoLabel")
        self.analysisOutLabel = QtWidgets.QLabel(self.MainWindow)
        self.analysisOutLabel.setGeometry(QtCore.QRect(20, 480, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.analysisOutLabel.setFont(font)
        self.analysisOutLabel.setObjectName("analysisOutLabel")
        MainWindow.setCentralWidget(self.MainWindow)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.searchButton.clicked.connect(self.searchClicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.recordBrowserLabel.setText(_translate("MainWindow", "Personal check-in records"))
        self.personInfoLabel.setText(_translate("MainWindow", "Personal info"))
        self.analysisOutLabel.setText(_translate("MainWindow", "Attendance analysis"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

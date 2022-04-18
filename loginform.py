import sys
import csv
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)
from PyQt5 import QtCore, QtGui, QtWidgets




'''
Phase 1
class LoginWindow is a login window which the user is able to enter in a password, which upon authentication allows them to access the rest of the system.
'''
class LoginWindow(QWidget):  # Login window class, provides user interface for login window when user initially launches program
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Form")
        self.resize(1000, 240)
        grid = QGridLayout()

        password_label = QLabel("<font size='4'> Password </font>")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Please enter your password")
        grid.addWidget(password_label, 1, 0)
        grid.addWidget(self.password_input, 1, 1)

        login_button = QPushButton("Click to Login")
        login_button.clicked.connect(self.validate_password) # Runs function validate_password upon the clicking of the button
        grid.addWidget(login_button, 2, 0, 1, 2)
        grid.setRowMinimumHeight(2, 75)

        self.setLayout(grid)

    def validate_password(self):
        msg = QMessageBox()
        with open("password.txt") as passwordFile:
            password = str(passwordFile.read())[0:32767]
        if self.password_input.text() == str(password):
            self.setWindowTitle("")
            msg.setText("Success")
            msg.exec()
            self.selectionMenu = menuSelect()
            self.selectionMenu.show()
            self.hide()
        else:
            msg.setText("Incorrect Password")
            msg.exec_()

'''
Phase 1 + 2
class menuSelect is a simple selection menu which allows the user to launch either the query menu or the password reset form.
'''
class menuSelect(QWidget):  # Menu which provides user interface so that the user is able to decide what they want to do
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu")
        self.resize(600, 120)

        grid = QGridLayout()

        search_button = QPushButton("Search database")
        search_button.clicked.connect(self.launch_db)
        grid.addWidget(search_button, 1, 0, 1, 2)

        # add_face_button = QPushButton("Add face")
        # add_face_button.clicked.connect(self.add_person)
        # grid.addWidget(add_face_button, 2, 0, 1, 2)

        reset_password_button = QPushButton("Reset password")
        reset_password_button.clicked.connect(self.launch_reset_menu)
        grid.addWidget(reset_password_button, 3, 0, 1, 2)

        self.setLayout(grid)

    def launch_db(self):
        self.dbMenu = Ui_MainWindow()
        self.dbMenu.setupUi(MainWindow)
        MainWindow.show()
        self.hide()

    # def add_person(self):
    #     print("MMMM£")

    def launch_reset_menu(self):
        self.resetMenu = passwordReset()
        self.resetMenu.show()
        self.hide()


'''
Phase 2
class passwordReset is a form with validation that is used to reset the password that is used to login onto the system with.
'''

class passwordReset(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Reset Form")
        self.resize(1000, 240)

        grid = QGridLayout()

        password_label = QLabel("<font size='4'> Password </font>")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Please enter your password")
        grid.addWidget(password_label, 1, 0)
        grid.addWidget(self.password_input, 1, 1)

        password_label2 = QLabel("<font size='4'> Password </font>")
        self.password_input2 = QLineEdit()
        self.password_input2.setPlaceholderText("Please enter your password again")
        grid.addWidget(password_label2, 1, 0)
        grid.addWidget(self.password_input2, 1, 2)

        confirm_reset_button = QPushButton("Reset password")
        confirm_reset_button.clicked.connect(self.resetPassword)
        grid.addWidget(confirm_reset_button, 2, 0, 1, 2)
        grid.setRowMinimumHeight(2, 75)

        self.setLayout(grid)

    def resetPassword(self):
        msg = QMessageBox()
        specialSymbols = ["%", "$", "@", "#", "="]
        print(len(self.password_input.text()))
        with open("password.txt") as passwordFile:
            pass
        if not self.password_input.text() or not self.password_input2.text():  # Checks if either input space is blank
            msg.setText("Fields cannot be left blank")
            msg.exec()
        elif self.password_input.text() != self.password_input2.text():  # Checks if both input spaces match
            msg.setText("Passwords must match")
            msg.exec()
        elif len(self.password_input.text()) < 10:  # Checks if password is over 10 characters
            msg.setText("Length should be at least 10 characters")
            msg.exec()
        elif not any(char.isdigit() for char in self.password_input.text()):  # Checks that at least one of the characters in the password is a digit
            msg.setText("Password should contain numbers")
            msg.exec()
        elif not any(char.isupper() for char in self.password_input.text()):  # Checks that at least one of the characters in the password is an uppercase letter
            msg.setText("Password should contain uppercase letters")
            msg.exec()
        elif not any(char.islower() for char in self.password_input.text()):  # Checks that at least one of the characters in the password is a lowercase letter
            msg.setText("Password should lowercase letters")
            msg.exec()
        if not any(char in specialSymbols for char in self.password_input.text()):  # Checks that at least one of the characters in the password is a special symbol
            msg.setText("Password should contain special symbols (e.g., @, $, =, #, $)")
        else: # After ALL validation checks are passed, the password is able to be changed
            self.setWindowTitle("")
            msg.setText("Success")
            msg.exec()
            with open("password.txt", "w") as passwordFile:  # Opens password file
                passwordFile.write(self.password_input.text())  # Writes new password into file
            resetWindow.quit()


# Phase 3

class Ui_MainWindow(object):  # Main window where user queries

    def searchClicked(self):

        self.personInfo.clear()
        self.recordBrowser.clear()
        self.analysisOut.clear()
        queriedPerson = self.searchBox.toPlainText()
        workerIDs = []
        workerIDs.clear()

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



        if len(workerIDs) == 1:  # Populates boxes with information of queried person
            self.populatePersonDetails(workerIDs[0])
            self.populateRecords(workerIDs[0])

        else:
            self.personInfo.setText("PERSON DOES NOT EXIST")


            # Need to deal with multiple search results

    def populatePersonDetails(self, workerID):  # Populates boxes with information of queried person
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
                lates_amount = 0
                onTime_amount = 0
                for line in csv.reader(workerRecords):
                    if line[3] == "late":  # Counts how many lates on worker's record
                        lates_amount += 1
                    elif line[3] == "good":  # Counts how many on-times on worker's record
                        onTime_amount += 1
                    self.recordBrowser.append(line[0] + "  " + line[1] + "  " + line[2])

                self.analysisOut.setText("Lates: " + str(lates_amount) +
                                        "\nOn Time: " + str(onTime_amount) +
                                        "\nTotal: " + str(lates_amount + onTime_amount))
        except:
            self.recordBrowser.setText("FAILED TO LOAD")
            self.analysisOut.setText("FAILED TO LOAD")


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Database search menu")
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
    loginWindow = QApplication(sys.argv)
    loginForm = LoginWindow()
    resetWindow = QApplication(sys.argv)
    resetForm = passwordReset()
    mainMenu = QApplication(sys.argv)
    menuForm = menuSelect()
    dbWindow = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    loginForm.show()
    sys.exit(loginWindow.exec())
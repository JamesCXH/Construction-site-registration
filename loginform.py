import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)

class LoginWindow(QWidget):
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

		login_button = QPushButton("Login")
		login_button.clicked.connect(self.validate_password)
		grid.addWidget(login_button, 2, 0, 1, 2)
		grid.setRowMinimumHeight(2, 75)

		self.setLayout(grid)

	def validate_password(self):
		msg = QMessageBox()

		if self.password_input.text() == '000':
			self.setWindowTitle("")
			msg.setText("Success")
			msg.exec_()
			app.quit()
		else:
			msg.setText("Incorrect Password")
			msg.exec_()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	form = LoginWindow()
	form.show()
	sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)
import menu as menu

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
		with open("password.txt") as passwordFile:
			pass
		if not self.password_input.text() or not self.password_input2.text():
			msg.setText("Fields cannot be left blank")
			msg.exec()
		elif self.password_input.text() == self.password_input2.text():
			self.setWindowTitle("")
			msg.setText("Success")
			msg.exec()
			with open("password.txt", "w") as passwordFile:
				passwordFile.write(self.password_input.text())
			resetWindow.quit()
		else:
			msg.setText("Password's don't match")
			msg.exec()

if __name__ == "__main__":
	resetWindow = QApplication(sys.argv)
	form = passwordReset()
	form.show()
	sys.exit(resetWindow.exec_())
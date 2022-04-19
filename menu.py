import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QGridLayout)

class menuSelect(QWidget):
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
		print("YEET")

	# def add_person(self):
	# 	print("MMMM£")

	def launch_reset_menu(self):
		print("YYYWWW")

def execute():
	mainMenu = QApplication(sys.argv)
	form = menuSelect()
	form.show()
	sys.exit(mainMenu.exec())

# if __name__ == "__main__":
# 	mainMenu = QApplication(sys.argv)
# 	form = menuSelect()
# 	form.show()
# 	sys.exit(mainMenu.exec())
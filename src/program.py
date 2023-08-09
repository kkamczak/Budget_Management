'''
This module is responsible for displaying the program window and its content.
'''
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class MyGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # Load and init GUI-----------------
        uic.loadUi('src/gui/mygui.ui', self)


        # Configuring the appearance of the window--------------
        self.setWindowTitle("Budget Management App by kkamczak")
        self.setFixedSize(self.size())
        self.show()
        # Configure all buttons-----------------------------------

        # Define data-------------------------------------------





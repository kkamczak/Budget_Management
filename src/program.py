'''
This module is responsible for displaying the program window and its content.
'''
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from src.support import format_list_row, puts, message_box
from src.settings import COLUMNS_WIDTH, COLUMNS_NAMES, DATABASE_PATH, EXPENSES
from src.expenses import Add_Window, Edit_Expense
from src.database import create_tables, load_expenses


class MyGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # Load and init GUI-----------------
        uic.loadUi('src/gui/mygui.ui', self)

        # Configuring the appearance of the window--------------
        self.setWindowTitle("Budget Management App by kkamczak")
        self.setFixedSize(self.size())
        self.show()

        # Configuring buttons:
        self.button_add_expense.clicked.connect(self.open_add_expense)
        self.action_close.triggered.connect(exit)
        self.button_edit_expense.clicked.connect(self.edit_expense)

        # Create tables if not exists
        create_tables()

        # Configure list of expenses-----------------------------------
        self.configure_table_of_expenses()



    def configure_table_of_expenses(self) -> None:
        """
        This method configure table that shows all expenses.
        :return: None
        """
        expenses = load_expenses()
        self.table_of_expenses.setColumnCount(len(COLUMNS_NAMES))
        self.table_of_expenses.setHorizontalHeaderLabels(COLUMNS_NAMES)
        x_position = int(self.geometry().width() / 4)
        y_position = int(self.geometry().height() / 5)
        width = 0
        height = int(self.geometry().height() / 2)
        for column in range(self.table_of_expenses.columnCount()):
            self.table_of_expenses.setColumnWidth(column, COLUMNS_WIDTH[column])
            width += COLUMNS_WIDTH[column]
        self.table_of_expenses.setGeometry(x_position, y_position, width+35, height)
        self.table_of_expenses.setRowCount(len(expenses))
        for row, row_content in enumerate(expenses):
            for column, column_content in enumerate(row_content):
                self.table_of_expenses.setItem(row, column, QTableWidgetItem(str(column_content)))

    def open_add_expense(self) -> None:
        """
        This method creates and open 'Add Expense Window'...
        :return: None
        """
        self.add_window = Add_Window(self.configure_table_of_expenses)
        self.add_window.show()

    def edit_expense(self) -> None:
        row_data = []
        row = self.table_of_expenses.currentRow()
        if row == -1:
            message_box('Nie zaznaczono żadnego wiersza...')
        else:
            puts(f'Edytuje wydatek -> {row}')
            for index in range(0, self.table_of_expenses.columnCount()):
                row_data.append(self.table_of_expenses.item(row, index).text())
            self.open_edit_expense(row_data)
    def open_edit_expense(self, row_data) -> None:
        self.edit_expense_window = Edit_Expense(self.configure_table_of_expenses, row_data)
        self.edit_expense_window.show()




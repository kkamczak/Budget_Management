'''
This module is responsible for displaying the program window and its content.
'''
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from src.support import puts, message_box
from src.settings import EXPENSES_COLUMNS_WIDTH, EXPENSES_COLUMNS_NAMES, CATEGORIES_TABLE_COLUMN_NAMES
from src.expenses import Add_Window, Edit_Expense
from src.categories import Categories_Window
from src.database import create_tables, load_data, delete_record, sum_all_cells
from typing import Optional


class MyGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # Load and init GUI-----------------
        uic.loadUi('src/gui/mygui.ui', self)

        # Configuring the appearance of the window--------------
        self.setWindowTitle("Budget Management App by kkamczak")
        self.resize(1280, 720)
        self.setFixedSize(self.size())
        self.show()

        # Create tables if not exists
        create_tables()

        # Configure list of expenses and buttons-----------------------------------
        self.configure_table_of_expenses()
        self.configure_table_of_categories()
        self.configure_buttons()



    def configure_table_of_expenses(self, order: Optional[str] = 'Data') -> None:
        """
        This method configure table that shows all expenses.
        :return: None
        """
        expenses = load_data('expenses', order)
        self.table_of_expenses.setColumnCount(len(EXPENSES_COLUMNS_NAMES))
        self.table_of_expenses.setHorizontalHeaderLabels(EXPENSES_COLUMNS_NAMES)

        width = 0
        height = int(self.geometry().height() / 2)
        x_position = int(self.geometry().width() / 160)
        y_position = self.geometry().height() - int(self.geometry().height() / 10) - height
        for column in range(self.table_of_expenses.columnCount()):
            self.table_of_expenses.setColumnWidth(column, EXPENSES_COLUMNS_WIDTH[column])
            width += EXPENSES_COLUMNS_WIDTH[column]
        self.table_of_expenses.setGeometry(x_position, y_position, width+35, height)
        self.table_of_expenses.setRowCount(len(expenses))
        for row, row_content in enumerate(expenses):
            for column, column_content in enumerate(row_content):
                self.table_of_expenses.setItem(row, column, QTableWidgetItem(str(column_content)))

    def configure_table_of_categories(self, order: Optional[str] = 'Nazwa') -> None:
        """
        This method configure table that shows all category expenses.
        :return: None
        """
        respond = load_data('categories', order)
        categories = []
        for item in respond:
            categories.append([item[1], 0.0])
        self.table_of_category_expenses.setColumnCount(len(CATEGORIES_TABLE_COLUMN_NAMES))
        self.table_of_category_expenses.setHorizontalHeaderLabels(CATEGORIES_TABLE_COLUMN_NAMES)

        width = int(self.geometry().width() / 5)
        height = int(self.geometry().height() / 2)
        x_position = int(self.geometry().width() / 2) + 50
        y_position = self.geometry().height() - int(self.geometry().height() / 10) - height
        for column in range(self.table_of_category_expenses.columnCount()):
            self.table_of_category_expenses.setColumnWidth(column, int(width / 2))
        self.table_of_category_expenses.setGeometry(x_position, y_position, width+35, height)
        self.table_of_category_expenses.setRowCount(len(categories))
        for row, row_content in enumerate(categories):
            row_content[1] = float(sum_all_cells('expenses', 'Wartość', 'Kategoria', row_content[0]))
            for column, column_content in enumerate(row_content):
                self.table_of_category_expenses.setItem(row, column, QTableWidgetItem(str(column_content)))

    def configure_buttons(self):
        # Configuring buttons:
        self.action_close.triggered.connect(exit)
        self.action_categories.triggered.connect(self.open_categories)

        x_position = self.table_of_expenses.x() + self.table_of_expenses.width() + int(self.geometry().width() / 160)
        y_position = self.geometry().height() - self.table_of_expenses.height() - int(self.geometry().height() / 10)

        self.button_add_expense.clicked.connect(self.open_add_expense)
        self.button_add_expense.move(x_position, y_position)

        self.button_edit_expense.clicked.connect(self.edit_expense)
        self.button_edit_expense.move(x_position, y_position + 50)

        self.button_delete_expense.clicked.connect(self.remove_expense)
        self.button_delete_expense.move(x_position, y_position + 100)

        self.button_sort_expense.clicked.connect(self.sort_expenses)
        self.button_sort_expense.move(x_position, y_position + 150)

        self.label_date_start.move(x_position, y_position + 200)
        self.date_start.move(x_position, y_position + 225)
        self.label_date_end.move(x_position, y_position + 250)
        self.date_end.move(x_position, y_position + 275)
        self.update_date.move(x_position, y_position + 310)

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

    def remove_expense(self) -> None:
        row = self.table_of_expenses.currentRow()
        if row == -1:
            message_box('Nie zaznaczono żadnego wiersza...')
        else:
            puts(f'Usuwam wydatek -> {row}')
            expense_index = self.table_of_expenses.item(row, 0).text()
            delete_record('expenses', expense_index)
            message_box(f"Usunięto wydatek {self.table_of_expenses.item(row, 2).text()}")
            self.configure_table_of_expenses()

    def sort_expenses(self) -> None:
        column = self.table_of_expenses.currentColumn()
        if column == -1:
            message_box('Nie zaznaczono żadnej kolumny...')
        else:
            name = self.table_of_expenses.horizontalHeaderItem(column).text()
            puts(f"Sortuję według kolumny {name}")
            self.configure_table_of_expenses(order=name)

    def open_categories(self) -> None:
        self.categories_window = Categories_Window(self.configure_table_of_expenses)
        self.categories_window.show()




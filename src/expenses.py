"""
This module contains classes responsible for operations on expenses
"""
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from PyQt5.QtCore import QDate
from src.support import puts
from src.database import insert_data, update_row, load_data
from src.settings import  EXPENSES_COLUMNS_NAMES
from typing import Callable


class Add_Window(QWidget):
    """
    This class is used to create an expense adding window
    """
    def __init__(self, configure: Callable) -> None:
        """
        :param configure: Callable
        """
        super().__init__()
        uic.loadUi('src/gui/add_window.ui', self) # Load GUI from designer.exe file
        self.setWindowTitle("Add expense")
        self.setFixedSize(self.size())
        self.show()

        self.configure_main_window = configure

        # Configure window
        self.button_cancel.clicked.connect(self.close)
        self.button_add.clicked.connect(self.add)

        self.configure_window()

    def configure_window(self) -> None:
        """
        This method is used to configure elements on window
        :return:
        """
        # Data element:
        self.date_edit.setDate(QDate.currentDate())

        # ComboBox category element:
        self.category_edit.clear()
        categories_names = []
        respond = load_data('categories', 'ID')
        for item in respond:
            categories_names.append(item[1])
        self.category_edit.addItems(categories_names)

        # Value of expense element:
        self.value_edit.setMaximum(1000000.00)
        self.value_edit.setMinimum(0.00)
    def add(self) -> None:
        """
        This method is used to add a new expense
        :return: None
        """
        date = self.date_edit.date().toString("yyyy-MM-dd")
        name = self.name_edit.text()
        category = self.category_edit.currentText()
        value = round(float(self.value_edit.value()), 2)

        insert_data('expenses', [date, name, category, value])
        self.configure_main_window()
        self.close()

class Edit_Expense(Add_Window):
    """
    This class is used to create an expense editing window
    """
    def __init__(self, configure: Callable, row_data: list) -> None:
        """
        :param configure: Callable
        :param row_data: list
        """
        super().__init__(configure)
        self.index = row_data[0]

        self.configure_interface(row_data)

    def configure_interface(self, row_data) -> None:
        # - Configure names:
        self.setWindowTitle("Edit expense")
        self.setFixedSize(self.size())
        self.button_add.setText('Edytuj')

        # - Configure edit labels:
        date_format = "yyyy-MM-dd"
        date = QDate.fromString(row_data[1], date_format)
        self.date_edit.setDate(date)

        self.name_edit.setText(row_data[2])

        self.category_edit.setCurrentText(row_data[3])

        self.value_edit.setValue(round(float(row_data[4]), 2))


    def add(self) -> None:
        """
        This method is used to edit expense
        :return: None
        """
        date = self.date_edit.date().toString("yyyy-MM-dd")
        name = self.name_edit.text()
        category = self.category_edit.currentText()
        value = str(self.value_edit.value())

        puts(f'Index = {self.index}')
        update_row('expenses', EXPENSES_COLUMNS_NAMES, [self.index, date, name, category, value])

        self.configure_main_window()
        self.close()
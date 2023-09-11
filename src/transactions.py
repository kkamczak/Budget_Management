"""
This module contains classes responsible for operations on expenses
"""
from typing import Callable, Optional
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from PyQt5.QtCore import QDate
from src.support import puts
from src.database import insert_data, update_row, load_data
from src.settings import  TRANS_COLS_NAMES, TRANSACTIONS, CATS_DB_COLS_NAMES, VALUE_MAX, VALUE_MIN

class AddWindow(QWidget):
    """
    This class is used to create an expense adding window
    """
    def __init__(self, configure: Callable) -> None:
        """
        Initialize an expense adding window.

        Args:
            configure (Callable): A callable function used to configure the main window.
        """
        super().__init__()
        uic.loadUi('src/gui/add_window.ui', self) # Load GUI from designer.exe file
        self.setWindowTitle("add Transaction")
        self.setFixedSize(self.size())
        self.show()

        self.configure_main_window = configure

        # Configure window
        self.button_cancel.clicked.connect(self.close)
        self.button_add.clicked.connect(self.add)
        self.type_choose.addItems(TRANSACTIONS)
        self.type_choose.currentTextChanged.connect(
            lambda: self.configure_window(kind=self.type_choose.currentText())
        )

        self.configure_window()

    def configure_window(self, kind: Optional[str] = TRANSACTIONS[0]) -> None:
        """
        Configure elements on the expense adding window.

        Args:
            kind (Optional[str]): The type of transaction. Defaults to TRANSACTIONS[0].
        """

        self.type_choose.setCurrentText(kind) # Choose type of transaction
        self.date_edit.setDate(QDate.currentDate()) # Data element
        self.category_edit.clear() # ComboBox category element:

        categories_names = []
        if self.type_choose.currentText() == TRANSACTIONS[0]:
            respond = load_data('categories', 'ID', kind=[CATS_DB_COLS_NAMES[3], TRANSACTIONS[0]])
        else:
            respond = load_data('categories', 'ID', kind=[CATS_DB_COLS_NAMES[3], TRANSACTIONS[1]])
        for item in respond:
            categories_names.append(item[1])
        self.category_edit.addItems(categories_names)

        # Value of expense element:
        self.value_edit.setMaximum(VALUE_MAX)
        self.value_edit.setMinimum(VALUE_MIN)
    def add(self) -> None:
        """
        Add a new expense to the database.
        """
        kind = self.type_choose.currentText()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        name = self.name_edit.text()
        category = self.category_edit.currentText()
        value = round(float(self.value_edit.value()), 2)

        if kind == TRANSACTIONS[0]:
            table = 'expenses'
        else:
            table = 'revenues'

        insert_data(table, [date, name, category, value])
        self.configure_main_window()
        self.close()

class EditTransaction(AddWindow):
    """
    This class is used to create a transaction editing window
    """
    def __init__(self, configure: Callable, row_data: list) -> None:
        """
        Initialize an expense editing window.

        Args:
            configure (Callable): A callable function used to configure the main window.
            row_data (list): The data of the selected transaction row.
        """
        super().__init__(configure)
        self.index = row_data[1]

        self.configure_interface(row_data)

    def configure_interface(self, row_data: list) -> None:
        """
        Configure the interface of the transaction editing window.

        Args:
            row_data (list): The data of the selected transaction row.
        """

        # - Configure names:
        self.setWindowTitle("Edit transaction")
        self.setFixedSize(self.size())
        self.button_add.setText('Edytuj')

        # - Configure edit labels:
        self.type_choose.setCurrentText(row_data[0])

        date_format = "yyyy-MM-dd"
        date = QDate.fromString(row_data[2], date_format)
        self.date_edit.setDate(date)

        self.name_edit.setText(row_data[3])

        self.category_edit.setCurrentText(row_data[4])

        self.value_edit.setValue(round(float(row_data[5]), 2))

    def add(self) -> None:
        """
        Edit an existing transaction in the database.
        """
        kind = self.type_choose.currentText()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        name = self.name_edit.text()
        category = self.category_edit.currentText()
        value = str(self.value_edit.value())

        puts(f'Index = {self.index}')
        if kind == TRANSACTIONS[0]:
            table = 'expenses'
        else:
            table = 'revenues'
        update_row(table, TRANS_COLS_NAMES, [self.index, date, name, category, value])

        self.configure_main_window()
        self.close()

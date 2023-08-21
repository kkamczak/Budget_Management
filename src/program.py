'''
This module is responsible for displaying the program window and its content.
'''
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from src.support import puts, message_box, get_first_last_day
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, DOWNSPACE, LEFTSPACE, BUTTONSPACE
from src.expenses import Add_Window, Edit_Expense
from src.categories import Categories_Window
from src.database import create_tables, delete_record
from src.widgets import configure_table_of_expenses, configure_table_of_categories, configure_table_of_revenues


class MyGUI(QMainWindow):
    """
    This class is used to create main window object
    """
    def __init__(self) -> None:
        """
        :return: None
        """
        super().__init__()
        uic.loadUi('src/gui/mygui.ui', self) # Load GUI from designer.exe file

        # Configuring the appearance of the window--------------
        self.setWindowTitle("Budget Management App by kkamczak")
        self.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setFixedSize(self.size())
        self.show()

        # Create tables if not exists
        create_tables()

        # Configure list of expenses and buttons-----------------------------------

        self.date_start.setDate(get_first_last_day()[0])
        self.date_end.setDate(get_first_last_day()[1])
        self.date_between = [self.date_start.date().toString("yyyy-MM-dd"), self.date_end.date().toString("yyyy-MM-dd")]
        self.configure_main_window()
        self.configure_buttons()



    def configure_main_window(self) -> None:

        configure_table_of_expenses(self.table_of_expenses, date=self.date_between)
        configure_table_of_categories(self.table_of_category_expenses, date=self.date_between)
        configure_table_of_revenues(self.table_of_revenues)
        

    def configure_buttons(self):
        # Configuring buttons:
        self.action_close.triggered.connect(exit)
        self.action_categories.triggered.connect(self.open_categories)

        self.label_revenues.move(int(SCREEN_WIDTH / 8), int(SCREEN_HEIGHT / 150))
        self.label_expenses.move(int(SCREEN_WIDTH / 8), int(SCREEN_HEIGHT / 2.55))

        x_position = self.table_of_expenses.x() + self.table_of_expenses.width() + LEFTSPACE
        y_position = self.geometry().height() - self.table_of_expenses.height() - DOWNSPACE

        self.button_add_transaction.clicked.connect(self.open_add_expense)
        self.button_add_transaction.move(x_position, y_position)

        self.button_edit_transaction.clicked.connect(self.edit_expense)
        self.button_edit_transaction.move(x_position, y_position + 1*BUTTONSPACE)

        self.button_delete_transaction.clicked.connect(self.remove_expense)
        self.button_delete_transaction.move(x_position, y_position + 2*BUTTONSPACE)

        self.button_sort_table.clicked.connect(self.sort_expenses)
        self.button_sort_table.move(x_position, y_position + 3*BUTTONSPACE)

        self.label_date_start.move(x_position, y_position + 4*BUTTONSPACE)
        self.date_start.move(x_position, y_position + int(4.5*BUTTONSPACE))
        self.date_start.setDate(get_first_last_day()[0])

        self.label_date_end.move(x_position, y_position + 5*BUTTONSPACE)
        self.date_end.move(x_position, y_position + int(5.5*BUTTONSPACE))
        self.date_end.setDate(get_first_last_day()[1])

        self.update_date.move(x_position, y_position + 6*BUTTONSPACE)
        self.update_date.clicked.connect(self.update_buttons_date)
        self.reset_date.move(x_position + 75, y_position + 6*BUTTONSPACE)
        self.reset_date.clicked.connect(lambda: self.reset_buttons_date(self.date_start, self.date_end))

    def open_add_expense(self) -> None:
        """
        This method creates and open 'Add Expense Window'...
        :return: None
        """
        self.add_window = Add_Window(self.configure_main_window)
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
        self.edit_expense_window = Edit_Expense(self.configure_main_window, row_data)
        self.edit_expense_window.show()

    def remove_expense(self) -> None:
        row = self.table_of_expenses.currentRow()
        if row == -1:
            message_box('No row selected...')
        else:
            expense_index = self.table_of_expenses.item(row, 0).text()
            delete_record('expenses', expense_index)
            message_box(f"Removed expense: {self.table_of_expenses.item(row, 2).text()}")
            self.configure_main_window()

    def sort_expenses(self) -> None:
        column = self.table_of_expenses.currentColumn()
        if column == -1:
            message_box('No column selected...')
        else:
            name = self.table_of_expenses.horizontalHeaderItem(column).text()
            reverse = False
            if name == self.table_of_expenses.sort_name and not self.table_of_expenses.reversed:
                reverse = True
            puts(f"Sorting by column: {name}, reverse -> {reverse}")
            configure_table_of_expenses(self.table_of_expenses, order=name, reverse=reverse)

    def open_categories(self) -> None:
        self.categories_window = Categories_Window(self.configure_main_window)
        self.categories_window.show()

    def reset_buttons_date(self, first, last):
        first.setDate(get_first_last_day()[0])
        last.setDate(get_first_last_day()[1])
        self.date_between = [self.date_start.date().toString("yyyy-MM-dd"), self.date_end.date().toString("yyyy-MM-dd")]
        self.configure_main_window()

    def update_buttons_date(self):
        self.date_between = [self.date_start.date().toString("yyyy-MM-dd"), self.date_end.date().toString("yyyy-MM-dd")]
        self.configure_main_window()
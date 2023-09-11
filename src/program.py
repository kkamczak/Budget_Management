'''
This module is responsible for displaying the program window and its content.
'''
from typing import Optional
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene
from PyQt5.QtCore import Qt, QFile, QTextStream, QRectF
from src.support import puts, message_box, get_first_last_day, get_current_month
from src.plot import Canvas, load_plot_content
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, DOWNSPACE, LEFTSPACE, \
    BUTTONSPACE, TRANSACTIONS, MONTHS, TABLES_SIZE, LABELS
from src.transactions import AddWindow, EditTransaction
from src.categories import CategoriesWindow
from src.database import create_tables, delete_record
from src.widgets import configure_table_of_expenses, configure_table_of_categories, \
    configure_table_of_revenues

class MyGUI(QMainWindow):
    """
    This class is used to create main window object
    """
    def __init__(self) -> None:
        """
        Initialize the main window.

        Returns:
            None
        """
        super().__init__()
        uic.loadUi('src/gui/mygui.ui', self) # Load GUI from designer.exe file

        # Configuring the appearance of the window--------------
        style_file = QFile("src/style.css")
        style_file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(style_file)
        self.setStyleSheet(stream.readAll())

        self.setWindowTitle("Budget Management App by kkamczak")
        self.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setFixedSize(self.size())
        self.show()

        # Create tables if not exists
        create_tables()

        # Configure list of transaction and buttons-----------------------------------
        self.date_start.setDate(get_first_last_day()[0])
        self.date_end.setDate(get_first_last_day()[1])
        self.date_between = [
            self.date_start.date().toString("yyyy-MM-dd"),
            self.date_end.date().toString("yyyy-MM-dd")
        ]
        self.selected_cell = None

        self.configure_plot_view()
        self.configure_main_window()
        self.configure_buttons()

        # Sub-windows:
        self.add_window = None
        self.edit_transaction_window = None
        self.categories_window = None

        self.reset_buttons_date(
            self.date_start, self.date_end, month=MONTHS[self.month_choose.currentText()]
        )

    def configure_main_window(self) -> None:
        """
        Configure the main window.

        Returns:
            None
        """
        configure_table_of_expenses(self.table_of_expenses, date=self.date_between)
        configure_table_of_categories(self.table_of_category_expenses, date=self.date_between)
        configure_table_of_revenues(self.table_of_revenues)

        self.selected_cell = None

        data = load_plot_content(self.table_of_category_expenses)
        if len(data[0]) > 0:
            self.canvas.plot(data[0], data[1])

    def configure_buttons(self):
        """
        Configure buttons in the main window.

        Returns:
            None
        """

        # Configuring buttons:
        self.action_close.triggered.connect(exit)
        self.action_categories.triggered.connect(self.open_categories)

        self.label_revenues.setGeometry(*LABELS['Revenues'])
        self.label_expenses.setGeometry(*LABELS['Expenses'])

        x_position = self.table_of_expenses.x() + self.table_of_expenses.width() + LEFTSPACE
        y_position = self.geometry().height() - self.table_of_expenses.height() - DOWNSPACE

        self.button_add_transaction.clicked.connect(self.open_add_transaction)
        self.button_add_transaction.move(x_position, y_position)

        self.button_edit_transaction.clicked.connect(self.edit_transaction)
        self.button_edit_transaction.move(x_position, y_position + 1*BUTTONSPACE)

        self.button_delete_transaction.clicked.connect(self.remove_transaction)
        self.button_delete_transaction.move(x_position, y_position + 2*BUTTONSPACE)

        self.button_sort_table.clicked.connect(self.sort_table)
        self.button_sort_table.move(x_position, y_position + 3*BUTTONSPACE)

        self.label_date_start.move(x_position, y_position + 4*BUTTONSPACE)
        self.date_start.move(x_position, y_position + int(4.5*BUTTONSPACE))
        self.date_start.setDate(get_first_last_day()[0])

        self.label_date_end.move(x_position, y_position + 5*BUTTONSPACE)
        self.date_end.move(x_position, y_position + int(5.5*BUTTONSPACE))
        self.date_end.setDate(get_first_last_day()[1])

        self.update_date.move(x_position, y_position + 6*BUTTONSPACE)
        self.update_date.clicked.connect(self.update_buttons_date)
        self.reset_date.move(x_position + 85, y_position + 6*BUTTONSPACE)
        self.reset_date.clicked.connect(
            lambda: self.reset_buttons_date(self.date_start, self.date_end)
        )

        self.table_of_expenses.selectionModel().selectionChanged.connect(
            lambda sel, desel: self.update_selected_cell('expenses', sel))
        self.table_of_revenues.selectionModel().selectionChanged.connect(
            lambda sel, desel: self.update_selected_cell('revenues', sel))
        # Problem to solve: nazwy kolumn w tabeli róznią od nazw w bazie danych
        #self.table_of_category_expenses.selectionModel().selectionChanged.connect(
        #    lambda sel, desel: self.update_selected_cell('categories', sel))

        for month, _ in MONTHS.items():
            self.month_choose.addItem(month)
        self.month_choose.setCurrentText(get_current_month())
        self.month_choose.currentTextChanged.connect(
            lambda: self.reset_buttons_date(
                self.date_start, self.date_end, month=MONTHS[self.month_choose.currentText()]
            )
        )
    def configure_plot_view(self) -> None:
        """
        Configure the plot view.

        Returns:
            None
        """

        self.plot_scene = QGraphicsScene(self)
        self.plot_view.setScene(self.plot_scene)

        self.canvas = Canvas()
        self.canvas.setFixedSize(TABLES_SIZE['Plot'][0]-30, TABLES_SIZE['Plot'][1]-30)
        self.plot_scene.addWidget(self.canvas)

        # self.canvas.setPos(SCREEN_WIDTH / 2, 100)
        self.plot_view.setGeometry(int(SCREEN_WIDTH / 2) + LEFTSPACE,
                                   DOWNSPACE,
                                   TABLES_SIZE['Plot'][0],
                                   TABLES_SIZE['Plot'][1]
                                   )
        new_scene_rect = QRectF(0, 0, TABLES_SIZE['Plot'][0],
                                   TABLES_SIZE['Plot'][1]
                                )
        self.plot_scene.setSceneRect(new_scene_rect)
        self.plot_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.plot_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def open_add_transaction(self) -> None:
        """
        Open the 'Add Expense Window'.

        Returns:
            None
        """
        self.add_window = AddWindow(self.configure_main_window)
        self.add_window.show()
    def edit_transaction(self) -> None:
        """
        Edit a transaction.

        Returns:
            None
        """
        row_data = []
        if self.selected_cell is None:
            message_box('No row selected...')
        else:
            row = self.selected_cell[1]
            puts(f'Edytuje wydatek -> {self.selected_cell}')
            if self.selected_cell[0] == 'expenses':
                for index in range(0, self.table_of_expenses.columnCount()):
                    row_data.append(self.table_of_expenses.item(row, index).text())
                row_data.insert(0, TRANSACTIONS[0])
                self.open_edit_transaction(row_data)
            elif self.selected_cell[0] == 'revenues':
                for index in range(0, self.table_of_revenues.columnCount()):
                    row_data.append(self.table_of_revenues.item(row, index).text())
                row_data.insert(0, TRANSACTIONS[1])
                self.open_edit_transaction(row_data)
            else:
                message_box("Wystąpił problem z edycją transakcji...")
    def open_edit_transaction(self, row_data) -> None:
        """
        Open the 'Edit Transaction' window.

        Args:
            row_data (list): Data of the row to edit.

        Returns:
            None
        """
        self.edit_transaction_window = EditTransaction(self.configure_main_window, row_data)
        self.edit_transaction_window.show()
    def remove_transaction(self) -> None:
        """
        Remove a transaction.

        Returns:
            None
        """
        row = self.table_of_expenses.currentRow()
        if row == -1:
            message_box('No row selected...')
        else:
            expense_index = self.table_of_expenses.item(row, 0).text()
            delete_record('expenses', expense_index)
            message_box(f"Removed expense: {self.table_of_expenses.item(row, 2).text()}")
            self.configure_main_window()
    def sort_table(self) -> None:
        """
        Sort the table.

        Returns:
            None
        """
        if self.selected_cell is None:
            message_box('No row selected...')
        else:
            if self.selected_cell[0] == 'expenses':
                table = self.table_of_expenses
            elif self.selected_cell[0] == 'revenues':
                table = self.table_of_revenues
            elif self.selected_cell[0] == 'categories':
                table = self.table_of_category_expenses
            else:
                table = None
            if table is not None:
                name = table.horizontalHeaderItem(self.selected_cell[2]).text()
                reverse = False
                if name == table.sort_name and not table.reversed:
                    reverse = True
                puts(f"Sorting by column: {name}, reverse -> {reverse}")
                if self.selected_cell[0] == 'expenses':
                    configure_table_of_expenses(
                        self.table_of_expenses, order=name, reverse=reverse
                    )
                elif self.selected_cell[0] == 'revenues':
                    configure_table_of_revenues(
                        self.table_of_revenues, order=name, reverse=reverse
                    )
                elif self.selected_cell[0] == 'categories':
                    configure_table_of_categories(
                        self.table_of_category_expenses, order=name, reverse=reverse
                    )
    def open_categories(self) -> None:
        """
        Open the 'Categories' window.

        Returns:
            None
        """
        self.categories_window = CategoriesWindow(self.configure_main_window)
        self.categories_window.show()
    def reset_buttons_date(self, first, last, month: Optional[int] = None):
        """
        Reset the date for buttons.

        Args:
            first: The start date.
            last: The end date.
            month: The month to reset the buttons to. Defaults to None.

        Returns:
            None
        """
        first.setDate(get_first_last_day(month=month)[0])
        last.setDate(get_first_last_day(month=month)[1])
        self.date_between = [
            self.date_start.date().toString("yyyy-MM-dd"),
            self.date_end.date().toString("yyyy-MM-dd")
        ]
        self.configure_main_window()
    def update_buttons_date(self):
        """
        Update the date for buttons.

        Returns:
            None
        """
        self.date_between = [
            self.date_start.date().toString("yyyy-MM-dd"),
            self.date_end.date().toString("yyyy-MM-dd")
        ]
        self.configure_main_window()
    def update_selected_cell(self, table, selected):
        """
        Update the selected cell in the table.

        Args:
            table: The table type.
            selected: The selected item.

        Returns:
            None
        """
        row = [ix.row() for ix in selected.indexes()]
        column = [iy.column() for iy in selected.indexes()]
        try:
            self.selected_cell = [table, row[0], column[0]]
        except IndexError:
            puts('update_selected_cell warning...')
            self.selected_cell = None
        puts(f"Selected: {self.selected_cell}")

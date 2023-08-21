from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDoubleSpinBox
from typing import Optional
from src.settings import EXPENSES_COLUMNS_WIDTH, EXPENSES_COLUMNS_NAMES, TABLES_SIZE, LEFTSPACE, DOWNSPACE, \
    SCREEN_WIDTH, SCREEN_HEIGHT, ID_WIDTH, CATEGORIES_COLUMNS_WIDTH, CATEGORIES_COLUMNS_NAMES, \
    CATEGORIES_TABLE_COLUMN_NAMES, VALUE_MAX, VALUE_MIN
from src.database import load_data, get_id_by_name, sum_all_cells, update_row
from functools import partial


def configure_table_of_expenses(table: QTableWidget, order: Optional[str] = EXPENSES_COLUMNS_NAMES[1],
                                reverse: Optional[bool] = False, date: Optional[list[str]] = None) -> None:
    """
    This method configure table that shows all expenses.
    :param order: str
    :param reverse: bool
    :return: None
    """
    expenses = load_data('expenses', order, reverse, date)
    table.setColumnCount(len(EXPENSES_COLUMNS_NAMES))
    table.setHorizontalHeaderLabels(EXPENSES_COLUMNS_NAMES)

    table.sort_name = order
    table.reversed = reverse
    width, height = TABLES_SIZE['Expenses']
    x_position = LEFTSPACE
    y_position = SCREEN_HEIGHT - DOWNSPACE - height
    for column in range(table.columnCount()):
        table.setColumnWidth(column, EXPENSES_COLUMNS_WIDTH[column])
    table.setGeometry(x_position, y_position, width + ID_WIDTH, height)
    table.verticalHeader().setFixedWidth(ID_WIDTH)
    table.setRowCount(len(expenses))
    for row, row_content in enumerate(expenses):
        for column, column_content in enumerate(row_content):
            table.setItem(row, column, QTableWidgetItem(str(column_content)))


def configure_table_of_categories(table: QTableWidget, order: Optional[str] = CATEGORIES_COLUMNS_NAMES[1], date: Optional[list[str]] = None) -> None:
    """
    This method configure table that shows all category expenses.
    :return: None
    """
    respond = load_data('categories', column_order=order)
    categories = []

    for item in respond:
        categories.append([item[1], item[2], 0.0])
    table.setColumnCount(len(CATEGORIES_TABLE_COLUMN_NAMES))
    table.setHorizontalHeaderLabels(CATEGORIES_TABLE_COLUMN_NAMES)

    width, height = TABLES_SIZE['Categories']
    x_position = int(SCREEN_WIDTH / 2) + LEFTSPACE
    y_position = SCREEN_HEIGHT - DOWNSPACE - height
    for column in range(table.columnCount()):
        table.setColumnWidth(column, CATEGORIES_COLUMNS_WIDTH[column])
    table.setGeometry(x_position, y_position, width + ID_WIDTH, height)
    table.verticalHeader().setFixedWidth(ID_WIDTH)
    table.setRowCount(len(categories))
    for row, row_content in enumerate(categories):
        row_content[2] = float(
            sum_all_cells('expenses', EXPENSES_COLUMNS_NAMES[4], EXPENSES_COLUMNS_NAMES[3], row_content[0], date))
        for column, column_content in enumerate(row_content):
            if column == 1:
                double_edit = QDoubleSpinBox()
                double_edit.setMaximum(VALUE_MAX)
                double_edit.setMinimum(VALUE_MIN)
                double_edit.setValue(round(column_content, 2))
                double_edit.valueChanged.connect(partial(update_budget,
                                                         get_id_by_name('categories', CATEGORIES_COLUMNS_NAMES[1],
                                                                        row_content[0])))
                table.setCellWidget(row, column, double_edit)
            else:
                table.setItem(row, column, QTableWidgetItem(str(column_content)))

def configure_table_of_revenues(table: QTableWidget, order: Optional[str] = EXPENSES_COLUMNS_NAMES[1],
                                reverse: Optional[bool] = False) -> None:
    """
    This method configure table that shows all revenues.
    :param order: str
    :param reverse: bool
    :return: None
    """
    revenues = load_data('revenues', order, reverse)
    table.setColumnCount(len(EXPENSES_COLUMNS_NAMES))
    table.setHorizontalHeaderLabels(EXPENSES_COLUMNS_NAMES)

    table.sort_name = order
    table.reversed = reverse
    width, height = TABLES_SIZE['Revenues']
    x_position = LEFTSPACE
    y_position = DOWNSPACE
    for column in range(table.columnCount()):
        table.setColumnWidth(column, EXPENSES_COLUMNS_WIDTH[column])
    table.setGeometry(x_position, y_position, width + ID_WIDTH, height)
    table.verticalHeader().setFixedWidth(ID_WIDTH)
    table.setRowCount(len(revenues))
    for row, row_content in enumerate(revenues):
        for column, column_content in enumerate(row_content):
            table.setItem(row, column, QTableWidgetItem(str(column_content)))

def update_budget(index: int, data: float) -> None:
    update_row('categories', [CATEGORIES_COLUMNS_NAMES[0], CATEGORIES_COLUMNS_NAMES[2]], [index, data])

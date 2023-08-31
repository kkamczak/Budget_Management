from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDoubleSpinBox
from typing import Optional
from src.settings import TRANS_COLS_WIDTH, TRANS_COLS_NAMES, TABLES_SIZE, LEFTSPACE, DOWNSPACE, \
    SCREEN_WIDTH, SCREEN_HEIGHT, ID_WIDTH, CAT_TABLE_COLS_WIDTH, CATS_DB_COLS_NAMES, \
    CATS_TABLE_COLS_NAMES, VALUE_MAX, VALUE_MIN, TRANSACTIONS
from src.database import load_data, get_id_by_name, sum_all_cells, update_row
from functools import partial


def configure_table_of_expenses(table: QTableWidget, order: Optional[str] = TRANS_COLS_NAMES[1],
                                reverse: Optional[bool] = False, date: Optional[list[str]] = None) -> None:
    """
    This method configure table that shows all expenses.
    :param order: str
    :param reverse: bool
    :return: None
    """
    expenses = load_data('expenses', column_order=order, reverse=reverse, date=date)
    table.setColumnCount(len(TRANS_COLS_NAMES))
    table.setHorizontalHeaderLabels(TRANS_COLS_NAMES)

    table.sort_name = order
    table.reversed = reverse
    width, height = TABLES_SIZE['Expenses']
    x_position = LEFTSPACE
    y_position = SCREEN_HEIGHT - DOWNSPACE - height
    for column in range(table.columnCount()):
        table.setColumnWidth(column, TRANS_COLS_WIDTH[column])
    table.setGeometry(x_position, y_position, width + ID_WIDTH, height)
    table.verticalHeader().setFixedWidth(ID_WIDTH)
    table.setRowCount(len(expenses))
    for row, row_content in enumerate(expenses):
        for column, column_content in enumerate(row_content):
            table.setItem(row, column, QTableWidgetItem(str(column_content)))


def configure_table_of_categories(table: QTableWidget, order: Optional[str] = CATS_DB_COLS_NAMES[1], date: Optional[list[str]] = None,  reverse: Optional[bool] = False) -> None:
    """
    This method configure table that shows all category expenses.
    :return: None
    """
    respond = load_data('categories', order, kind=[CATS_DB_COLS_NAMES[3], TRANSACTIONS[0]])
    categories = []

    for item in respond:
        categories.append([item[1], item[2], 0.0, 0.0])
    table.setColumnCount(len(CATS_TABLE_COLS_NAMES))
    table.setHorizontalHeaderLabels(CATS_TABLE_COLS_NAMES)

    table.sort_name = order
    table.reversed = reverse
    width, height = TABLES_SIZE['Categories']
    x_position = int(SCREEN_WIDTH / 2) + LEFTSPACE
    y_position = SCREEN_HEIGHT - DOWNSPACE - height
    for column in range(table.columnCount()):
        table.setColumnWidth(column, CAT_TABLE_COLS_WIDTH[column])
    table.setGeometry(x_position, y_position, width + ID_WIDTH, height)
    table.verticalHeader().setFixedWidth(ID_WIDTH)
    table.setRowCount(len(categories))
    for row, row_content in enumerate(categories):
        row_content[2] = float(
            sum_all_cells('expenses', TRANS_COLS_NAMES[4], TRANS_COLS_NAMES[3], row_content[0], date=date))
        if row_content[1] != 0.0:
            row_content[3] = f"{round(row_content[2] / row_content[1] * 100, 2)}%"
        else:
            row_content[3] = f"N/D"
        for column, column_content in enumerate(row_content):
            if column == 1:
                double_edit = QDoubleSpinBox()
                double_edit.setMaximum(VALUE_MAX)
                double_edit.setMinimum(VALUE_MIN)
                double_edit.setValue(round(column_content, 2))
                double_edit.valueChanged.connect(partial(update_budget,
                                                         get_id_by_name('categories', CATS_DB_COLS_NAMES[1],
                                                                        row_content[0])))
                table.setCellWidget(row, column, double_edit)
            else:
                table.setItem(row, column, QTableWidgetItem(str(column_content)))

def configure_table_of_revenues(table: QTableWidget, order: Optional[str] = TRANS_COLS_NAMES[1],
                                reverse: Optional[bool] = False) -> None:
    """
    This method configure table that shows all revenues.
    :param order: str
    :param reverse: bool
    :return: None
    """
    revenues = load_data('revenues', column_order=order, reverse=reverse)
    table.setColumnCount(len(TRANS_COLS_NAMES))
    table.setHorizontalHeaderLabels(TRANS_COLS_NAMES)

    table.sort_name = order
    table.reversed = reverse
    width, height = TABLES_SIZE['Revenues']
    x_position = LEFTSPACE
    y_position = DOWNSPACE
    for column in range(table.columnCount()):
        table.setColumnWidth(column, TRANS_COLS_WIDTH[column])
    table.setGeometry(x_position, y_position, width + ID_WIDTH, height)
    table.verticalHeader().setFixedWidth(ID_WIDTH)
    table.setRowCount(len(revenues))
    for row, row_content in enumerate(revenues):
        for column, column_content in enumerate(row_content):
            table.setItem(row, column, QTableWidgetItem(str(column_content)))

def update_budget(index: int, data: float) -> None:
    update_row('categories', [CATS_DB_COLS_NAMES[0], CATS_DB_COLS_NAMES[2]], [index, data])



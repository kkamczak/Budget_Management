"""
This module contains auxiliary functions
"""
from datetime import datetime
from typing import Optional, Any
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate
from src.settings import MONTHS

def puts (text: Any) -> None:
    """
    Print a formatted message and write it to the logging file.

    Args:
    text (Any): The message to be printed and logged.

    Prints a formatted message with a timestamp and writes it to the 'src/logging.txt' file.
    """
    text = str(text)
    date_time = datetime.now()
    message = '['+str(date_time.strftime("%Y/%m/%d, %H:%M:%S"))+'] '+ text
    with open('src/logging.txt', 'a', encoding='utf-8') as file:
        file.write(message)
    print(message)

def message_box(msg: str, info: Optional[str] = None) -> None:
    """
    Display a message box.

    Args:
        msg (str): The main message to be displayed in the message box.
        info (Optional[str]): Additional information to be displayed
        in the message box. Default is None.
    """
    if info is not None:
        text = f'{msg}\n--message: "{info}"'
    else:
        text = msg
    message = QMessageBox()
    message.setText(text)
    message.exec_()

def get_first_last_day(month: Optional[int] = None) -> list[QDate, QDate]:
    """
    Get the first and last day of a given month or the current month.

    Args:
        month (Optional[int]): The month for which to get the first and last day.
        If None, the current month is used.

    Returns:
        list[QDate, QDate]: A list containing the first and last day of the specified month.
    """
    today = QDate.currentDate()
    if month is None:
        month = today.month()

    first_day = QDate(today.year(), month, 1)

    next_month = QDate(today.year(), month + 1, 1)
    last_day = next_month.addDays(-1)

    return [first_day, last_day]

def get_current_month() -> str:
    """
    Get the name of the current month.

    Returns:
        str: The name of the current month.
    """
    month = QDate.currentDate().month()
    months = list(MONTHS.keys())
    return months[month-1]

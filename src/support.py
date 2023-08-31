"""
This module contains auxiliary functions
"""
from datetime import datetime
from typing import Optional
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate

def puts (text: str) -> None:
    """
    This method prints formatted message and also writes this on the logging file...
    :param text: str
    :return: None
    """
    date_time = datetime.now()
    message = '['+str(date_time.strftime("%Y/%m/%d, %H:%M:%S"))+'] '+ text
    with open('src/logging.txt', 'a') as file:
        file.write(message)
    print(message)

def message_box(msg: str, info: Optional[str] = None) -> None:
    '''
    This function display message box
    :param msg: str
    :param info: Optional[str]
    :return: None
    '''
    if info is not None:
        text = f'{msg}\n--message: "{info}"'
    else:
        text = msg
    message = QMessageBox()
    message.setText(text)
    message.exec_()

def get_first_last_day(month: Optional[int] = None) -> list[QDate, QDate]:
    today = QDate.currentDate()
    if month is None:
        month = today.month()

    first_day = QDate(today.year(), month, 1)

    next_month = QDate(today.year(), month + 1, 1)
    last_day = next_month.addDays(-1)

    return [first_day, last_day]

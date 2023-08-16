from datetime import datetime
from typing import Optional
from PyQt5.QtWidgets import QMessageBox

def format_list_row(row: tuple) -> str:
    text = f"{row[0]} | {row[1]} | {row[2]} | {row[3]} zł"
    return text

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
    :param info: str
    :return: None
    '''
    if info is not None:
        text = f'{msg}\n--message: "{info}"'
    else:
        text = msg
    message = QMessageBox()
    message.setText(text)
    message.exec_()

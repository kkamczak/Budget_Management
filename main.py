import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.program import MyGUI

#---------CATCHING ERRORS--------------------------------------
def catch_exceptions(type, value, traceback):
    QMessageBox.critical(None,
                         "An exception was raised", f"\nException type: '{type}' \nDescription: '{value}'")
    old_hook(type, value, traceback)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions
#--------------------------------------------------------------

def main() -> None:

    app = QApplication(sys.argv)
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()
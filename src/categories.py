"""
Then module is used to display category edit window.
"""
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from typing import Callable
from src.database import check_if_exists, insert_data, load_data, get_id_by_name, update_row, delete_record
from src.support import message_box
from src.settings import CATEGORIES_COLUMNS_NAMES

class Categories_Window(QWidget):
    """
    This class is responsible for the category edit window
    """
    def __init__(self, configure: Callable) -> None:
        """
        :param configure: Callable
        """
        super().__init__()
        uic.loadUi('src/gui/categories_window.ui', self) # Load GUI from designer.exe file
        self.setWindowTitle("Categories")
        self.setFixedSize(self.size())
        self.show()

        self.configure_main_window = configure # This is method for configure tables on main window

        self.button_add.clicked.connect(self.add)
        self.button_edit.clicked.connect(self.edit)
        self.button_delete.clicked.connect(self.delete)
        self.button_cancel.clicked.connect(self.close)
        self.configure_window()

    def configure_window(self) -> None:
        """
        This method configures the items on the window
        :return: None
        """
        # -- Configure QComboBox item ----------------
        self.box_categories.clear()
        categories_names = []
        respond = load_data('categories', 'ID')
        for item in respond:
            categories_names.append(item[1])
        self.box_categories.addItems(categories_names)
        # --------------------------------------------

    def add(self) -> None:
        """
        This method is used to add a new category
        :return: None
        """
        name = self.line_name.text()
        if check_if_exists('categories', 'Nazwa', name):
            message_box('[ADD]This category already exists...')
        else:
            insert_data('categories', [name, 0.0])
            message_box(f"Added category: '{name}'")
            self.configure_window()
            self.configure_main_window()
            self.box_categories.setCurrentText(name)

    def edit(self) -> None:
        """
        This method is used to edit category
        :return: None
        """
        name = self.line_name.text()
        if check_if_exists('categories', 'Nazwa', name):
            message_box('[EDIT]This category already exists...')
        else:
            old_name = self.box_categories.currentText()
            id = get_id_by_name('categories', 'Nazwa', old_name)
            new_data = [id, name]
            update_row('categories', CATEGORIES_COLUMNS_NAMES, new_data)
            message_box(f"Category name changed from '{old_name}' to '{name}'")
            self.configure_window()
            self.configure_main_window()

    def delete(self) -> None:
        """
        This category is used to delete category
        :return: None
        """
        name = self.box_categories.currentText()
        id = get_id_by_name('categories', 'Nazwa', name)
        delete_record('categories', id)
        message_box(f"Removed category: '{name}'")
        self.configure_window()
        self.configure_main_window()

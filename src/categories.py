from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from typing import Callable
from src.database import check_if_exists, insert_data, load_data, get_id_by_name, update_row, delete_record
from src.support import message_box, puts
from src.settings import CATEGORIES_COLUMNS_NAMES

class Categories_Window(QWidget):
    def __init__(self, configure: Callable) -> None:
        super().__init__()
        # Load and init GUI-----------------
        uic.loadUi('src/gui/categories_window.ui', self)
        self.setWindowTitle("Categories")
        self.setFixedSize(self.size())
        self.show()

        self.configure_table = configure

        self.button_add.clicked.connect(self.add)
        self.button_edit.clicked.connect(self.edit)
        self.button_delete.clicked.connect(self.delete)
        self.button_cancel.clicked.connect(self.close)
        self.configure_window()

    def configure_window(self):
        self.box_categories.clear()
        categories_names = []
        respond = load_data('categories', 'ID')
        for item in respond:
            categories_names.append(item[1])
        self.box_categories.addItems(categories_names)

    def add(self):
        name = self.line_name.text()
        if check_if_exists('categories', 'Nazwa', name):
            message_box('[ADD]Ta kategoria już istnieje...')
        else:
            insert_data('categories', [name])
            message_box(f"Dodano kategorie '{name}'")
            self.configure_window()

    def edit(self):
        name = self.line_name.text()
        if check_if_exists('categories', 'Nazwa', name):
            message_box('[EDIT]Ta kategoria już istnieje...')
        else:
            old_name = self.box_categories.currentText()
            id = get_id_by_name('categories', 'Nazwa', old_name)
            new_data = [id, name]
            update_row('categories', CATEGORIES_COLUMNS_NAMES, new_data)
            message_box(f"Zmieniono nazwe kategorii '{old_name}' na '{name}'")
            self.configure_window()

    def delete(self):
        name = self.box_categories.currentText()
        id = get_id_by_name('categories', 'Nazwa', name)
        delete_record('categories', id)
        message_box(f"Usunięto kategorie '{name}'")
        self.configure_window()

"""
This module set up all global variables
"""
DATABASE_PATH = 'src/data/database.db'

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
DOWNSPACE = int(SCREEN_HEIGHT / 17)
LEFTSPACE = int(SCREEN_WIDTH / 150)
BUTTONSPACE = 50
ID_WIDTH = 25

TABLES_SIZE = {
    'Expenses': (int(SCREEN_WIDTH / 3), int(SCREEN_HEIGHT / 2)),
    'Categories': (int(SCREEN_WIDTH / 3), int(SCREEN_HEIGHT / 2)),
    'Revenues': (int(SCREEN_WIDTH / 3), int(SCREEN_HEIGHT / 3))
}

BUTTON_1_SIZE = (140, 40)

w = int(TABLES_SIZE['Expenses'][0] / 10)
EXPENSES_COLUMNS_WIDTH = [w, 2*w,3*w, 2*w, 2*w]
EXPENSES_COLUMNS_NAMES = ['ID', 'Data', 'Nazwa', 'Kategoria', 'Wartość']

CATEGORIES_COLUMNS_NAMES = ['ID', 'Nazwa', 'Budżet']
w = int(TABLES_SIZE['Categories'][0] / 10)
CATEGORIES_COLUMNS_WIDTH = [4*w, 3*w, 3*w]
CATEGORIES_TABLE_COLUMN_NAMES = ['Nazwa kategorii', 'Budżet', 'Suma wydatków']


ERROR_CONNECT_TO_DATABASE = 'There was problem with connect to database...'

VALUE_MAX = 10000.00
VALUE_MIN = 0.00




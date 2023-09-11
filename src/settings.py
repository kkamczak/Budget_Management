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

TRANSACTIONS = ['Wydatek', 'Przychód']
MONTHS = {
    "styczeń": 1,
    "luty": 2,
    "marzec": 3,
    "kwiecień": 4,
    "maj": 5,
    "czerwiec": 6,
    "lipiec": 7,
    "sierpień": 8,
    "wrzesień": 9,
    "październik": 10,
    "listopad": 11,
    "grudzień": 12
}

TABLES_SIZE = {
    'Expenses': (int(SCREEN_WIDTH / 3), int(SCREEN_HEIGHT / 2)),
    'Categories': (int(SCREEN_WIDTH / 3), int(SCREEN_HEIGHT / 2)),
    'Revenues': (int(SCREEN_WIDTH / 3), int(SCREEN_HEIGHT / 3)),
    'Plot': (int(SCREEN_WIDTH / 3) + 28, int(SCREEN_HEIGHT / 3))
}

LABELS = {
    'Revenues': (LEFTSPACE, int(SCREEN_HEIGHT / 80), int(SCREEN_WIDTH / 3) + 25, 28),
    'Expenses': (LEFTSPACE, int(SCREEN_HEIGHT / 2.52), int(SCREEN_WIDTH / 3) + 25, 28)
}

PLOT_SIZE = (5, 4) # <- in inches

BUTTON_1_SIZE = (140, 40)

w = int(TABLES_SIZE['Expenses'][0] / 10)
TRANS_COLS_WIDTH = [w, 2 * w, 3 * w, 2 * w, 2 * w]
TRANS_COLS_NAMES = ['ID', 'Data', 'Nazwa', 'Kategoria', 'Wartość']

CATS_DB_COLS_NAMES = ['ID', 'Nazwa', 'Budżet', 'Rodzaj']
w = int(TABLES_SIZE['Categories'][0] / 10)
CAT_TABLE_COLS_WIDTH = [4 * w, 2 * w, 2 * w, 2 * w]
CATS_TABLE_COLS_NAMES = ['Nazwa kategorii', 'Budżet', 'Wydane', 'Stan']

ERROR_CONNECT_TO_DATABASE = 'There was problem with connect to database...'

VALUE_MAX = 10000.00
VALUE_MIN = 0.00






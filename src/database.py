import sqlite3
from src.settings import COLUMNS_NAMES, DATABASE_PATH
from src.support import puts

def create_tables() -> None:
    """
    This function create database and table 'expenses' if not exists...
    :return: None
    """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        puts(e.__str__())
    finally:
        if connection:
            # Create cursor
            cursor = connection.cursor()
            # Create a Table
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS expenses(
                           {COLUMNS_NAMES[0]} text,
                           {COLUMNS_NAMES[1]} text,
                           {COLUMNS_NAMES[2]} text,
                           {COLUMNS_NAMES[3]} text,
                           {COLUMNS_NAMES[4]} text
                       )""")

            cursor.execute(f"""CREATE TABLE IF NOT EXISTS categories(
                                       'Nazwa' text                 
                        )""")

            connection.commit()
            connection.close()
        else:
            puts('There was problem with connect to database...')


def insert_data(table_name: str, data: list[str]) -> None:
    """
    This function inserts data to table in database...
    :param table_name: str
    :param data: list[str]
    :return: None
    """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        puts(e.__str__())
    finally:
        if connection:
            # Create cursor
            cursor = connection.cursor()
            # Insert data
            cursor.execute(f"SELECT MAX(rowid) FROM {table_name}")
            print(data)
            for answer in cursor.fetchone():
                if not answer:
                    data.insert(0, 0)
                else:
                    data.insert(0, answer)
            print(data)
            placeholders = ",".join(["?" for _ in data])
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)

            connection.commit()
            connection.close()
        else:
            puts('There was problem with connect to database...')

def load_expenses() -> list[tuple]:
    """
        This function inserts data to table in database...
        :param table_name: str
        :param data: list[str]
        :return: None
        """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        puts(e.__str__())
    finally:
        expenses = []
        if connection:
            # Create cursor
            cursor = connection.cursor()

            table = 'expenses'

            cursor.execute(f"SELECT rowid, * FROM {table} ORDER BY Data")
            for item in cursor.fetchall():
                expense = (item[1], item[2], item[3], item[4], float(item[5]))
                expenses.append(expense)

            connection.commit()
            connection.close()

            return expenses
        else:
            puts('There was problem with connect to database...')
            return expenses

def update_row(table_name: str, column_names: list[str], data: list[str]) -> None:
    """
    This function inserts data to table in database...
    :param table_name: str
    :param data: list[str]
    :return: None
    """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        puts(e.__str__())
    finally:
        if connection:
            # Create cursor
            cursor = connection.cursor()
            # Insert data
            set_placeholder = [f"{column_name} = '{data[index]}'" for index, column_name in enumerate(column_names)]
            set_placeholder = ", ".join(set_placeholder)

            cursor.execute(f"UPDATE {table_name} SET {set_placeholder} WHERE ID = {data[0]}")

            connection.commit()
            connection.close()
        else:
            puts('There was problem with connect to database...')

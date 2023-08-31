"""
This module contains functions to handle the database
"""
import sqlite3
from src.settings import DATABASE_PATH, TRANS_COLS_NAMES, CATS_DB_COLS_NAMES, ERROR_CONNECT_TO_DATABASE
from src.support import puts, message_box
from typing import Optional, Any

def create_tables() -> None:
    """
    This function create database and tables if they not exists...
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
                           {TRANS_COLS_NAMES[0]} integer,
                           {TRANS_COLS_NAMES[1]} text,
                           {TRANS_COLS_NAMES[2]} text,
                           {TRANS_COLS_NAMES[3]} text,
                           {TRANS_COLS_NAMES[4]} real
                       )""")

            cursor.execute(f"""CREATE TABLE IF NOT EXISTS revenues(
                                       {TRANS_COLS_NAMES[0]} integer,
                                       {TRANS_COLS_NAMES[1]} text,
                                       {TRANS_COLS_NAMES[2]} text,
                                       {TRANS_COLS_NAMES[3]} text,
                                       {TRANS_COLS_NAMES[4]} real
                                   )""")

            cursor.execute(f"""CREATE TABLE IF NOT EXISTS categories(
                            {CATS_DB_COLS_NAMES[0]} integer,
                            {CATS_DB_COLS_NAMES[1]} text,
                            {CATS_DB_COLS_NAMES[2]} real,
                            {CATS_DB_COLS_NAMES[3]} text              
                        )""")

            connection.commit()
            connection.close()
        else:
            puts(ERROR_CONNECT_TO_DATABASE)

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
            cursor = connection.cursor() # Create cursor

            try:
                cursor.execute(f"SELECT MAX(rowid) FROM {table_name}") # Check for last row id

                for answer in cursor.fetchone(): # If there is nothing in table, put 0
                    if not answer:
                        data.insert(0, 0)
                    else:
                        data.insert(0, answer)

                placeholders = ",".join(["?" for _ in data])
                cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)

            except Exception as e:
                puts(f"Exception: {e.__str__()}")
                message_box(f'There was unexpected error with inserting data...')

            connection.commit()
            connection.close()
        else:
            puts(ERROR_CONNECT_TO_DATABASE)

def load_data(table_name: str, column_order: str, reverse: Optional[bool] = False, kind: Optional[list] = None, date: Optional[list[str]] = None) -> list[tuple]:
    """
        This function inserts data from table in database...
        :param table_name: str
        :param column_order: str
        :param reverse: Optional[bool]
        :param kind: Optional[list]
        :param date: Optional[list]
        :return: None
        """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        puts(e.__str__())
    finally:
        data_list = []
        if connection:
            cursor = connection.cursor() # Create cursor

            try:
                if reverse:
                    column_order = f"{column_order} DESC"
                if date:
                    cursor.execute(f"SELECT rowid, * FROM {table_name} WHERE Data BETWEEN '{date[0]}' AND '{date[1]}' ORDER BY {column_order}")
                elif kind:
                    cursor.execute(f"SELECT rowid, * FROM {table_name} WHERE {kind[0]} LIKE '{kind[1]}' ORDER BY {column_order}")
                else:
                    cursor.execute(f"SELECT rowid, * FROM {table_name} ORDER BY {column_order}")
                for item in cursor.fetchall():
                    date = item[1:]
                    data_list.append(date)
            except Exception as e:
                puts(f"Exception: {e.__str__()}")
                message_box(f'There was unexpected error with loading data...')

            connection.commit()
            connection.close()

            return data_list
        else:
            puts(ERROR_CONNECT_TO_DATABASE)
            return data_list

def update_row(table_name: str, column_names: list[str], data: list[Any]) -> None:
    """
    This function inserts data to table in database...
    :param table_name: str
    :param column_names: list[str]
    :param data: list[Any]
    :return: None
    """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        puts(e.__str__())
    finally:
        if connection:
            cursor = connection.cursor() # Create cursor

            set_placeholder = [f"{column_name} = '{data[index]}'" for index, column_name in enumerate(column_names)]
            set_placeholder = ", ".join(set_placeholder)
            try:
                cursor.execute(f"UPDATE {table_name} SET {set_placeholder} WHERE ID = {data[0]}")
            except Exception as e:
                puts(f"Exception: {e.__str__()}")
                message_box(f'There was unexpected error with updating data...')

            connection.commit()
            connection.close()
        else:
            puts(ERROR_CONNECT_TO_DATABASE)

def delete_record(table_name: str, index: int) -> None:
    """
        This function delete one record in table...
        :param table_name: str
        :param index: int
        :return: None
        """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        puts(e.__str__())
    finally:
        if connection:
            cursor = connection.cursor() # Create cursor

            try:
                cursor.execute(f"DELETE from {table_name} WHERE ID = {index}")
            except Exception as e:
                puts(f"Exception: {e.__str__()}")
                message_box(f'There was unexpected error with deleting data...')

            connection.commit()
            connection.close()
        else:
            puts(ERROR_CONNECT_TO_DATABASE)

def check_if_exists(table_name: str, column_name: str, content: str) -> bool:
    """
            This function check if record exists in table...
            :param table_name: str
            :param column_name: str
            :param content: str

            :return: bool
            """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        puts(e.__str__())
    finally:
        if connection:
            cursor = connection.cursor() # Create cursor

            try:
                cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} LIKE '{content}'")
                if cursor.fetchall():
                    return True
                return False
            except Exception as e:
                puts(f"Exception: {e.__str__()}")
                message_box(f'There was unexpected error with checking data...')

            connection.commit()
            connection.close()
        else:
            puts(ERROR_CONNECT_TO_DATABASE)

def get_id_by_name(table_name: str, column_name: str, name: str) -> Optional[int]:
    """
    This function gets id by name...
    :param table_name: str
    :param column_name: str
    :param name: str

    :return: Optional[int]
    """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        puts(e.__str__())
    finally:
        if connection:
            cursor = connection.cursor()  # Create cursor

            try:
                cursor.execute(f"SELECT ID FROM {table_name} WHERE {column_name} LIKE '{name}'")
                respond = cursor.fetchall()
                if respond:
                    id = respond[0][0]
                    return id
                return
            except Exception as e:
                puts(f"Exception: {e.__str__()}")
                message_box(f'There was unexpected error with getting ID by name...')

            connection.commit()
            connection.close()
        else:
            puts(ERROR_CONNECT_TO_DATABASE)

def sum_all_cells(table_name: str, target: str, by_column: str, content: str, date: str) -> float:
    """
   This function gets id by name...
   :param table_name: str
   :param target: str
   :param by_column: str
   :param content: str

   :return: float
   """
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_PATH)
    except Exception as e:
        puts(e.__str__())
    finally:
        if connection:
            cursor = connection.cursor() # Create cursor

            try:
                cursor.execute(f"SELECT {target} FROM {table_name} WHERE {by_column} LIKE '{content}' AND Data BETWEEN '{date[0]}' AND '{date[1]}'")
                respond = cursor.fetchall()
                sum = 0.0
                for item in respond:
                    sum += item[0]
                return sum
            except Exception as e:
                puts(f"Exception: {e.__str__()}")
                message_box(f'There was unexpected error with summing database cells function..')

            connection.commit()
            connection.close()
        else:
            puts(ERROR_CONNECT_TO_DATABASE)

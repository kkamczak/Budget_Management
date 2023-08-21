import unittest
from src.database import load_data
from unittest.mock import patch


class TestLoadExpenses(unittest.TestCase):
    @patch('src.database.sqlite3.connect')
    def test_load_expenses(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (1, 1, 'Item1', 'Category1', '2023-08-01', 100.0),
            (2, 2, 'Item2', 'Category2', '2023-08-02', 150.0)
        ]

        result = load_data()

        expected_result = [
            (1, 'Item1', 'Category1', '2023-08-01', 100.0),
            (2, 'Item2', 'Category2', '2023-08-02', 150.0)
        ]

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
import os
import pyodbc
from pyodbc import Cursor, Connection
from utility.colors import Colors

class SqlMode:
    """
    Manages all SQL related operations for the application.
    """
    def __init__(self):
        self.conn: Connection = None
        self.cursor: Cursor = None

    def connect_to_database(self) -> bool:
        """
        Connects to an SQL Server database using the configs provided in the .env file

        Returns:
            bool: Represents whether or not the connection was successful
        """
        driver = '{ODBC Driver 18 for SQL Server}'
        server = os.getenv('DB_Server')
        database = os.getenv('DB_Database')
        username = os.getenv('DB_Username')
        password = os.getenv('DB_Password')
        encrypt = 'no'
        trustServerCertificate = 'yes'

        conn_str = (
            f"DRIVER={driver};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"Encrypt={encrypt};"
            f"TrustServerCertificate={trustServerCertificate};"
        )

        try:
            self.conn = pyodbc.connect(conn_str, autocommit = True)
            self.cursor = self.conn.cursor()
            print(f'{Colors.GREEN}Successfully connected to database.{Colors.ENDC}')
            return True
        except Exception as e:
            print(f'{Colors.FAIL}Failed to connect to database: {str(e)}{Colors.ENDC}')
            return False
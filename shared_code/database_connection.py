from urllib.parse import quote_plus

class SQLconnection:
    def __init__(self, server, database, user, password, port) -> None:
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn_str = self.__get_connection_str()

    def __get_connection_str(self):
        # params = quote_plus(f'mysql+pymysql://{self.user}:{self.password}@{self.server}:{self.port}/{self.database}')

        params = quote_plus(
            "Driver={ODBC Driver 18 for SQL Server};"
            f"Server=tcp:{self.server},{self.port};Database={self.database};"
            f"Uid=n{self.user};"
            f"Pwd={self.password};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )

        conn_str = f'mssql+pyodbc:///?odbc_connect={params}'
        return conn_str




from sqlalchemy import create_engine
import pandas as pd

class conexion_SQL:
    def __init__(self, server, driver="ODBC Driver 17 for SQL Server"):
        self.__server = server
        self.__database = 'energia'
        self.__driver = driver
        self.__create_engine()

    def __create_engine(self):
        connection_string = (
            f"mssql+pyodbc://@{self.__server}/{self.__database}"
            f"?driver={self.__driver.replace(' ', '+')}"
            f"&Trusted_Connection=yes"
        )
        self.__engine = create_engine(connection_string)

    @property
    def server(self):
        return self.__server

    @server.setter
    def server(self, value):
        self.__server = value
        self.__create_engine()

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, value):
        self.__database = value
        self.__create_engine()

    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, value):
        self.__driver = value
        self.__create_engine()

    @property
    def engine(self):
        return self.__engine

    def consultar(self, query):
        return pd.read_sql_query(query, con=self.__engine)

    def df_a_sql(self, df, tabla, if_exists="replace"):
        df.to_sql(tabla, con=self.__engine, if_exists=if_exists, index=False)

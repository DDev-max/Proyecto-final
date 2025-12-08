import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from basedatos.conexion_sql import conexion_SQL


class Visualizador:

    def __init__(self, servidor):
        self.__servidor = None
        self.__conexion = None
        self.__df = None
        self.servidor = servidor

    @property
    def servidor(self):
        return self.__servidor

    @servidor.setter
    def servidor(self, servidor):
        self.__servidor = servidor
        self.__conexion = conexion_SQL(self.__servidor)

    @property
    def conexion(self):
        return self.__conexion

    @conexion.setter
    def conexion(self, conexion):
        self.__conexion = conexion

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, df):
        self.__df = df

    def cargar_tabla(self, tabla="consumo"):
        query = f"SELECT * FROM {tabla}"
        self.__df = self.__conexion.consultar(query)

    # 1️ MW por hora
    def grafico_mw_por_hora(self):
        datos = self.__df.groupby("hora")["MW"].mean()
        sns.lineplot(x=datos.index, y=datos.values)
        plt.title("Consumo promedio (MW) por hora del día")
        plt.xlabel("Hora")
        plt.ylabel("MW")
        plt.tight_layout()
        plt.show()

    # 2 MW por mes
    def grafico_mw_por_mes(self):
        datos = self.__df.groupby("mes")["MW"].mean()
        sns.barplot(x=datos.index, y=datos.values)
        plt.title("Consumo promedio (MW) por mes del año")
        plt.xlabel("Mes")
        plt.ylabel("MW")
        plt.tight_layout()
        plt.show()

    # 3 MW vs temperatura
    def grafico_mw_vs_temp(self):
        sns.scatterplot(data=self.__df, x="apparent_temperature", y="MW")
        plt.title("Relación entre temperatura y MW")
        plt.xlabel("Temperatura Aparente")
        plt.ylabel("MW")
        plt.tight_layout()
        plt.show()

    # 4️ MW vs nubosidad
    def grafico_mw_vs_nubes(self):
        sns.scatterplot(data=self.__df, x="cloud_cover", y="MW")
        plt.title("Consumo de MW según nubosidad")
        plt.xlabel("Nubosidad (%)")
        plt.ylabel("MW")
        plt.tight_layout()
        plt.show()


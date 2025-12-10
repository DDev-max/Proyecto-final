import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from basedatos.conexion_sql import conexion_SQL


# Clase para realizar EDA
class ProcesadorEDA:

    def __init__(self, servidor):
        self.__servidor = None
        self.__conexion = None
        self.__df = None
        self.servidor = servidor

    # Propiedad servidor
    @property
    def servidor(self):
        return self.__servidor

    @servidor.setter
    def servidor(self, servidor):
        self.__servidor = servidor
        self.__conexion = conexion_SQL(self.__servidor)

    # Propiedad conexión a la BD
    @property
    def conexion(self):
        return self.__conexion

    @conexion.setter
    def conexion(self, conexion):
        self.__conexion = conexion

    # Propiedad DataFrame
    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, df):
        self.__df = df

    # Cargar tabla desde SQL
    def cargar_tabla(self, tabla="consumo"):
        query = f"SELECT * FROM {tabla}"
        self.__df = self.__conexion.consultar(query)

    # Estadísticas básicas
    def estadisticas(self):
        return self.__df.describe(include="all")

    # Matriz de correlación
    def correlacion(self):
        return self.__df.corr(numeric_only=True)

    # Heatmap
    def grafico_correlacion(self):
        corr = self.correlacion()
        plt.figure(figsize=(12, 7))
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.title("Matriz de Correlación")
        plt.tight_layout()
        plt.show()







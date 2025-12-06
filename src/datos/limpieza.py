class Limpieza():
    def __init__(self, df):
        self.__df = df

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, nuevo_df):
        self.__df = nuevo_df

    def eliminar_cols(self, columnas):
        self.__df = self.__df.drop(columns = columnas)

    def transformar_fecha(self, columna):
        self.__df['mes'] = self.__df[columna].dt.month
        self.__df['dia_mes'] = self.__df[columna].dt.day
        self.__df['hora'] = self.__df[columna].dt.hour
        self.__df['dia_sem'] = self.__df[columna].dt.weekday
        self.__df['anio'] = self.__df[columna].dt.year



from pandas import read_csv
from .modify import add_dates
from datetime import datetime

class Cirrus:
    def __init__(self, path:str):
        self.path = path
        self.data = self.__parse_data__()
    
    def __import_data__(self):
        data = read_csv(self.path,
                           delimiter=';',
                           decimal=',',
                           parse_dates=True)
        return data
    
    def __parse_data__(self):
        return add_dates(self.__import_data__(),
                         self.start_date,
                         formatted=True
                         ).drop(['Fecha', 'Tiempo'], axis=1)
    @property
    def start_date(self):
        date = f'{self.__import_data__().iloc[0]['Fecha']} {self.__import_data__().iloc[0]['Tiempo']}'
        return datetime.strptime(date, '%d-%m-%Y %H:%M:%S')       
    
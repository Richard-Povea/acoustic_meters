from pandas import read_csv, DataFrame
from .modify import add_dates
from datetime import datetime
from .sonometer import Sonometer

class Cirrus(Sonometer):
    def __init__(self, path:str):
        super().__init__(path)
    
    def __import_data__(self)->DataFrame:
        data = read_csv(self.path,
                           delimiter=';',
                           decimal=',',
                           parse_dates=True)
        return self.__parse_data__(data)
    
    def __parse_data__(self, data:DataFrame):
        return add_dates(data,
                         self.start_date,
                         formatted=True
                         ).drop(['Fecha', 'Tiempo'], axis=1)
    @property
    def start_date(self):
        start_date = self.__import_data__().iloc[0]['Fecha']
        start_time = self.__import_data__().iloc[0]['Tiempo']
        date = '{} {}'.format(start_date, start_time)
        return datetime.strptime(date, '%d-%m-%Y %H:%M:%S')       
    
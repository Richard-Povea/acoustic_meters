from pandas import read_csv, DataFrame
from .modify import add_dates
from datetime import datetime
from .sonometer import Sonometer

class CirrusSonometer(Sonometer):
    def __init__(self, path:str):
        super().__init__(path)
        self._data = None  # Atributo para almacenar los datos una vez importados
    
    def __import_data__(self)->DataFrame:
        return read_csv(self.path,
                           delimiter=';',
                           decimal=',',
                           parse_dates=True)
    
    def __parse_data__(self)->None:
        """
        Modify the data
        """
        self.data = add_dates(self.data,
                              self.start_date,
                              formatted=True
                              ).drop(['Fecha', 'Tiempo'], axis=1)
    
    @property
    def data(self):
        if self._data is None:
            self._data = self.__import_data__()
        return self._data

    @data.setter
    def data(self, new_data):
        # Puedes implementar la lógica necesaria aquí para validar o procesar los nuevos datos asignados
        self._data = new_data
    @property
    def start_date(self):
        if self._data is None:
            self._data = self.__import_data__()
        start_date = self.data.iloc[0]['Fecha']
        start_time = self.data.iloc[0]['Tiempo']
        date = '{} {}'.format(start_date, start_time)
        return datetime.strptime(date, '%d-%m-%Y %H:%M:%S')       
    
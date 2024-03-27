from datetime import timedelta
from enum import Enum
from pandas import DataFrame, ExcelFile, read_excel
from numpy import log10
from sonometer import Sonometer

class Sheets_es(Enum):
	RESUMEN = 0
	OBA = 1
	REGISTRO_DE_SESION = 2
	ESTADISTICAS = 3
	HISTORIA_DEL_TIEMPO = 4

class Sheets_en(Enum):
	SUMMARY = 0
	OBA = 1
	SESSION_LOG = 2
	STATISTICS = 3
	TIME_HISTORY = 4
	HOJA1 = 5

class Larson(Sonometer):
    def __init__(self, path:str):
        self.path = path
        super().__init__(path) 

    def __import_data__(self) -> DataFrame:
        file = ExcelFile(self.path)
        return file.getData()

    @property
    def one_third_octaves(self):
        return Larson(self.data.filter(like='1/3 LZ'))
    
    @property
    def octaves(self):
        return Larson(self.data.filter(like='1/1 LZ'))
    
    @property
    def eq(self):
        return Larson(self.data.filter(like='eq'))

    @property
    def min(self):
        return Larson(self.data.filter(like='min'))
    
    @property
    def max(self):
        return Larson(self.data.filter(like='max'))
    
    @property
    def n_days(self)->int:
        return (self.data.index.max() - 
                self.data.index.min()).days
    
    @property
    def start_date(self):
        start_date = self.data.index.min()
        return start_date
    
    def week(self, n_week:int):
        if n_week*7>=self.n_days:
            return None
        # Obtener el índice datetime del DataFrame
        time = self.data.index
        week = time.min() + timedelta(weeks=n_week) + timedelta(days=n_week)
        # Obtener el rango de fechas de la semana siguiente
        weekend = time.min() + timedelta(weeks=n_week+1)
        # Filtrar el DataFrame por el rango de fechas de la semana 
        week:int = self.data[(time >= week) & (time <= weekend)]
        return week
    
class ExcelFile:
    __TIME_HISTORY_COLUMNS__ = [
        'Registro #','Tipo de registro','Hora',
        'LAeq','LZpk','LASmax',
        'LASmin','OVLD','OBA OVLD',
        'marcadores'
        ] #Time history columns to drop

    def __init__(self, file_path:str):
        self.file_path = file_path
        self.file = self.readExcelFile(file_path)

    def readExcelFile(self, file_path):
        try:
            return ExcelFile(file_path)
        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")

    def basicStats(self):
        return self.file.parse(sheet_name=self.sheetNames[-1],
                               index_col=0,
                               skiprows=[1],
                               usecols=['Fecha', 
                                        'LAeq', 
                                        'LASmax', 
                                        'LASmin'])

    @property
    def sheetNames(self):
        return self.file.sheet_names  
    
    def getData(self) -> DataFrame:
        return read_excel(
            self.file_path,
            sheet_name=self.sheetNames[-1],
            index_col=2, 
            skiprows=[1]).drop(
                self.__TIME_HISTORY_COLUMNS__, axis=1
                )

def to_octave(data:DataFrame)->None:
    data = data
    group_columns = [data.columns[i:i+3] for i in range(0, len(data.columns), 3)]
    # Calcular la suma de cada grupo y crear un nuevo DataFrame
    df_sum = DataFrame()
    for group in group_columns:
        column = group[1]  # Nombre de la segunda columna en el grupo
        sum = 10*log10((10**(data[group]/10)).sum(axis=1))
        df_sum[column] = sum

from pandas import DataFrame
from numpy  import log10, arange
from datetime import datetime, timedelta
from .sonometer import Sonometer

def reduce_data(sonometer:Sonometer, time:int = 60):
    """Take the data and reduce it to the time period specified

    Args:
        time (int, optional): Time to reduce all data. Defaults to 60.
    """
    df = sonometer.data
    index = df.index
    # Agrupar los datos en intervals de 60 segundos
    interval = time  # segundos
    df['interval'] = (arange(len(df)) // interval) * interval

    # Calcular el promedio logarítmico para cada interval
    log_mean = df.groupby(
        'interval'
        ).apply(
            lambda x: 10 * log10((
                10**(x/10)
                ).mean()))
    log_mean = log_mean.drop(columns='interval').round(1)
    return log_mean.set_index(index[log_mean.index])

def add_dates(data:DataFrame, base_date:str, formatted:bool=False)->DataFrame:
    """ Adds a date index to the dataframe

    Args:
        data (pd.DataFrame): data to add dates
        base_date (str): base date of the dataframe as a string 
        like `2024-02-07 19:40:22`

    Returns:
        pd.DataFrame: data with dates as index
    """
    if not formatted:
        base_date = datetime.strptime(base_date, '%Y-%m-%d %H:%M:%S')
    dates = [base_date + timedelta(seconds=number) for number in data.index]
    data.index = dates
    return data

if __name__ == '__main__':
    print("Modify package")

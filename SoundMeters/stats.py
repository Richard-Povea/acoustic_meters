from .constants import FREQ_1_1_TICKS, FREQ_SYMLOG_TICKS, FREQ_SYMLOG_LABELS, DAYS, map_days
from .larson import Data
from acoustics.calc import log_mean
from numpy import arange, meshgrid, linspace
from pandas import DataFrame
import matplotlib.pyplot as plt

def plot_contourf(df:DataFrame, ax):
    # Obtener el índice datetime del DataFrame
    tiempo = df.index
    # Convertir el índice datetime a números enteros (puede ser necesario para contourf)
    tiempo_num = arange(len(tiempo))
    # Convertir las frecuencias a números enteros
    frecuencias_num = FREQ_1_1_TICKS
    # Crear una cuadrícula de coordenadas de tiempo y frecuencia
    tiempo_grid, frecuencias_grid = meshgrid(tiempo_num, frecuencias_num)
    # Obtener los decibeles del DataFrame
    decibeles = df.values.T  # Transponer para que las frecuencias estén en el eje y
    # Crear el gráfico contourf
    
    im = ax.contourf(tiempo_grid, frecuencias_grid, decibeles, cmap='viridis')
    return im

def compare_weeks(data:Data, name:str)->None:
    n_weeks = data.n_days//7
    weeks = [data.week(n_week) for n_week in range(n_weeks)]
    fig, axes = plt.subplots(n_weeks, 1, sharex=True, sharey=True, figsize=(10, 7))
    for index, week in enumerate(weeks):
        ax = axes[index]
        im = plot_contourf(week, ax)
        ax.title.set_text('Semana N°{}'.format(index+1))
        ax.set_ylabel('Frecuencia [Hz]')
        ax.set_ylim(bottom=8, top=16_000)
        ax.set_yscale('symlog')
        ax.set_yticks(FREQ_SYMLOG_TICKS)
        ax.set_yticklabels(FREQ_SYMLOG_LABELS)
        ax.set_xlabel('Tiempo')
        ax.set_xticks(linspace(0, 10081, num=7),
               DAYS, rotation=45)
        ax.grid(True)
    
    fig.tight_layout()
    fig.subplots_adjust(right=0.8)
    fig.colorbar(im, ax=axes.ravel().tolist())
    fig.savefig(name)
    return None

def compare_days(data:Data):
    # Convertir el índice a día de la semana
    data = data.data
    data['dia_semana'] = data.index.day_name()
    data['dia_semana'] = data['dia_semana'].map(map_days)

    # Agrupar por día de la semana y aplicar el promedio logarítmico
    days:DataFrame = data.groupby('dia_semana').agg(log_mean).round(1)
    return days

DAYS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
FREQ_1_1_LABEL = ['8', '16', '31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k']
FREQ_1_1_TICKS = [8, 16, 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
FREQ_SYMLOG_LABELS = ['10', '100', '1k', '10k']
FREQ_SYMLOG_TICKS = [10, 100, 1000, 10000]
FREQ_2K_LABELS = ['0', '2k', '4k', '8k', '16k']
FREQ_2K_TICKS = [0, 2000, 4000, 8000, 16000]

from enum import Enum, auto

class WeekDays_es(Enum):
    LUNES = auto()
    MARTES = auto()
    MIERCOLES = auto()
    JUEVES = auto()
    VIERNES = auto()
    SABADO = auto()
    DOMINGO = auto()

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    
    def __repr__(self):
        return self.name.capitalize()
    
    def __str__(self) -> str:
        return self.name.capitalize()

map_days = {
    'Monday': WeekDays_es.LUNES,
    'Tuesday': WeekDays_es.MARTES,
    'Wednesday': WeekDays_es.MIERCOLES,
    'Thursday': WeekDays_es.JUEVES,
    'Friday': WeekDays_es.VIERNES,
    'Saturday': WeekDays_es.SABADO,
    'Sunday': WeekDays_es.DOMINGO
    }

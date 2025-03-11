# calendar_app/enums.py
from enum import Enum

class View(Enum):
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"
    YEAR = "Year"

class Theme(Enum):
    DARK = "Dark"
    LIGHT = "Light"
    PURPLE = "Purple"
    ORANGE = "Orange"
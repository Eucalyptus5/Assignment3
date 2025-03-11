# calendar_app/calendar_factory.py
from calendar_model import Calendar

class CalendarFactory:
    @staticmethod
    def create_calendar(calendar_id: int, name: str, private: bool, time_zone):
        return Calendar(calendar_id, name, private, time_zone)
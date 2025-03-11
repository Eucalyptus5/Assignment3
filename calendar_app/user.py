# calendar_app/user.py
from ui import UI
from timezone import TimeZone
from datetime import datetime
from calendar_factory import CalendarFactory

class User:
    def __init__(self, user_id: int, user_name: str, user_email: str, ui: UI = None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.calendars = []
        self.ui = ui if ui else UI()

    def get_calendar_by_id(self, cal_id: int):
        for c in self.calendars:
            if c.calendar_id == cal_id:
                return c
        return None

    def create_calendar(self, name: str, private: bool = True):
        new_cal_id = len(self.calendars) + 1
        cal = CalendarFactory.create_calendar(new_cal_id, name, private, self.ui.time_zone)
        cal.users.append(self.user_id)
        self.calendars.append(cal)
        return cal

    def add_event_to_calendar(self, cal_id: int, name: str, start_time: datetime, end_time: datetime = None):
        cal = self.get_calendar_by_id(cal_id)
        if cal is not None:
            from .event_factory import EventFactory
            new_event_id = len(cal.events) + 1
            evt = EventFactory.create_event(new_event_id, start_time, name, self.user_id, end_time)
            cal.events.append(evt)
            return evt
        return None

    def view_event(self, cal_id: int, event_id: int):
        cal = self.get_calendar_by_id(cal_id)
        if cal is None:
            return None
        for e in cal.events:
            if e.event_id == event_id:
                if e.owned_by_user == self.user_id or self.user_name in e.shared_with_users:
                    return e
        return None

    def change_view(self, new_view):
        self.ui.change_view(new_view)

    def change_theme(self, new_theme):
        self.ui.change_theme(new_theme)

    def change_time_zone(self, offset: int):
        self.ui.change_time_zone(offset)
        for cal in self.calendars:
            cal.set_time_zone(offset)
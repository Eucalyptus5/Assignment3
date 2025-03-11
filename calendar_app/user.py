# calendar_app/user.py
from ui import UI
from calendar_model import Calendar
from timezone import TimeZone
from datetime import datetime

class User:
    """
    A user with an ID, name, email, personal UI settings, and a list of Calendars they own.
    """

    def __init__(self, user_id: int, user_name: str, user_email: str, ui: UI = None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.calendars = []
        if ui is None:
            self.ui = UI()
        else:
            self.ui = ui

    def create_calendar(self, name: str, private: bool = True):
        """
        Creates a new Calendar. The user is automatically considered an owner (added to .users).
        """
        new_cal_id = len(self.calendars) + 1
        cal = Calendar(
            calendar_id=new_cal_id,
            name=name,
            private=private,
            time_zone=self.ui.time_zone  # Use the user's current time zone
        )
        cal.users.append(self.user_id)
        self.calendars.append(cal)
        return cal

    def view_calendar(self, cal_id: int):
        """
        Return the Calendar if the user can see it, otherwise None.
        """
        for c in self.calendars:
            if c.calendar_id == cal_id:
                # The user "owns" this calendar, so we can let them view it
                return c
        # If we don't own it, we might need to handle globally stored calendars. 
        # For simplicity, we assume user only sees calendars in their list.
        return None

    def view_event(self, cal_id: int, event_id: int):
        cal = self.view_calendar(cal_id)
        if cal is None:
            return None
        for e in cal.events:
            # Check if event is viewable for this user
            if e.event_id == event_id:
                # If user is the owner or in shared list, we can see it
                if e.owned_by_user == self.user_id or self.user_name in e.shared_with_users:
                    return e
        return None

    def change_view(self, new_view):
        self.ui.change_view(new_view)

    def change_theme(self, new_theme):
        self.ui.change_theme(new_theme)

    def change_time_zone(self, offset: int):
        # Change the offset in the user's UI
        self.ui.change_time_zone(offset)
        # Optionally also change all owned calendars to match
        for cal in self.calendars:
            cal.set_time_zone(offset)

    def add_event_to_calendar(self, cal_id: int, name: str,
                              start_time: datetime,
                              end_time: datetime = None):
        cal = self.view_calendar(cal_id)
        if cal is not None:
            return cal.add_event(start_time, name, end_time, self.user_id)
        return None
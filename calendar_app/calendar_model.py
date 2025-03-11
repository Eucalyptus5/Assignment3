# calendar_app/calendar_model.py
from datetime import datetime
from event import Event
from timezone import TimeZone

class Calendar:
    """
    A user's calendar, containing events. 
    'private' indicates whether it is visible only to sharedWithUsers or publicly visible.
    """

    def __init__(self, calendar_id: int, name: str, private: bool, time_zone: TimeZone):
        self.calendar_id = calendar_id
        self.name = name
        self.private = private
        self.time_zone = time_zone

        # The UML references "privateEvents" vs. "sharedEvents" 
        # but we'll keep a single list of events and a 'shared_with_users' for the entire calendar.
        self.events = []
        self.shared_with_users = []
        # Which user(s) created or can manage this calendar
        self.users = []

    def update_time_zone(self, offset: int):
        """
        Optionally shift all events in this calendar by the offset.
        For demonstration, we'll skip actual datetime shifting.
        """
        for event in self.events:
            event.update_time_zone(offset)

    def add_event(self, start_time: datetime, name: str, end_time: datetime, owner_id: int):
        new_event_id = len(self.events) + 1
        event = Event(new_event_id, start_time, name, owner_id, end_time)
        self.events.append(event)
        return event

    def delete_event(self, event_id: int):
        self.events = [e for e in self.events if e.event_id != event_id]

    def share_calendar(self, usernames: list[str]):
        for user in usernames:
            if user not in self.shared_with_users:
                self.shared_with_users.append(user)

    def set_time_zone(self, offset: int):
        self.time_zone.set_offset(offset)
        self.update_time_zone(offset)

    def verify_user(self, username: str):
        """
        Returns 'self' if the user is allowed to see the calendar. Otherwise None.
        If the calendar is not private, anyone can see it.
        If it is private, user must be in shared_with_users or in self.users.
        """
        if not self.private:
            return self
        if username in self.shared_with_users:
            return self
        # Also, if the username is the name of one of the owners...
        # But we only stored user_id in self.users, not user_name. 
        # This is a slight simplification from the UML. 
        return None
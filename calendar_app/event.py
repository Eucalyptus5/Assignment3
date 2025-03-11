# calendar_app/event.py
from datetime import datetime

class Event:
    """
    Represents an event with start/end times, a name, an owner, and a list
    of users with whom it is shared.
    """

    def __init__(self, 
                 event_id: int,
                 start_time: datetime,
                 name: str,
                 owned_by_user: int,
                 end_time: datetime = None):
        self.event_id = event_id
        self.start_time = start_time
        # If no end_time, default 1 hour after start_time for demonstration
        if end_time is None:
            # Basic example: 1 hour from start
            self.end_time = start_time
        else:
            self.end_time = end_time

        self.name = name
        self.owned_by_user = owned_by_user
        self.shared_with_users = []  # list of user names (strings)

    def update_time_zone(self, offset: int):
        """
        Here, we could shift self.start_time and self.end_time by offset,
        or do nothing if we keep times naive. We'll just store the offset
        if needed.
        """
        pass

    def share_event(self, users: list[str]):
        """
        Add users to the event's sharedWithUsers list if not already present.
        """
        for u in users:
            if u not in self.shared_with_users:
                self.shared_with_users.append(u)

    def update(self, start_time: datetime, name: str, end_time: datetime):
        self.start_time = start_time
        self.name = name
        self.end_time = end_time

    def verify_user(self, username: str):
        """
        Return 'self' if the user can access the event, otherwise None.
        """
        if username in self.shared_with_users or username == str(self.owned_by_user):
            return self
        return None
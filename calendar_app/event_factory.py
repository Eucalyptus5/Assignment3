# calendar_app/event_factory.py
from event import Event

class EventFactory:
    @staticmethod
    def create_event(event_id: int, start_time, name: str, owner_id: int, end_time=None):
        return Event(event_id, start_time, name, owner_id, end_time)
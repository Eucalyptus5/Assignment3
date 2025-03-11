# calendar_app/timezone.py

class TimeZone:
    """
    A simple class to store time zone data such as an ID, offset, and name.
    In a real app, we might shift actual datetime objects by offset, etc.
    """
    def __init__(self, time_zone_id: int, offset: int, name: str):
        self.time_zone_id = time_zone_id
        self.offset = offset
        self.name = name

    def set_offset(self, new_offset: int):
        self.offset = new_offset
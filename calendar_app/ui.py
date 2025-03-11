# calendar_app/ui.py
from enums import View, Theme
from timezone import TimeZone

class UI:
    """
    Stores a user's chosen View, Theme, and TimeZone.
    """

    def __init__(self, 
                 user_view: View = View.DAY, 
                 theme: Theme = Theme.LIGHT, 
                 time_zone: TimeZone = None):
        self.user_view = user_view
        self.theme = theme
        if time_zone is None:
            # default timezone: ID=0, offset=0, name="UTC"
            self.time_zone = TimeZone(0, 0, "UTC")
        else:
            self.time_zone = time_zone

    def change_view(self, new_view: View):
        self.user_view = new_view

    def change_theme(self, new_theme: Theme):
        self.theme = new_theme

    def change_time_zone(self, offset: int):
        """
        Changes the offset of the current TimeZone to the given integer.
        """
        self.time_zone.set_offset(offset)
# CalendarApp (Python Version)

This is a Python implementation of a Calendar application, originally based on a UML design featuring:
- User
- Calendar
- Event
- UI (with Theme, View, and TimeZone settings)

I have extended it to provide a menu-driven terminal interface where you can create users, switch between them, create calendars, add events, share calendars, and view events — all from the console.

## Requirements

- **Python 3.9** or higher

## How to Run
Open a terminal in the root folder (the one containing the calendar_app directory) and run the following command:
python3 main.py

Usage
Once the program starts, you’ll see a menu:
===================================
No user is currently logged in.
Choose an option:
1) Create a new User
2) Switch active User
3) Create a Calendar (active user)
4) View Calendars (active user)
5) Add Event to a Calendar (active user)
6) View Events in a Calendar (active user)
7) Share a Calendar with another User (active user)
8) Change active User's UI settings (View/Theme/TimeZone)
9) Exit

Example Flow
Create a new User: (Option 1)
Switch to that user: (Option 2) by entering their user ID
Create a Calendar: (Option 3) — provide a name, select private or not
Add an Event: (Option 5) — specify calendar ID, event name, start/end times
View your Calendars: (Option 4) to see the results
Share a Calendar: (Option 7) with another user by user ID
All data is in memory only; once you exit, changes are lost.
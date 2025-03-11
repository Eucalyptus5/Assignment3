# calendar_app/main.py

from datetime import datetime, timedelta
from user import User
from enums import View, Theme
from timezone import TimeZone

def main():
    """
    A simple terminal-based menu to manage Users, Calendars, and Events.
    """
    users = {}         # dictionary: user_id -> User
    active_user = None # track which user is "logged in"
    next_user_id = 1   # auto-increment for new users

    while True:
        print("\n===================================")
        if active_user is not None:
            print(f"Currently logged in as: '{active_user.user_name}' (ID={active_user.user_id})")
        else:
            print("No user is currently logged in.")

        print("Choose an option:")
        print("1) Create a new User")
        print("2) Switch active User")
        print("3) Create a Calendar (active user)")
        print("4) View Calendars (active user)")
        print("5) Add Event to a Calendar (active user)")
        print("6) View Events in a Calendar (active user)")
        print("7) Share a Calendar with another User (active user)")
        print("8) Change active User's UI settings (View/Theme/TimeZone)")
        print("9) Exit")

        choice = input("Enter choice: ").strip()
        if choice == '1':
            # Create a new User
            name = input("Enter new user's name: ")
            email = input("Enter new user's email: ")
            user = User(user_id=next_user_id, user_name=name, user_email=email)
            users[next_user_id] = user
            print(f"User created with ID={next_user_id}")
            next_user_id += 1

        elif choice == '2':
            # Switch active user
            if not users:
                print("No users exist yet. Create a user first.")
                continue
            print("Available user IDs:")
            for uid in users:
                print(f"  {uid} -> {users[uid].user_name}")
            try:
                uid = int(input("Enter user ID to switch to: "))
                if uid in users:
                    active_user = users[uid]
                    print(f"Switched active user to '{active_user.user_name}'.")
                else:
                    print("Invalid user ID.")
            except ValueError:
                print("Invalid input.")

        elif choice == '3':
            # Create a calendar for the active user
            if active_user is None:
                print("No active user. Please switch or create a user first.")
                continue
            name = input("Enter calendar name: ")
            is_private = input("Make this calendar private? (y/n): ").lower().startswith('y')
            cal = active_user.create_calendar(name, private=is_private)
            print(f"Created calendar '{cal.name}' with ID={cal.calendar_id}")

        elif choice == '4':
            # View calendars for the active user
            if active_user is None:
                print("No active user. Please switch or create a user first.")
                continue
            if not active_user.calendars:
                print("You have no calendars.")
            else:
                print("Your calendars:")
                for c in active_user.calendars:
                    private_status = "Private" if c.private else "Public"
                    print(f"  ID={c.calendar_id}, Name='{c.name}', {private_status}")

        elif choice == '5':
            # Add an event to a calendar
            if active_user is None:
                print("No active user.")
                continue
            if not active_user.calendars:
                print("Active user has no calendars. Create one first.")
                continue
            try:
                cal_id = int(input("Enter calendar ID to add event to: "))
                cal = active_user.view_calendar(cal_id)
                if cal is None:
                    print("Could not access that calendar (not owned by this user).")
                    continue
                event_name = input("Enter event name: ")
                start_input = input("Enter start time (YYYY-MM-DD HH:MM) or press Enter for 'now': ")
                if start_input.strip() == "":
                    start_time = datetime.now()
                else:
                    start_time = datetime.strptime(start_input, "%Y-%m-%d %H:%M")
                
                end_input = input("Enter end time (YYYY-MM-DD HH:MM) or press Enter for +1 hour: ")
                if end_input.strip() == "":
                    end_time = start_time + timedelta(hours=1)
                else:
                    end_time = datetime.strptime(end_input, "%Y-%m-%d %H:%M")

                evt = active_user.add_event_to_calendar(cal_id, event_name, start_time, end_time)
                if evt is not None:
                    print(f"Event '{evt.name}' added (ID={evt.event_id}).")
                else:
                    print("Failed to create event.")
            except ValueError:
                print("Invalid input.")

        elif choice == '6':
            # View events in a calendar
            if active_user is None:
                print("No active user.")
                continue
            if not active_user.calendars:
                print("No calendars. Please create one.")
                continue
            try:
                cal_id = int(input("Enter calendar ID to view events: "))
                cal = active_user.view_calendar(cal_id)
                if cal is None:
                    print("Could not access that calendar.")
                    continue
                if not cal.events:
                    print(f"No events in calendar '{cal.name}'.")
                else:
                    print(f"Events in '{cal.name}':")
                    for e in cal.events:
                        # Check if current user can actually view it
                        # (We use user.view_event to see if we get None or the event)
                        if active_user.view_event(cal_id, e.event_id) is not None:
                            print(f"  EventID={e.event_id}, Name='{e.name}', "
                                  f"Start={e.start_time}, End={e.end_time}")
                        else:
                            print(f"  EventID={e.event_id} (not shared with you).")
            except ValueError:
                print("Invalid input.")

        elif choice == '7':
            # Share a calendar with another user
            if active_user is None:
                print("No active user.")
                continue
            if not active_user.calendars:
                print("No calendars. Please create one.")
                continue
            try:
                cal_id = int(input("Enter calendar ID to share: "))
                cal = active_user.view_calendar(cal_id)
                if cal is None:
                    print("Could not access that calendar.")
                    continue
                # Let user specify the other user's name or ID
                print("Available users to share with:")
                for uid, usr in users.items():
                    if usr != active_user:
                        print(f"  ID={uid}, Name='{usr.user_name}'")
                share_list = input("Enter comma-separated user IDs to share with: ")
                share_ids = [s.strip() for s in share_list.split(",") if s.strip()]
                share_user_names = []
                for s_id in share_ids:
                    try:
                        u_id = int(s_id)
                        if u_id in users:
                            share_user_names.append(users[u_id].user_name)
                    except ValueError:
                        pass

                if not share_user_names:
                    print("No valid user IDs found.")
                else:
                    cal.share_calendar(share_user_names)
                    print(f"Calendar '{cal.name}' shared with {share_user_names}.")
                    # Optionally also add the calendar to the other user's 'calendars' list,
                    # so they can see it in "view_calendar"
                    for su in share_user_names:
                        # find user by name
                        for usr in users.values():
                            if usr.user_name == su:
                                # only add if not already in that user's list
                                if cal not in usr.calendars:
                                    usr.calendars.append(cal)
                    print("Calendar appended to the other user's calendars for demonstration.")
            except ValueError:
                print("Invalid input.")

        elif choice == '8':
            # Change UI settings
            if active_user is None:
                print("No active user.")
                continue
            print("1) Change View (Day, Week, Month, Year)")
            print("2) Change Theme (Dark, Light, Purple, Orange)")
            print("3) Change TimeZone offset")
            c2 = input("Enter choice: ").strip()
            if c2 == '1':
                v = input("Enter new view [day/week/month/year]: ").lower()
                mapping = {
                    'day': View.DAY,
                    'week': View.WEEK,
                    'month': View.MONTH,
                    'year': View.YEAR,
                }
                if v in mapping:
                    active_user.change_view(mapping[v])
                    print(f"Changed view to {mapping[v].name}.")
                else:
                    print("Invalid view.")
            elif c2 == '2':
                t = input("Enter new theme [dark/light/purple/orange]: ").lower()
                mapping = {
                    'dark': Theme.DARK,
                    'light': Theme.LIGHT,
                    'purple': Theme.PURPLE,
                    'orange': Theme.ORANGE,
                }
                if t in mapping:
                    active_user.change_theme(mapping[t])
                    print(f"Changed theme to {mapping[t].name}.")
                else:
                    print("Invalid theme.")
            elif c2 == '3':
                try:
                    offset_str = input("Enter integer offset (e.g., -5 for UTC-5): ")
                    offset_val = int(offset_str)
                    active_user.change_time_zone(offset_val)
                    print(f"Changed time zone offset to {offset_val}.")
                except ValueError:
                    print("Invalid offset.")
            else:
                print("Invalid choice.")

        elif choice == '9':
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
# Design Changes
# 1. Pythonic Method Names

- Changed methods from `verifyUser()` to `verify_user()`, `deleteEvent()` to `delete_event()`, etc.  
- Return types differ slightly: some methods return `None` (if something fails) rather than throwing exceptions or returning new objects.

---

## 2. File and Module Organization

- Placed `Calendar` in `calendar_model.py` to avoid clashing with Python’s built-in `calendar` module.
- Created `enums.py` for `View` and `Theme`.
- Moved `TimeZone`, `UI`, `Event`, and `User` into separate files for clarity.

---

## 3. In-Memory User Management

- The UML did not specify a global store of users. To enable the console menu for user creation and switching, `main.py` maintains a dictionary of users (`users`) in memory.
- User IDs auto-increment. We prompt to switch the “active user.”

---

## 4. Calendar Sharing

- The original UML concept: “share a calendar.” In practice:
  - When a user shares a calendar with another user, we add the other user’s name to the calendar’s `shared_with_users`.
  - Additionally, we append that calendar object to the other user’s `.calendars` list so they can access it. This is an extra step not explicitly in the UML, but it allows demonstration of shared calendars in the console interface.

---

## 5. Time Zone Handling

- We store an integer offset and a name in `TimeZone`.

---

## 6. Console-Based Menu

- The UML did not specify a UI. We added `main.py` with an interactive text menu:
  1. Create users
  2. Switch active user
  3. Create/view/share calendars
  4. Add/view events
  5. Change UI settings (view, theme, time zone)

This lets us test the system in a single run without code changes each time.

---

## 7. Summary

These modifications allow for a simple, menu-driven Python application while keeping the core UML design intact (Users, Calendars, Events, UI, Themes, Views, and TimeZones).
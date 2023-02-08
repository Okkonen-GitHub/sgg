

Here is a 'simple' example

```bash
python_version = 3.11
indentation = 4
case_sensitive = false

# variables start with $
$name: What is your name traveler? -> event1

# events are created like this:
# each following event can have multiple triggers
event1: Hello $name, are you looking for something? (yes/y,no/n) -> (event2, event3)

# Prior to any event there can be a text info with a pause (user can be made hit enter to continue)
@info: Well maybe I have what you are looking for, step in
event2: Do you step into the shop? (yes/y,no/n) -> (event4, event3)


@info1: Farewell then, may our paths cross another time
event3: \quit

event4: ...
```

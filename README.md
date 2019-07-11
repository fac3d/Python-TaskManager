# Python-TaskManager
This program uses an SQLite Database to manage task completion through
a GUI. Users may enter Task ID and Description to add "Pending Tasks" which
are initialized to a completed value of 0. You may only add a task number if
it does not already exist.Users may complete or delete tasks by entering
the Task ID.

Included along with the .py files is a copy of the SQLite Database.

To begin the program, click "Display Completed Tasks" and "Display Pending Tasks" in the UI. 

---
userInterface.py:

Constructor for Class taskManager includes tkinter instance variables creating a main window,
    and a series of frames for labels, userinput, and buttons.

    Instance methods allow user to:
        Display Completed Tasks
        Display Pending Tasks
        Add task to Pending Tasks if task does not exist already
        Mark tasks as completed
        Delete tasks
---
task.py:

Class Task is defined by three instance variables: int task_id, string description, and int completed

---
db.py:

includes methods to connect to task_list_db.sqlite database on a Window's machine,
close the database connection, add a task object to the database using an SQL script,
search pending and completed tasks to see if a task already exists, return pending tasks,
add an item to completed tasks, and delete tasks

'''
Aaron LaVallee
5/5/2019

db.py: includes methods to connect to task_list_db.sqlite database on a Window's machine,
close the database connection, add a task object to the database using an SQL script,
search pending and completed tasks to see if a task already exists, return pending tasks,
add an item to completed tasks, and delete tasks

'''

import sys
import os
import sqlite3
from contextlib import closing
from TaskManager.task import Task

conn = None

def connect():
    global conn
    if not conn:
        if sys.platform == "win32":
            DB_FILE = "task_list_db.sqlite"

        else:
            HOME = os.environ["HOME"]
            DB_FILE = HOME + "task_list_db.sqlite"

        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def addTask(task):
    sql = '''INSERT INTO Task (taskID, description, completed)
             VALUES (?, ?, ?)'''

    with closing(conn.cursor()) as c:
        c.execute(sql, (task.task_id, task.description, task.completed))
        conn.commit()

def makeTask(row):
    return Task(row["taskID"], row["description"], row["completed"])

def searchPendingTask(taskID):

    query = '''SELECT * 
               FROM Task
               WHERE completed = 0 AND taskID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (taskID,))
        row = c.fetchone()
        if row:
            return makeTask(row)
        else:
            return []

def searchCompletedTasks(taskID):

    query = '''SELECT * 
               FROM Task
               WHERE completed = 1 AND taskID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (taskID,))
        row = c.fetchone()
        if row:
            return makeTask(row)
        else:
            return []

def getCompletedTasks():
    query = '''SELECT * 
               FROM Task
               WHERE completed = 1'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    completed = []
    for row in results:
        completed.append(makeTask(row))
    return completed

def getPendingTasks():
     query = '''SELECT * 
                FROM Task
                WHERE completed = 0'''
     with closing(conn.cursor()) as c:
         c.execute(query)
         results = c.fetchall()

     pending = []
     for row in results:
         pending.append(makeTask(row))
     return pending

def completeTask(task_id):

    query = '''UPDATE Task
               SET completed = 1 
               WHERE taskID = ?'''

    with closing(conn.cursor()) as c:
        c.execute(query, (task_id,))
        conn.commit()

def deleteTask(task_id):
    sql = '''DELETE FROM Task WHERE taskID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (task_id,))
        test = conn.commit()


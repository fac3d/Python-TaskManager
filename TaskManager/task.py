'''
Aaron LaVallee
5/5/2019
task.py:

Class Task is defined by three instance variables: int task_id, string description, and int completed

'''

class Task:

    def __init__(self, task_id=0, description=None, completed=0, minutes=0, category=None):
        self.task_id = task_id
        self.description = description
        self.completed = completed


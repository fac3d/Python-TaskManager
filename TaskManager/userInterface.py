'''
Aaron LaVallee
5/5/2019

This program uses an SQLite Database to manage task completion through
a GUI. Users may enter Task ID and Description to add "Pending Tasks" which
are initialized to a completed value of 0. You may only add a task number if
it does not already exist.Users may complete or delete tasks by entering
the Task ID.

Included along with the .py files is a copy of the SQLite Database.

To begin the program, click "Display Completed Tasks" and "Display Pending Tasks"

'''

from tkinter import *
import tkinter
from tkinter import scrolledtext
from TaskManager import db
from TaskManager.task import Task
import ctypes

class TaskManager:

    '''
    Constructor for Class taskManager includes tkinter instance variables creating a main window,
    and a series of frames for labels, userinput, and buttons.

    Instance methods allow user to:
        Display Completed Tasks
        Display Pending Tasks
        Add task to Pending Tasks if task does not exist already
        Mark tasks as completed
        Delete tasks
    '''

    def __init__(self):
        #main window
        self.main_window = tkinter.Tk()
        self.main_window.title("Task Manager")

        #title frame
        self.titleFrame = tkinter.Frame(self.main_window)
        #input frame
        self.frame1 = tkinter.Frame(self.main_window)
        #add button frame
        self.addButtonFrame = tkinter.Frame(self.main_window)
        #complete task Frame
        self.completeFrame = tkinter.Frame(self.main_window)
        #delete frame
        self.deleteFrame = tkinter.Frame(self.main_window)
        #display completed button frame
        self.displayCompletedFrame = tkinter.Frame(self.main_window)
        #display pending button frame
        self.displayPendingFrame = tkinter.Frame(self.main_window)
        #display frame completed
        self.displayCompletedTasks = tkinter.Frame(self.main_window)
        #display frame pending
        self.displayPendingTasks = tkinter.Frame(self.main_window)

        self.titleFrame.pack()
        self.frame1.pack()
        self.addButtonFrame.pack()
        self.completeFrame.pack()
        self.deleteFrame.pack()
        self.displayCompletedFrame.pack()

        self.displayCompletedTasks.pack()
        self.displayPendingFrame.pack()
        self.displayPendingTasks.pack()
        #self.displayPendingTasks.pack()

        #title label
        self.title = tkinter.Label(self.titleFrame, text= "Task Manager")
        self.title['font'] = ('times new roman', '16')
        self.title.pack(side= 'left')

        #input label and entry fields for complete task
        self.taskID_Label = tkinter.Label(self.frame1, text="Enter Task ID: ")
        self.taskID_Entry = tkinter.Entry(self.frame1, width = 30)
        self.description_Label = tkinter.Label(self.frame1, text="Enter Description: ")
        self.description_Entry = tkinter.Entry(self.frame1, width = 30)

        self.taskID_Label.pack(side='left')
        self.taskID_Entry.pack(side='left')
        self.description_Label.pack(side='left')
        self.description_Entry.pack(side='left')

        self.completeTaskLabel = tkinter.Label(self.completeFrame, text = "Complete by Task ID: ")
        self.completeTaskEntry = tkinter.Entry(self.completeFrame, width = 30)
        self.completeTaskLabel.pack(side='left')
        self.completeTaskEntry.pack(side='left')

        #input label, and entry for Delete
        self.taskManager_Label = tkinter.Label(self.deleteFrame, text="Delete by Task ID: ")
        self.deleteTask_Entry = tkinter.Entry(self.deleteFrame, width = 30)
        self.taskManager_Label.pack(side='left')
        self.deleteTask_Entry.pack(side='left')

        def completedTasks(): #Display Completed Tasks Button

            tasks = db.getCompletedTasks()
            self.scrollText.delete(1.0, END)
            self.scrollText.insert(END, ("Task ID \t\tDescription \t\tCompleted \n"))
            for task in tasks:

                self.scrollText.insert(END, (str(task.task_id) + " \t\t" + task.description + " \t\t" + str(task.completed) + "\n"))

        def pendingTasks(): #Display Pending Tasks Button

            tasks = db.getPendingTasks()
            self.scrollText1.delete(1.0, END)
            self.scrollText1.insert(END, ("Task ID \t\tDescription \t\tCompleted \n"))

            for task in tasks:

                self.scrollText1.insert(END, (str(task.task_id) + " \t\t" + task.description + " \t\t" + str(task.completed) + "\n"))

        def addTask():

            taskID = self.taskID_Entry.get()
            description = self.description_Entry.get()
            completed = 0

            #see if task already exists
            completedSearch = db.searchCompletedTasks(taskID)
            pendingSearch = db.searchPendingTask(taskID)

            if (completedSearch != []) or (pendingSearch != []):
                ctypes.windll.user32.MessageBoxW(0, "ID can not already exist.", "Error", 0x00000000)
            elif (taskID == ""):
                ctypes.windll.user32.MessageBoxW(0, "Task ID can not be blank. ", "Error", 0x00000000)
            elif (description == ""):
                ctypes.windll.user32.MessageBoxW(0, "Description can not be blank. ", "Error", 0x00000000)
            else:
                try:
                    task = Task(taskID, description, completed)
                    db.addTask(task)
                    completedTasks()
                    pendingTasks()

                    self.taskID_Entry.delete(0, END)
                    self.description_Entry.delete(0, END)

                except Exception as e:

                    ctypes.windll.user32.MessageBoxW(0, "Error: you may only enter numerical values for Task ID. ", "Error", 0x00000000)

        def completeTask():

            taskID = self.completeTaskEntry.get()

            pending = db.searchPendingTask(taskID)

            if (taskID == ""):
                ctypes.windll.user32.MessageBoxW(0, "Task ID can not be blank. ", "Error", 0x00000000)

            elif (pending == []):
                ctypes.windll.user32.MessageBoxW(0, "Pending task does not exist. Make sure it is a number.", "Error", 0x00000000)

            else:

                try:
                    db.completeTask(taskID)

                    completedTasks()
                    pendingTasks()

                    self.completeTaskEntry.delete(0, END)

                except Exception as e:

                    ctypes.windll.user32.MessageBoxW(0, "Error Occured. Please re-enter data. ", "Error", 0x00000000)

        def deleteTask():  #Delete Button

            #read task ID from screen
            entry = self.deleteTask_Entry.get()

            pending = db.searchPendingTask(entry)
            completed = db.searchCompletedTasks(entry)

            if (entry == ""):
                ctypes.windll.user32.MessageBoxW(0, "Task ID can not be blank. ", "Error", 0x00000000)
            elif (pending == []) and (completed == []):
                ctypes.windll.user32.MessageBoxW(0, "ID does not exist.", "Error", 0x00000000)
            else:

                try:
                    db.deleteTask(entry)

                    completedTasks()
                    pendingTasks()

                    self.deleteTask_Entry.delete(0, END)

                except Exception as e:

                    ctypes.windll.user32.MessageBoxW(0, "Error Occured. Please re-enter data. ", "Error", 0x00000000)

        self.displayCompletedButton = tkinter.Button(self.displayCompletedFrame, text='Display Completed Tasks', command = completedTasks)
        self.displayAddTaskButton = tkinter.Button(self.frame1, text='Add Task', command = addTask)
        self.displayDeleteButton = tkinter.Button(self.deleteFrame, text='Delete Task', command = deleteTask)
        self.completeButton = tkinter.Button(self.completeFrame, text = 'Complete Task', command = completeTask)

        self.displayCompletedButton.pack(side='left')
        self.displayAddTaskButton.pack(side='left')
        self.displayDeleteButton.pack(side='left')
        self.completeButton.pack(side='left')

        #Create and pack multiline text scroll widget
        self.scrollText = scrolledtext.ScrolledText(self.displayCompletedTasks, width=45,height=10)
        self.scrollText['font'] = ('times new roman', '12')
        self.scrollText.pack(side='left')

        self.displayPendingButton = tkinter.Button(self.displayPendingFrame, text='Display Pending Tasks', command = pendingTasks)
        self.displayPendingButton.pack(side='bottom') #displayCompletedTasks

        self.scrollText1 = scrolledtext.ScrolledText(self.displayPendingTasks, width=45,height=10)
        self.scrollText1['font'] = ('times new roman', '12')
        self.scrollText1.pack(side='left')

        tkinter.mainloop()

def main():
    db.connect()
    TaskManager()
    db.close()

main()

from nltk.chat.util import Chat, reflections
from flask import Flask, render_template, request
import pandas as pd
import random
import datetime
import os


app = Flask(__name__)
# As each valid task is submitted by the user, it gets added to the tasks array which will be used to display the table 
tasks = []
studentStartTime = None
studentEndTime = None
currentTask = None

# Matches the user input with the one of the responses listed in the pairs
         
taskList = [
  'essay',
  'coding',
  'notes',
  'test',
  'quiz',
  'videos'
]

taskDuration = {
  'essay': 120,
  'coding': 60,
  'notes': 45,
  'test': 60,
  'quiz': 40,
  'videos': 30
}

def setStudentStartTime(userInput):
  global studentStartTime
  studentStartTime = datetime.datetime.strptime(userInput,"%Y-%m-%d %H:%M:%S")
  return studentStartTime.strftime("%Y-%m-%d %H:%M:%S")

def removeStudentStartTime():
  global studentStartTime
  studentStartTime = None
  return "Start time removed successfully."

def setStudentEndTime(userInput):
  global studentEndTime
  studentEndTime = datetime.datetime.strptime(userInput,"%Y-%m-%d %H:%M:%S")
  return studentEndTime.strftime("%Y-%m-%d %H:%M:%S")

def removeStudentEndTime():
  global studentEndTime
  studentEndTime = None
  return "End time removed successfully."

def calculateTaskTime(task):
  global studentStartTime
  global currentTask
  taskSplit = task.split()

  if 'quiz' in taskSplit:
    taskCompletionTime = studentStartTime + datetime.timedelta(minutes=taskDuration['quiz'])
    preparation = input("How prepared are you for the quiz? (1=Not Prepared, 4=Mostly Prepared)")
    while True:
      if preparation == "1":
        taskCompletionTime += datetime.timedelta(minutes=30)
        break
      elif preparation == "2":
        taskCompletionTime += datetime.timedelta(minutes=15)
        break
      elif preparation == "3":
        taskCompletionTime
        break
      elif preparation == "4":
        taskCompletionTime -= datetime.timedelta(minutes=10)
        break
      else:
        preparation = input("How prepared are you for the quiz? (1=Not Prepared, 4=Mostly Prepared)")
    if taskCompletionTime > studentEndTime:
      taskCompletionTime = studentEndTime
      tasks.append((task, taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")))
      return "The task has been added. Since the task exceeds the end time, the completion for this task is the end time. Task completion time: " + taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")
    studentStartTime = taskCompletionTime
    currentTask = task
    tasks.append((task, taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")))
    return "The task has been added. Task completion time: " + taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")
  
  elif 'test' in taskSplit:
    taskCompletionTime = studentStartTime + datetime.timedelta(minutes=taskDuration['test'])
    preparation = input("How prepared are you for the test? (1=Not Prepared, 4=Mostly Prepared)")
    while True:
      if preparation == "1":
        taskCompletionTime += datetime.timedelta(minutes=30)
        break
      elif preparation == "2":
        taskCompletionTime += datetime.timedelta(minutes=15)
        break
      elif preparation == "3":
        taskCompletionTime
        break
      elif preparation == "4":
        taskCompletionTime -= datetime.timedelta(minutes=10)
        break
      else:
        preparation = input("How prepared are you for the test? (1=Not Prepared, 4=Mostly Prepared)")
    if taskCompletionTime > studentEndTime:
      taskCompletionTime = studentEndTime
      tasks.append((task, taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")))
      return "The task has been added. Since the task exceeds the end time, the completion for this task is the end time. Task completion time: " + taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")
    studentStartTime = taskCompletionTime
    currentTask = task
    tasks.append((task, taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")))
    return "The task has been added. Task completion time: " + taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")
      
  else:
    elementIndex = -1
    for x in range(0, len(taskSplit)):
      if taskSplit[x] in taskList:
        elementIndex = x
        break

    if elementIndex != -1:
      dueDateQuestion = input("Do you have any specific due date that the task has to be completed by? [yes/no] ")
      if dueDateQuestion == "yes":
        dueDateTime = input("What is the due date for this task? [YYYY-MM-DD HH:MM:SS]")
        convertedDueDate = datetime.datetime.strptime(dueDateTime,"%Y-%m-%d %H:%M:%S")
      taskCompletionTime = studentStartTime + datetime.timedelta(minutes=taskDuration[taskSplit[elementIndex]])
      if taskCompletionTime > convertedDueDate:
          return "The task cannot be added as it is exceeds the due date."
      if taskCompletionTime > studentEndTime:
        taskCompletionTime = studentEndTime
        tasks.append((task, taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")))
        return "The task has been added. Since the task exceeds the end time, the completion for this task is the end time. Task completion time: " + taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")
      
      studentStartTime = taskCompletionTime
      currentTask = task
      tasks.append((task, taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")))
      return "The task has been added. Task completion time: " + taskCompletionTime.strftime("%Y-%m-%d %H:%M:%S")
    else:
      return "The task you entered cannot be found. Supported tasks are:\n\n" + '\n'.join(f'- {task}' for task in taskDuration.keys())

def displayTaskTable():
  df = pd.DataFrame(tasks, columns=['Task', 'Completion Time'])
  return df.to_html(index=False)

class SchedulerChatbot(Chat):
  def respond(self, str):
    for (pattern, response) in self._pairs:
      match = pattern.match(str)
      if match:
        resp = random.choice(response)
        if callable(resp):
          return resp(*match.groups())
        else:
          return resp
             

pairs = [
     [
        r"Hello|Hi|Howdy|Hey",
        ["Hello!", "Hi!", "How are you today?", "Nice to meet you!"]
    ],
       [
        r"Bye|Quit|See you tommorow|That's all the help I need",
        ["It was my pleasure helping you today!", "Have a great day!", "Bye! See you later!"]
    ],
   [
        r"add task (.*)",
        [lambda userInput: calculateTaskTime(userInput) if (studentStartTime != None and studentEndTime != None) else "Please tell me when you will be working on your tasks.\nStart Time: " + str(studentStartTime) + " | End Time: " + str(studentEndTime)]
    ],
    [
        r"set start time (.*)",
        [lambda userInput: "You will begin your tasks at " + setStudentStartTime(userInput) if not studentStartTime else "Start time is already set."] # Prompts the user to set a start time if they try to add a task before setting it
    ],
    [
        r"remove start time",
        [lambda: removeStudentStartTime() if studentStartTime != None else "Start time is not yet set."] # Removes the currently set start time, if existing
    ],
    [
        r"set end time (.*)",
        [lambda userInput: "You will end your tasks at " + setStudentEndTime(userInput) if not studentEndTime else "End time is already set."] # Prompts the user to set a start time if they try to add a task before setting it
    ],
    [
        r"remove end time",
        [lambda: removeStudentEndTime() if studentEndTime != None else "End time is not yet set."] # Removes the currently set end time, if existing
    ],
    [
        r"display tasks",
        [lambda: "Here are your tasks that you need to complete:\n" + displayTaskTable() if not len(tasks) == 0 else "No tasks to display."] # Prints all tasks unless the user has not yet added tasks
    ],
    
]
chat = SchedulerChatbot(pairs, reflections)

@app.route("/")
def landing():
    return render_template("chatbot.html")

@app.route("/get")
def get_chatbot_response():
    displayResponse = request.args.get('msg')
    return str(chat.respond(displayResponse))

if __name__ == '__main__':
      app.run()

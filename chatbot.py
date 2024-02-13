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
currentTask = None

# Matches the user input with the one of the responses listed in the pairs

         
taskDuration= {
  'English essay': 120,
  'coding assignment': 60,
  'class notes': 45,
  'study for test': 60,
  'watch Heimler videos': 30
}

def setStudentStartTime(userInput):
  global studentStartTime
  studentStartTime = datetime.datetime.strptime(userInput,"%Y-%m-%d %H:%M:%S")
  return studentStartTime.strftime("%Y-%m-%d %H:%M:%S")

def calculateTaskTime(task):
  global studentStartTime
  global currentTask
  if task in taskDuration:
    taskCompletionTime = studentStartTime + datetime.timedelta(minutes=taskDuration[task])
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
        ["Hello", "How are you today?", "Nice to meet you!"]
    ],
       [
        r"Bye|Quit|See you tommorow|That's all the help I need",
        ["It was my pleasure helping you today!", "Have a great day!", "Bye. See you later."]
    ],
   [
        r"add task (.*)",
        [lambda userInput: calculateTaskTime(userInput) if studentStartTime else "Please tell me when you will start working on your tasks."]
    ],
    [
        r"set start time (.*)",
        [lambda userInput: "You will begin your tasks at " + setStudentStartTime(userInput) if not studentStartTime else "Start time is already set."] # Prompts the user to set a start time if they try to add a task before setting it
    ],
    [
        r"display tasks",
        [lambda: "Here are your tasks that you need to complete:\n" + displayTaskTable()]
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
      print("About to run...")
      port = int(os.environ.get('VAPOR_LOCAL_PORT', 5000)) 
      host = os.environ.get('VAPOR_LOCAL_HOST', "127.0.0.1")
      print("About to run with port ", port, " and host ", host)
      app.run(port=port, host=host)

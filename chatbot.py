from chatterbot import ChatBot
import re

bot = ChatBot('Scheduler Chatbot') 

bot = ChatBot(
    'Scheduler Chatbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
)

from chatterbot.trainers import ListTrainer

trainer = ListTrainer(bot)

trainer.train([
'Hello! How are you today?',
'What describes your visit today?',
'How may I help you today?',
'Are you a student?'
])

name=input("Enter Your Name: ")
print("Welcome to the Scheduler Bot Service! Let me know how can I help you?")
def chatbot_response(request):
  requestResponse = ('Sorry, I have not learned how to respond to your request.')
  if re.search(r'\b(student|homework|school)\b', request, re.IGNORECASE):
    requestResponse = 1
  elif re.search(r'\b(work|office|meeting|meetings)\b', request, re.IGNORECASE):
    requestResponse = 2
  return requestResponse

def request_school_response():
  print( 'Ok. I understand that you need help with organzation related to school.' )
  schoolEnd = input("When does your school end? ")

  
while True:
  request=input(name+':')
  if request=='Bye' or request =='bye':
    print('Bot: Bye')
    break
  response = chatbot_response(request)
  if response == 1:
    request_school_response()
  
 
    
    


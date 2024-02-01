import numpy as np
import re

class ChatBot():
    def __init__(self, name):
        print("----- starting up", name, "-----")
        self.name = name
if __name__ == "__main__":
    ai = ChatBot(name="Scheduler Chatbot")
    
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
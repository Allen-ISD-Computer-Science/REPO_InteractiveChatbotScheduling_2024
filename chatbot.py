from chatterbot import ChatBot

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
while True:
    request=input(name+':')
    if request=='Bye' or request =='bye':
        print('Bot: Bye')
        break
    else:
        response=bot.get_response(request)
        print('Scheduler Chatbot:',response)
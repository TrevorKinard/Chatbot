from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

#Introduction
print("\tWelcome to the Murphy Chatbot cult! This Chatbot is a prototype for the generational cult\n"
      "civilization that is currently in production. This Chatbot greets the user with a basic conversation\n"
      "set based around its cult of Murphy. This conversation set is the Bot's basic means of debating.\n"
      "\nTo begin, simply say Hello when training is finished!\n")
# Create Chatbot
saintBot = ChatBot('Big Ted - Pure Murpholicism')
# Create Trainer
trainer = ListTrainer(saintBot)
# Train Chatbot on text in files
for _file in os.listdir('Conversations'):
    knowledge = open('Conversations/' + _file, 'r').readlines()
    trainer.train(knowledge)

# Loop Sentinel
sentinel = True

# Conversation Loop
while sentinel:
    # Grab User input
    request = input('User: ')
    # Have the chatbot respond to the user statement
    response = saintBot.get_response(request)

    # Exit Conditions
    if request == "Dismantle Murphy" or request == "I don't believe in Murphy." or request == "Goodbye" or request == "So long.":
        sentinel = False

    #Print Chatbot's response
    print('Saint Bot: ', response)
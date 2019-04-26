"""
    This file defines the chatbot backend of the program
"""

# Import necessary files
from chatterbot.trainers import ListTrainer  # method to train chatbot
from chatterbot import ChatBot  # pretty obvious what this is doing
import os
from random import choice

# A list of names for naming the bots
names = ["Ted", "Graham", "John", "Terry", "Eric", "Michael", "Jimenez", "Biggles", "Fang", "Monty",
             "Merle", "Denzel", "Ryan", "Dana", "Trevor", "Brandon", "Zack", "Cletus", "Isabelle", "Shannon",
             "Faith", "Duncan", "Mike", "Bonnie", "Nadeem", "Jasmine", "Roberto", "Emily", "Yuvraj", "Roxanne",
             "Nikita", "Connor", "Gia", "Tomas", "Scarlett", "Diego", "Sofia", "Nikolas", "Billie", "Vladimir",
             "Atlas", "Deep", "River", "Frances", "Max", "Allegra", "Markus", "Lindsay", "Arjan", "Lina",
             "Yosef", "Shea", "Nazir", "Rae", "Alexander", "Hashim", "Kris", "Chester", "Morgan", "Finn",
            "Edgar", "Gwen", "Alan", "Leona", "Enrique", "Annabel", "Louis", "Alma", "Oscar", "Reuben"]

# The different groups the bots can be in
groups = ["Inquisitor", "Cleric", "Zealot", "Open_Minded"]


class ChatBotFactory():
    # Initialize the bot
    def __init__(self):
        self.name = choice(names) # Grab a random name
        self.bot = ChatBot(self.name, tie_breaking_method="random_response")  # Create a chatbot
        self.trainer = ListTrainer(self.bot)  # set trainer of the bot to lists, and train sequentially on them
        self.group = choice(groups) # Grab a random group
        self.files = os.listdir('Conversations') # Get all the files we can train off of

        # for each file in the directory named 'Conversations' read each line and train the chatbot on it.
        for _file in self.files:
            chats = open('Conversations/' + _file, 'r').readlines()
            self.trainer.train(chats)

        # Train the bot based on the group it is in
        chats = open('Conversations/' + self.group + '.txt', 'r').readlines()
        self.trainer.train(chats)

    def __repr__(self):
        return self.group

    def __str__(self):
        return self.group

    # Get a response for the given input
    def response(self, saying):
        return self.bot.get_response(saying)

    # Generate a random response from the three main files
    def random_response(self):
        rand_file = choice(self.files[:3]) # Get the first three files for training
        lines_list = open('Conversations/' + rand_file, 'r').readlines() # Read the lines from that file
        lines_list = [x.strip() for x in lines_list] # Cut out white space
        return choice(lines_list) # Return the random input

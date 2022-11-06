#####################
# Python Chatbot to record coffees consumed on a shared machine
# Integrates with Mattermost Messenger (https://mattermost.com) and uses the Mattermost Web Services API (https://api.mattermost.com)
# Uses the framework provided by mmpy-bot (https://pypi.org/project/mmpy-bot/)
# needs installation of mmpy-bot via pip install mmpy-bot

import re
import os

from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to
from mmpy_bot.utils import allowed_users
from mmpy_bot.utils import allowed_channels


def check_coffee_file(filename):
    if not os.path.exists(filename):
        open(filename, 'w').close()
        return False
    return True


def read_coffees(filename):
    if check_coffee_file(filename):
        file = open(filename, "r")
        lines = file.read().splitlines()
        current_coffees = lines[-1]
        file.close()
    else:
        current_coffees = 0
    return current_coffees


def write_coffees(filename, new_coffees):
    file = open(filename, "a")
    file.write(str(new_coffees))
    file.write('\n')
    file.close()


@listen_to('(.*)')
@allowed_channels('coffee')
def count(message, something):
    if something.isnumeric():
        coffees = int(something)
        coffee_counter = int(read_coffees('coffees.txt'))
        coffee_counter += coffees
        write_coffees('coffees.txt', coffee_counter)
        message.reply('I recorded %s :coffee: for you' %str(coffees))
    else:
        message.reply('Please give me a number')



@respond_to('Reset counter', re.IGNORECASE)
@allowed_users('michael_denner','martisoldini','titus.neupert')
def reset(message):
    coffee_counter = int(read_coffees('coffees.txt'))
    message.reply('Counter reset at %s coffees'%str(coffee_counter))
    coffee_counter = 0
    write_coffees('coffees.txt', coffee_counter)


@respond_to('Get number of coffees', re.IGNORECASE)
@allowed_users('michael_denner','martisoldini','titus.neupert')
def printcoffees(message):
    coffee_counter = int(read_coffees('coffees.txt'))
    message.reply('Counter at %s :coffee:'%str(coffee_counter))


@respond_to('Are you awake?', re.IGNORECASE)
@allowed_users('michael_denner','martisoldini','titus.neupert')
def respond(message):
    message.reply('I am up and running!')

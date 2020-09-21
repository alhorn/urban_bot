from room import Room
from telebot import types
import math
import config
import sqlite3
import statistic

def render_invite_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    item1 = types.InlineKeyboardButton('Join', callback_data = 'joined')
    item2 = types.InlineKeyboardButton('Begin', callback_data = 'begined')
    keyboard.add(item1, item2)
    return keyboard

def render_send_invite_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width = 1)
    item1 = types.InlineKeyboardButton('▶️ Play the game', switch_inline_query = '')
    keyboard.add(item1)
    return keyboard

def get_info_text():
    text = """
Created in the K&K STUDENTS community

Idea: *@karozas*
Creator: *@alhorn*

© K&K TEAM
Website: kandk.team
Contact: students@kandk.team
    """
    return text

def render_invite(room):
    text = '*Now Joined:*\n'

    for r in room.users:
        if r.last_name != None:
            text += '{} {}\n'.format(r.first_name, r.last_name)
        else:
            text += '{}\n'.format(r.first_name)

    if len(room.users) == 0:
        text = "Press *'Join'*"

    return (text, render_invite_keyboard())


def render_result(room):
    room.is_correct_answer()

    text = '*Total Results:*\n'

    top_dict = dict()
    top_list = list()

    for r in room.users:
        statistic.stat_insert([r.id, 1, room.user_score.get(r.id), config.question_number - room.user_score.get(r.id)])
        if r.last_name != None:
            top_dict['{} {}'.format(r.first_name, r.last_name)] = room.user_score.get(r.id)
        else:
            top_dict['{}'.format(r.first_name)] = room.user_score.get(r.id)

    top_list = list(top_dict.items())
    top_list.sort(key=lambda i: i[1])
    top_list.reverse()
    top_dict = dict(top_list)

    if len(top_list) > 1:

        max_result = 0
        for i in range(len(top_list)):
            if top_list[i][1] > max_result:
                max_result = top_list[i][1]

        for i in range(len(top_list)):
            if top_list[i][1] == max_result:
                top_dict[top_list[i][0]] = str(top_list[i][1]) + ' 🏆'
            else:
                top_dict[top_list[i][0]] = str(top_list[i][1])

    else:
        top_dict[top_list[0][0]] = str(top_list[0][1]) + ' 🏆'

    for i in top_dict:
        text += '_{}_ - *{}*\n'.format(i, top_dict.get(i))


    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    item1 = types.InlineKeyboardButton('Start new game 🔄', switch_inline_query_current_chat = '')
    item2 = types.InlineKeyboardButton('To bot pm 👾', url = 'https://telegram.me/Urban_DictBot')
    keyboard.add(item1, item2)
    return (text, keyboard)



def render_question(room): 
    question = room.get_current_question()
    text = ''
    text += 'What is a *"{}"*?_({}/{})_\n\n'.format(question.word, room.current_question + 1, config.question_number)

    i = 1
    for op in question.options:
        text += '*{}.* {}\n\n'.format(i, op[0])
        i += 1
    if room.time_left() < 3:
        text += "*Next round*➡️\n\n"
    elif room.time_left() < 10:
        text += "_Less than 10 seconds left_\n\n"
    elif room.time_left() < 20:
        text += "_Less than 20 seconds left_\n\n"
    else:
        text += "_Waiting for answers from all players_\n\n"


    for r in room.users:
        if r.id in room.answers[room.current_question]:
            if room.is_current_answer_correct(r) == True:
                if r.last_name != None:
                    text += '{} {} {}\n'.format(r.first_name, r.last_name, '✅')
                else:
                    text += '{} - {}\n'.format(r.first_name, '✅')
            else:
                if r.last_name != None:
                    text += '{} {} {}\n'.format(r.first_name, r.last_name, '❎')
                else:
                    text += '{} - {}\n'.format(r.first_name, '❎')                   
        else:
            if r.last_name != None:
                text += '{} {} {}\n'.format(r.first_name, r.last_name, '⏳')
            else:
                text += '{} - {}\n'.format(r.first_name, '⏳')

    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    item1 = types.InlineKeyboardButton('1️⃣', callback_data = 'answer_1')
    item2 = types.InlineKeyboardButton('2️⃣', callback_data = 'answer_2')
    item3 = types.InlineKeyboardButton('3️⃣', callback_data = 'answer_3')
    item4 = types.InlineKeyboardButton('4️⃣', callback_data = 'answer_4')
    keyboard.add(item1, item2, item3, item4)

    return (text, keyboard)

def render_room(room):
    if room.is_ended():
        return render_result(room)
    elif not room.started:
        return render_invite(room)
    else:
        return render_question(room)
from room import Room
from telebot import types

def render_invite_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    item1 = types.InlineKeyboardButton('Join', callback_data = 'joined')
    item2 = types.InlineKeyboardButton('Begin', callback_data = 'begined')
    keyboard.add(item1, item2)
    return keyboard

def render_invite(room):
    text = ''

    for r in room.users:
        if r.last_name != None:
            text += '{} {}\n'.format(r.first_name, r.last_name)
        else:
            text += '{}\n'.format(r.first_name)

    if len(room.users) == 0:
        text = "----"

    return (text, render_invite_keyboard())


def render_result(room):
    room.is_correct_answer()
    text = ''
    i = 0
    for r in room.users:
        if r.last_name != None:
            text += '{} {} - {}\n'.format(r.first_name, r.last_name, room.user_score.get(r.id))
        else:
            text += '{} - {}\n'.format(r.first_name, room.user_score.get(r.id))           
        i += 1

    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    item1 = types.InlineKeyboardButton('a', callback_data = '1')
    item2 = types.InlineKeyboardButton('b', callback_data = '2')

    keyboard.add(item1, item2)
    return (text, keyboard)

def render_question(room):
    question = room.get_current_question()
    text = ''
    text += '{}. What is a "{}"?\n'.format(room.current_question + 1 ,question.word)

    i = 1
    for op in question.options:
        text += '{} -> {}\n'.format(i, op[0])
        i += 1


    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    item1 = types.InlineKeyboardButton('1', callback_data = '1')
    item2 = types.InlineKeyboardButton('2', callback_data = '2')
    item3 = types.InlineKeyboardButton('3', callback_data = '3')
    item4 = types.InlineKeyboardButton('4', callback_data = '4')
    keyboard.add(item1, item2, item3, item4)

    return (text, keyboard)

def render_room(room):
    if room.is_ended():
        return render_result(room)
    elif not room.started:
        return render_invite(room)
    else:
        return render_question(room)
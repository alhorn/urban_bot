import config
from room import Room
import telebot
from telebot import types
import requests
import roomview
from question import Question
import defmode
from threading import Timer
import statistic

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['start'])
def welcome(message):
    bot.send_message(message.chat.id,'To start the game, write @Urban_DictBot in any chat and click on the "start" button ', reply_markup = None)

@bot.message_handler(commands = ['stats'])
def statistics(message):
    bot.send_message(message.chat.id, statistic.get_stats(message) , reply_markup = None)


@bot.message_handler(content_types = ['text'])
def send_mes(message):
    bot.send_message(message.chat.id, "Please, use inline message via @Urban_DictBot")

@bot.inline_handler(lambda query: query)
def query_text(inline_query):

    if len(inline_query.query) == 0:
        r = types.InlineQueryResultArticle(
            "1",
            "Start",
            types.InputTextMessageContent("Press 'Join'"),
            reply_markup = roomview.render_invite_keyboard()
        )
        bot.answer_inline_query(inline_query.id, [r])


    elif len(inline_query.query) > 0:
        defins = defmode.get_def(inline_query.query)
        if len(defins) > 0:
            cut_defins = defmode.get_cut_def(defins)
            params = defmode.get_params(defins, cut_defins, inline_query)
            bot.answer_inline_query(inline_query.id, params)
        
        else:
            r = types.InlineQueryResultArticle(
            "1",
            "Word is not found",
            types.InputTextMessageContent('{} trying to find {}'.format(inline_query.from_user.first_name, inline_query.query)),
            reply_markup = None
            )
            bot.answer_inline_query(inline_query.id, [r])

rooms = dict() #ROOM LIST CREATING#

def get_room_or_create(inline_message_id):
    if inline_message_id in rooms:
        return rooms[inline_message_id]
    else:
        questions = []
        for i in range(config.question_number):
            q = Question()
            q.get_questions()
            questions.append(q)

        def update_handler(room):
            try:
                text, keyboard = roomview.render_room(room)
                bot.edit_message_text(inline_message_id = inline_message_id, text = text, reply_markup = keyboard, parse_mode = "Markdown")
            except:
                pass
        rooms[inline_message_id] = Room( questions, update_handler )
        return rooms[inline_message_id]


@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):  
#####################         INLINE         ##################################
        if call.inline_message_id:
            room = get_room_or_create(call.inline_message_id)

            text, keyboard = None, None     
           
            if call.data == 'joined':
                if not room.is_user_player(call.from_user):
                    room.add_user(call.from_user)
                    text, keyboard = roomview.render_room(room)

            elif call.data == 'begined':
                if room.is_user_player(call.from_user):
                    room.start_game()
                    text, keyboard = roomview.render_room(room)

            elif call.data.startswith("answer_"):
                answer_val = call.data.split("_")[1]
                if not call.from_user.id in room.answers[room.current_question]:   
                    room.add_user_answer(call.from_user, answer_val)
                    text, keyboard = roomview.render_room(room)
                # if room.is_all_answer():
                #     room.next_question()
                #     text, keyboard = roomview.render_room(room)
                room.is_all_answer()

            if text != None:
                bot.edit_message_text(inline_message_id = call.inline_message_id, text = text, reply_markup = keyboard, parse_mode = "Markdown")

bot.polling(none_stop=True)
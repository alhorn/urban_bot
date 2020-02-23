import config
from room import Room
import telebot
from telebot import types
import requests
import random
import sqlite3
import roomview
from question import Question

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Start game", callback_data ="start")
    markup.add(item1)
    bot.send_message(message.chat.id,'Welcome', reply_markup = markup)


@bot.inline_handler(lambda query: query)
def query_text(inline_query):
    r = types.InlineQueryResultArticle(
        "1",
        "Start",
        types.InputTextMessageContent("-----"),
        reply_markup = roomview.render_invite_keyboard()
    )
    bot.answer_inline_query(inline_query.id, [r])


rooms = dict()

def get_room_or_create(inline_message_id):
    if inline_message_id in rooms:
        return rooms[inline_message_id]
    else:
        questions = []
        for i in range(10):
            q = Question()
            q.get_questions()
            questions.append(q)
        rooms[inline_message_id] = Room( questions )
        return rooms[inline_message_id]

############################        DB         ############################# 



@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):



    # try:
#######################        NORMAL        #################################      
        # if call.message:
        #     conn = sqlite3.connect("urban_db.db")
        #     cursor = conn.cursor()

        #     def get_key():
        #         cursor.execute("SELECT rowid, word, word_def from Words ORDER BY RANDOM() LIMIT 1") 
        #         key_word = cursor.fetchall()
        #         return key_word

        #     def get_rand_def(key):
        #         cursor.execute("SELECT word_def from Words where rowid != {} ORDER BY RANDOM() LIMIT 3".format(str(key[0][0]))) 
        #         rnd_def = cursor.fetchall()
        #         rnd_def.append([key[0][2]])
        #         random.shuffle(rnd_def)
        #         return rnd_def

        #     if call.data == "start":
        #         key_word = get_key()
        #         rand_def = get_rand_def(key_word)
        #         msg_text = 'What is "{}"?\n'.format(key_word[0][1])
        #         for i in range(len(rand_def)):
        #             msg_text += '{} --> {}\n'.format(i+1,rand_def[i][0])
        #         bot.send_message(call.message.chat.id, msg_text, reply_markup = keyboard4k())
           
        #     elif call.data == "1":
        #         bot.edit_message_text(chat_id = call.message.chat.id, message_id= call.message.message_id,
        #         text = "Hello", reply_markup = keyboard4k())

        #     elif call.data == "2":
        #         bot.edit_message_text(chat_id = call.message.chat.id, message_id= call.message.message_id,
        #         text = "Hello", reply_markup = keyboard4k())       

        #     elif call.data == "3":
        #         bot.edit_message_text(chat_id = call.message.chat.id, message_id= call.message.message_id,
        #         text = "Hello", reply_markup = keyboard4k())  

        #     elif call.data == "4":
        #         bot.edit_message_text(chat_id = call.message.chat.id, message_id= call.message.message_id,
        #         text = "Hello", reply_markup = keyboard4k())    

#####################         INLINE         ##################################
        if call.inline_message_id:
            room = get_room_or_create(call.inline_message_id)

            text, keyboard = None, None     
           
            if call.data == 'joined':
                if not room.is_user_player(call.from_user):
                    room.add_user(call.from_user)
                    text, keyboard = roomview.render_room(room)

            elif call.data == 'begined':
                room.start_game()
                text, keyboard = roomview.render_room(room)

            elif call.data == "1":   
                room.add_user_answer(call.from_user, call.data)
                if room.is_all_answer():
                    text, keyboard = roomview.render_room(room)

            elif call.data == "2":
                room.add_user_answer(call.from_user, call.data)                                      
                if room.is_all_answer():
                    text, keyboard = roomview.render_room(room)

            elif call.data == "3":
                room.add_user_answer(call.from_user, call.data)                                      
                if room.is_all_answer():
                    text, keyboard = roomview.render_room(room)

            elif call.data == "4":
                room.add_user_answer(call.from_user, call.data)                                      
                if room.is_all_answer():
                    text, keyboard = roomview.render_room(room)

            if text != None:
                bot.edit_message_text(inline_message_id = call.inline_message_id, text = text, reply_markup = keyboard)

    # except Exception as e:
    #     print(repr(e))


bot.polling(none_stop=True)
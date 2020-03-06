import json
import requests
import telebot
from telebot import types

def get_def(word):
    
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    headers = {
                'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
                'x-rapidapi-key': "1881a80cbbmshf588b65a4687f44p128daajsn88de22ed7a29"
            }

    querystring = {"term": word}
    response = requests.request("GET", url, headers=headers, params=querystring)
    st = json.loads(response.text)
    defin = []
    repl = ('[', ']', '\r', '\n' , '\'')
    for s in st["list"]:
        d = str(s['definition']) 
        for r in repl:        
            d =  d.replace(r , '')
        defin.append(d)
    return(defin)

def get_cut_def(defin):
    cut_def = []
    for d in defin:
        if len(d) > 40:
            d = '{}...'.format(d[0:39:1])
        cut_def.append(d)    
    return cut_def

def get_params(defin, cut_def, inline_query):
    params = []
    for i in range(len(defin)):
        params.append(types.InlineQueryResultArticle(
                "{}".format(i),
                '{}\n'.format(cut_def[i]),
                types.InputTextMessageContent('{} — {}'.format(inline_query.query, defin[i])),
                reply_markup = None
                ))
        if len(params) == 5:
            break
    return params
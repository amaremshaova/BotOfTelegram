# -*- coding: utf-8 -*-

import config
import telebot
from BD_TVprogram import work_with_BaseData
import BD
import work_with_BD

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['searchTV'])

def searchTV(message): 
    nameTV = []
    session = BD.create_table()
    bot.send_message(message.chat.id, 'Какой канал Вас интересует?')

    flag_writing_to_BD = False
    flag_search_in_BD = True

    if flag_writing_to_BD==True:
    	work_with_BD.writing_to_BD(session)

    if flag_search_in_BD==True:
    	work_with_BD.search_in_BD(session, message.text, nameTV)
    	
    bot.send_message(message.chat.id, nameTV[0])
    nameTV.pop(0)

if __name__ == '__main__':

    bot.polling(none_stop=True)



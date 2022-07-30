from email import message
import telebot
import config
import requests

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    s = open('welcomesticker.webp', 'rb')
    bot.send_sticker(message.chat.id, s)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    weatherb = types.KeyboardButton('Show me the weather!')
    markup.add(weatherb)
    bot.send_message(message.chat.id, "Hi, {0.first_name}\nWant to know the weather?".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text', 'location'])
def reply(message):
    if message.chat.type == 'private':
        if message.text == 'Show me the weather!':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            locationb = types.KeyboardButton('send current location', request_location=True,)
            typeb = types.KeyboardButton('type in manually')
            markup.add(locationb, typeb)
            bot.send_message(message.chat.id, 'Okay, where?', reply_markup=markup)
        elif message.text == 'type in manually':
            bot.send_message(message.chat.id, 'Go ahead. \nDont forget to reply to message above.')
            types.ReplyKeyboardRemove()
        elif message.location != None:
            resp = requests.get("https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&units=metric&appid={2}".format(
                message.location.latitude, 
                message.location.longitude, 
                config.WEATHERAPI,
            ))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            locationb = types.KeyboardButton('send current location', request_location=True,)
            typeb = types.KeyboardButton('type in manually')
            markup.add(locationb, typeb)
            if resp.ok:
                bot.send_message(message.chat.id, 'Aight, here you go:')
                bot.send_message(message.chat.id, '{0} °C'.format(resp.json()['main']['temp']))
            else: bot.send_message(message.chat.id, 'Couldn\'t find the weather here') 
            bot.send_message(message.chat.id, 'Something else i can do?', reply_markup=markup)
        elif message.text != '':
            print(message.location)
            resp = requests.get("https://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid={1}".format(
                message.text.lower(),
                config.WEATHERAPI,
            ))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            locationb = types.KeyboardButton('send current location', request_location=True,)
            typeb = types.KeyboardButton('type in manually')
            markup.add(locationb, typeb)
            if resp.ok:
                bot.send_message(message.chat.id, 'Aight, here you go:')
                bot.send_message(message.chat.id, "{0} °C".format(resp.json()['main']['temp']))
            else: bot.send_message(message.chat.id, 'Couldn\'t find a city with this name')
            bot.send_message(message.chat.id, 'Something else i can do?', reply_markup=markup)

@bot.callback_query_handler(func = lambda call: True)
def reply(call):
    if call.data == 'type':
        bot.send_message(call.message.chat.id, 'Go ahead. \nDont forget to reply to message above.')
        types.ReplyKeyboardRemove()
    elif call.data == 'send':
        print('ey')
        print(call.message.location)
        # print(call.message.location.longitude)


bot.polling(non_stop=True) 
import os

import telebot
from telebot import types

from service import MapService

bot = telebot.TeleBot(os.environ.get('TG_TOKEN'))

service = MapService()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        '''Добро пожаловать.\nОтправьте своё местоположение или наберите /city и введите город вручную
        ''',
        reply_markup=keyboard())


def keyboard():
    keyboard_ = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard_.add(button_geo)
    return keyboard_


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        location_ = {
            'latitude': message.location.latitude,
            'longitude': message.location.longitude
        }
        try:
            output = service.get_places_nearby(**location_)
            if output:
                tmpstring = ""
                for idx, item in enumerate(output, 1):
                    tmpstring += f"{idx}. *{item['name']}*\n _Адрес_: {item['address']}\n _Рейтинг_: {item['rating']}\n"
                    tmpstring += "\n"
                tmpstring += "рейтинг основан на оценке пользователей Google"
                bot.send_message(message.chat.id, tmpstring, parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, 'Поиск не принес результата.\nПопробуйте изменить запрос.')
        except Exception:
            bot.send_message(message.chat.id, 'Что-то пошло не так. Попробуйте снова.')


@bot.message_handler(commands=['city'])
def send_welcome(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Введите название города:", reply_markup=markup)


@bot.message_handler(content_types='text')
def city_reply(message):
    if message.text:
        try:
            output = service.get_city_restaurants(message.text)
            if output:
                tmpstring = ""
                for idx, item in enumerate(output, 1):
                    print(item)
                    tmpstring += f"{idx}. *{item['name']}*\n _Адрес_: [{item['address']}]({item['map']})\n" \
                                 f" _Рейтинг_: {item['rating']}\n" \
                                 f"_Сайт_: {item['website'] or 'Нет информации'}\n"
                tmpstring += "\n\n"
                tmpstring += "рейтинг основан на оценке пользователей Google"
                bot.send_message(message.chat.id, tmpstring, parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, 'Поиск не принес результата.\nПопробуйте изменить запрос.')
        except Exception:
            bot.send_message(message.chat.id, 'Что-то пошло не так. Попробуйте снова.')


bot.polling()
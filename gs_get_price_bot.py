import telebot
import requests
from bs4 import BeautifulSoup
from vars import API_KEY, URL, FILE_ID

bot = telebot.TeleBot(API_KEY)
file_id = FILE_ID
say_hello = """
Добро пожаловать!
Я телеграм-бот компании Генснаб!
Я могу найти для вас цену и фото товара.
Просто введите ваш запрос.
Например: Перфоратор 800 Вт
"""


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.from_user.id, say_hello)


@bot.message_handler(commands=['help'])
def welcome_message(message):
    bot.send_message(message.from_user.id, 'Просто укажите что хотите найти.')


@bot.message_handler(content_types=['text', 'document', 'photo'])
def get_text_messages(message):
    try:
        with open('log.txt', 'a', encoding="utf-8") as log_text:
            log_text.write('<User request>: ' + message.text + ' \n')
        url = URL + message.text
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='html.parser')
        price = soup.find_all('div', class_='price')
        name = soup.find_all('div', class_='title mt_ten mb_ten')
        if name == [] or price == []:
            bot.send_photo(message.from_user.id, file_id)
            bot.send_message(
                message.from_user.id,
                'Сожалеем, но ничего не найдено. \nПопробуйте сформулировать запрос точнее')
        else:
            for n, p in zip(name, price):
                n.text.strip()
                p.text.strip()
                bot.send_message(
                    message.from_user.id,
                    '{} \n - цена - \n {}'.format(n.text, p.text))
        bot.send_message(message.from_user.id, 'Всё!')
    except:
        with open('log.txt', 'a', encoding="utf-8") as log_text:
            log_text.write(f'Что пришло: {message.text}.')
        bot.send_photo(message.from_user.id, file_id)
        bot.send_message(
            message.from_user.id,
            'Что-то пошло не так, попробуйте ещё раз')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    bot.send_photo(message.from_user.id, file_id)
    bot.send_message(
        message.from_user.id,
        'Сожалеем, но ничего не найдено. \nПопробуйте сформулировать запрос точнее')


bot.polling(none_stop=True, interval=0)

import telebot
import requests
import json
from telebot import types

TOKEN = '7362241112:AAE3WYw6XqhknE1G5QLIfW4kXoHtSUC3AwE'
API_ENDPOINT = 'http://192.168.1.72:1234/v1/chat/completions'


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в бот!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_input = message.text

    # Подготовьте данные для API-запроса
    api_data = {
        "messages": [
            {"role": "system", "content": "Ниже приведена инструкция, описывающая задачу. Напишите ответ, который соответствующим образом завершает запрос.."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 8000,
        "stream": False
    }

    # Сделайте запрос к API
    response = requests.post(API_ENDPOINT, json=api_data, headers={"Content-Type": "application/json"})


    if response.status_code == 200:
        # Анализ ответа API
        api_response = json.loads(response.text)

        # Извлечь ответ помощника из ответа API
        assistant_response = api_response["choices"][0]["message"]["content"]

        #bot.reply_to(message, assistant_response)
        bot.reply_to(message, assistant_response)
    else:
        bot.reply_to(message, "Извините, что-то пошло не так с запросом API.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
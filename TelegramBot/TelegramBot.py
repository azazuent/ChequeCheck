import os
from dotenv import load_dotenv
import telebot
import ServerAPI

load_dotenv()

api_token = os.getenv("telegram_api_token")

bot = telebot.TeleBot(token=api_token)


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    user_id = user.id
    user_name = user.username

    response = ServerAPI.register(user_id, user_name)

    if response["data"]["code"] == 0:
        user_db_id = response["data"]["user_id"]
        reply = f"You have registered under id {user_db_id}"
    else:
        reply = response["data"]["error"]

    bot.reply_to(message, reply)


@bot.message_handler(commands=['user_list'])
def get_user_list(message):
    user_list = ServerAPI.get_user_list()
    user_names = [user["user_name"] for user in user_list]
    text = '\n'.join(["Currently registered users:"] + user_names)

    bot.reply_to(message, text)


@bot.message_handler(commands=['cheque_amount'])
def get_check_amount(message):
    user_id = message.from_user.id
    response = ServerAPI.get_cheque_amount(user_id)
    if response["data"]["code"] == 0:
        cheque_amount = response["data"]["cheque_amount"]
        reply = f"You have submitted {cheque_amount} cheques"
    else:
        reply = response["data"]["error"]

    bot.reply_to(message, reply)


@bot.message_handler(content_types=['photo'])
def submit_cheque(message):
    user_id = message.from_user.id

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)

    downloaded_file = bot.download_file(file_info.file_path)
    response = ServerAPI.submit_cheque(user_id, downloaded_file)

    if response["data"]["code"] == 0:
        cheque_db_id = response["data"]["cheque_id"]
        reply = f"Check was submitted under id {cheque_db_id}"
    else:
        reply = response["data"]["error"]
    print(response)

    bot.reply_to(message, reply)


bot.infinity_polling()

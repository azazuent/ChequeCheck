#from dotenv import load_dotenv
#load_dotenv()

import os
import telebot
import ServerAPI

api_token = os.getenv("telegram_api_token")

bot = telebot.TeleBot(token=api_token)

help_message = "Привет! Этот бот позволяет сохранять и просматривать чеки.\n" \
               "Для работы отправь фото с QR-кодом чека!\n" \
               "У нас есть таблица лидеров, для желающих посоревноваться в потреблении и сканировании!\n" \
               "Буду благодарен за фидбек - пишите @azazuent.\n" \
               "И спасибо за помощь в тестировании!"


@bot.message_handler(commands=['start'])
def start(message):
    print(message.from_user.username, message.text)
    user = message.from_user
    user_id = user.id
    user_name = user.username

    response = ServerAPI.register(user_id, user_name)

    if response["data"]["code"] == 0:
        user_db_id = response["data"]["user_id"]
        reply = f"{help_message}\nВы зарегистрированы под id {user_db_id}!"
    else:
        reply = response["data"]["error"]

    bot.reply_to(message, reply)


@bot.message_handler(commands=['help'])
def get_help(message):
    print(message.from_user.username, message.text)
    bot.reply_to(message, help_message)


@bot.message_handler(commands=['user_list'])
def get_user_list(message):
    print(message.from_user.username, message.text)
    response = ServerAPI.get_user_list()
    user_list = response["data"]["user_list"]
    user_names = [user["user_name"] for user in user_list]
    text = '\n'.join(["Зарегистрированные пользователи:"] + user_names)

    bot.reply_to(message, text)


@bot.message_handler(commands=['leaderboard'])
def get_leaderboard(message):
    print(message.from_user.username, message.text)
    response = ServerAPI.get_leaderboard()
    leaderboard = response["data"]["leaderboard"]
    rows = [f'{row["user_name"]}   {row["cheque_amount"]}' for row in leaderboard]
    text = '\n'.join(["Таблица лидеров:"] + rows)

    bot.reply_to(message, text)


@bot.message_handler(commands=['cheque_amount'])
def get_cheque_amount(message):
    print(message.from_user.username, message.text)
    user_id = message.from_user.id
    response = ServerAPI.get_cheque_amount(user_id)

    if response["data"]["code"] == 0:
        cheque_amount = response["data"]["cheque_amount"]
        reply = f"Вы просканировали {cheque_amount} чека/ов!"
    else:
        reply = response["data"]["error"]

    bot.reply_to(message, reply)


@bot.message_handler(commands=['cheques'])
def get_cheques(message):
    print(message.from_user.username, message.text)
    user_id = message.from_user.id

    response = ServerAPI.get_cheques(user_id)

    if response["data"]["code"] == 0:
        cheques = response["data"]["cheques"]
        cheque_infos = []
        print(cheques)

        for cheque in cheques:
            date, time = cheque["data"]["json"]["dateTime"].split('T')
            total_sum = str(cheque["data"]["json"]["totalSum"])
            retail_place = cheque["data"]["json"]["retailPlace"]

            cheque_info = f"{date} в {time}\nвы совершили покупку в {retail_place}\n" \
                          f"на сумму {total_sum[:-2]}.{total_sum[-2:]} руб"
            cheque_infos.append(cheque_info)

        reply = "\n---------------------------------------\n".join(cheque_infos)

    else:
        reply = response["data"]["error"]

    bot.reply_to(message, reply)


@bot.message_handler(content_types=['photo'])
def submit_cheque(message):
    print(message.from_user.username, message.text)
    user_id = message.from_user.id

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)

    downloaded_file = bot.download_file(file_info.file_path)
    response = ServerAPI.submit_cheque(user_id, downloaded_file)

    if response["data"]["code"] == 666:
        reply = "Я почти попался)))"
    elif response["data"]["code"] == 0:
        cheque_db_id = response["data"]["cheque_id"]
        reply = f"Чеку присвоен id {cheque_db_id}... круто..."
    else:
        reply = response["data"]["error"]

    bot.reply_to(message, reply)


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()

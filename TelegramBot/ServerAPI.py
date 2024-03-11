import os
import requests
from dotenv import load_dotenv

load_dotenv()

server_api_url = os.getenv("server_api_url")

def register(user_telegram_id: str, user_name: str) -> dict:
    request = requests.post(url=server_api_url + f"register?"
                                                 f"user_telegram_id={user_telegram_id}"
                                                 f"&user_name={user_name}")
    response = request.json()
    return response


def submit_cheque(user_telegram_id: str, cheque_photo) -> dict:
    file = {'cheque_photo': cheque_photo}

    request = requests.post(url=server_api_url + f"submit_cheque?"
                                                 f"user_telegram_id={user_telegram_id}",
                            files=file)

    response = request.json()
    print(response)
    return response


def get_user_list() -> dict:
    request = requests.get(url=server_api_url + "user_list")
    response = request.json()
    return response


def get_cheque_amount(user_telegram_id: str) -> dict:
    request = requests.get(url=server_api_url + f"cheque_amount?user_telegram_id={user_telegram_id}")
    response = request.json()
    return response

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

import cv2
from flask import Flask, request, jsonify
import numpy as np
import json
from ChequeAPI import get_cheque_info_by_qr, QrCodeNotDetectedException, RickrollException
import DatabaseAPI

load_dotenv(find_dotenv())

app = Flask(__name__)


class RequestError(Exception):
    def __init__(self, message):
        super().__init__(message)


# noinspection PyTypedDict
@app.route("/submit_cheque", methods=['POST'])
def submit_cheque():
    user_telegram_id = request.args.get("user_telegram_id")

    response = {
        "request": {
            "action": "/submit",
            "user_telegram_id": user_telegram_id
        }
    }

    try:
        user_id = DatabaseAPI.get_user_id_by_telegram_id(user_telegram_id)

        if user_id is None:
            raise RequestError("Пользователь не зарегистрирован")

        cheque_raw = request.files['cheque_photo'].read()
        cheque_np_array = np.frombuffer(cheque_raw, np.uint8)
        cheque_qr = cv2.imdecode(cheque_np_array, cv2.IMREAD_GRAYSCALE)

        try:
            cheque_json = get_cheque_info_by_qr(cheque_qr)
            cheque_info = json.loads(cheque_json)
            print(cheque_info)
            code = cheque_info["code"]
            if code == 0 or code == 3:
                raise RequestError("Некорректный QR-код")
            if code == 5:
                raise RequestError("Информация по чеку еще не доступна, попробуйте позже")

        except RequestError:
            raise
        except QrCodeNotDetectedException:
            raise RequestError("QR-код не обнаружен, попробуйте еще раз")
        except RickrollException as err:
            response["data"] = {
                "code": 666,
                "error": str(err)
            }
            return jsonify(response)

        cheque_fiscal_sign = cheque_info["request"]["manual"]["fp"]

        try:
            cheque_id = DatabaseAPI.insert_cheque(cheque_fiscal_sign, cheque_json, user_id)
        except DatabaseAPI.DuplicateEntryError:
            raise RequestError("Чек уже был просканирован")

        response["data"] = {
            "code": 0,
            "cheque_id": cheque_id,
            "cheque_fiscal_sign": cheque_fiscal_sign
        }

    except RequestError as err:
        response["data"] = {
            "code": -1,
            "error": str(err)
        }

    return jsonify(response)


@app.route("/register", methods=["POST"])
def register():
    user_telegram_id = request.args.get("user_telegram_id")
    user_name = request.args.get("user_name")

    response = {
        "request": {
            "action": "/register",
            "user_telegram_id": user_telegram_id,
            "user_name": user_name
        }
    }

    try:
        try:
            user_id = DatabaseAPI.insert_user(user_telegram_id, user_name)
        except DatabaseAPI.DuplicateEntryError:
            raise RequestError("Пользователь уже зарегистрирован")

        response["data"] = {
            "code": 0,
            "user_id": user_id
        }

    except RequestError as err:
        response["data"] = {
            "code": -1,
            "error": str(err)
        }

    return jsonify(response)


@app.route("/user_list", methods=["GET"])
def get_user_list():
    response = {
        "request": {
            "action": "/user_list"
        }
    }

    user_list = DatabaseAPI.get_user_list()

    response["data"] = {
        "code": 0,
        "user_list": user_list
    }

    return jsonify(response)


@app.route("/cheque_amount", methods=["GET"])
def get_cheque_amount():
    user_telegram_id = request.args.get("user_telegram_id")

    response = {
        "request": {
            "action": "/cheque_amount",
            "user_telegram_id": user_telegram_id
        }
    }

    try:
        user_id = DatabaseAPI.get_user_id_by_telegram_id(user_telegram_id)

        if user_id is None:
            raise RequestError("Пользователь не зарегистрирован")

        cheque_amount = DatabaseAPI.get_cheque_amount_by_user_id(user_id)

        response["data"] = {
            "code": 0,
            "cheque_amount": cheque_amount
        }
    except RequestError as err:
        response["data"] = {
            "code": -1,
            "error": str(err)
        }

    return jsonify(response)


@app.route("/cheques", methods=["GET"])
def cheques():
    user_telegram_id = request.args.get("user_telegram_id")

    response = {
        "request": {
            "action": "/cheques",
            "user_telegram_id": user_telegram_id
        }
    }

    try:
        user_id = DatabaseAPI.get_user_id_by_telegram_id(user_telegram_id)

        if user_id is None:
            raise RequestError("Пользователь не зарегистрирован")

        cheque_list = DatabaseAPI.get_cheques_by_user_id(user_id)

        response["data"] = {
            "code": 0,
            "cheques": cheque_list
        }

    except RequestError as err:
        response["data"] = {
            "code": -1,
            "error": str(err)
        }

    return jsonify(response)


@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    response = {
        "request": {
            "action": "/leaderboard"
        }
    }

    leaderboard = DatabaseAPI.get_leaderboard()

    response["data"] = {
        "code": 0,
        "leaderboard": leaderboard
    }

    return jsonify(response)


def main():
    app.run(debug=True, host="0.0.0.0", port=3228)


if __name__ == "__main__":
    main()

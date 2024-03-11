import os

import MySQLdb
import cv2
from flask import Flask, request, jsonify
import numpy as np
import json
from dotenv import load_dotenv
from ChequeAPI import get_cheque_info_by_qr, QrCodeNotDetectedException
import SQLQueries

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv("mysql_host")
app.config['MYSQL_PORT'] = int(os.getenv("mysql_port"))
app.config['MYSQL_USER'] = os.getenv("mysql_user")
app.config['MYSQL_PASSWORD'] = os.getenv("mysql_password")
app.config['MYSQL_DB'] = os.getenv("mysql_db")

SQLQueries.init_app(app)


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
        user_id = SQLQueries.get_user_id_by_telegram_id(user_telegram_id)

        if user_id is None:
            raise RequestError("User is not registered")

        cheque_raw = request.files['cheque_photo'].read()
        cheque_np_array = np.frombuffer(cheque_raw, np.uint8)
        cheque_qr = cv2.imdecode(cheque_np_array, cv2.IMREAD_GRAYSCALE)

        try:
            cheque_json = get_cheque_info_by_qr(cheque_qr)
            cheque_info = json.loads(cheque_json)
            code = cheque_info["code"]
            if code == 0:
                raise RequestError("Incorrect cheque")
            elif code == 3:
                raise RequestError("API issue - contact developer")

        except RequestError:
            raise
        except QrCodeNotDetectedException:
            raise RequestError("QR-code not detected")

        cheque_request_number = cheque_info["data"]["json"]["requestNumber"]

        try:
            SQLQueries.insert_cheque(cheque_request_number, cheque_json, user_id)
        except MySQLdb.IntegrityError:
            raise RequestError("Cheque has already been submitted")

        cheque_id = SQLQueries.get_cheque_id_by_request_number(cheque_request_number)

        response["data"] = {
            "code": 0,
            "cheque_id": cheque_id,
            "cheque_request_number": cheque_request_number
        }

    except RequestError as err:
        response["data"] = {
            "code": -1,
            "error": str(err)
        }

    return jsonify(response)


@app.route("/register", methods=["POST"])
def register():
    user_telegram_id = str(request.args.get("user_telegram_id"))
    user_name = str(request.args.get("user_name"))

    response = {
        "request": {
            "action": "/register",
            "user_telegram_id": user_telegram_id,
            "user_name": user_name
        }
    }

    try:
        try:
            SQLQueries.insert_user(user_telegram_id, user_name)
        except MySQLdb.IntegrityError:
            raise RequestError("User is already registered")

        user_id = SQLQueries.get_user_id_by_telegram_id(user_telegram_id)

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
    user_list = SQLQueries.get_user_list()
    return jsonify(user_list)


@app.route("/cheque_amount", methods=["GET"])
def get_cheque_amount():
    user_telegram_id = str(request.args.get("user_telegram_id"))

    response = {
        "request": {
            "action": "/cheque_amount",
            "user_telegram_id": user_telegram_id
        }
    }

    try:
        user_id = SQLQueries.get_user_id_by_telegram_id(user_telegram_id)

        if user_id is None:
            raise RequestError("User is not registered")

        cheque_amount = SQLQueries.get_cheque_amount_by_user_id(user_id)

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

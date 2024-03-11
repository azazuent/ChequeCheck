from flask_mysqldb import MySQL

mysql = MySQL()

INSERT_USER = "INSERT INTO user(user_telegram_id, user_name) VALUES (%s, %s)"
INSERT_CHEQUE = "INSERT INTO cheque(cheque_request_number, cheque_json, cheque_user_id) VALUES(%s, %s, %s)"

GET_USER_ID_BY_TELEGRAM_ID = "SELECT user_id FROM user WHERE user_telegram_id = %s"
GET_CHEQUE_ID_BY_REQUEST_NUMBER = "SELECT cheque_id FROM cheque WHERE cheque_request_number = %s"
GET_USER_LIST = "SELECT * FROM user"
GET_CHEQUE_AMOUNT_BY_USER_ID = "SELECT COUNT(*) FROM cheque WHERE cheque_user_id = %s"


def init_app(app) -> None:
    mysql.init_app(app)


def insert_user(user_telegram_id: str, user_name: str) -> None:
    cursor = mysql.connection.cursor()

    cursor.execute(INSERT_USER, (user_telegram_id, user_name))

    mysql.connection.commit()
    cursor.close()


def insert_cheque(cheque_request_number: str, cheque_json: str, cheque_user_id: str) -> None:
    cursor = mysql.connection.cursor()

    cursor.execute(INSERT_CHEQUE, (cheque_request_number, cheque_json, cheque_user_id))

    mysql.connection.commit()
    cursor.close()


def get_user_id_by_telegram_id(user_telegram_id: str) -> str | None:
    cursor = mysql.connection.cursor()

    cursor.execute(GET_USER_ID_BY_TELEGRAM_ID, (user_telegram_id,))
    data = cursor.fetchall()

    if not data:
        return None

    user_id = str(data[0][0])

    cursor.close()

    return user_id


def get_cheque_id_by_request_number(cheque_request_number) -> str | None:
    cursor = mysql.connection.cursor()

    cursor.execute(GET_CHEQUE_ID_BY_REQUEST_NUMBER, (cheque_request_number,))
    data = cursor.fetchall()

    if not data:
        return None

    cheque_id = str(data[0][0])

    cursor.close()

    return cheque_id


def get_cheque_amount_by_user_id(user_id: str) -> str:
    cursor = mysql.connection.cursor()

    cursor.execute(GET_CHEQUE_AMOUNT_BY_USER_ID, (user_id,))
    data = cursor.fetchall()

    cheque_id = str(data[0][0])

    cursor.close()

    return cheque_id


def get_user_list() -> list:
    cursor = mysql.connection.cursor()

    cursor.execute(GET_USER_LIST)
    users = cursor.fetchall()
    cursor.close()

    user_list = []
    for user in users:
        user_list.append({"user_id": user[0],
                          "telegram_user_id": user[1],
                          "user_name": user[2]})

    return user_list

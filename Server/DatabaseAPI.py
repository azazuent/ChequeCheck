import os
import psycopg

INSERT_USER = "INSERT INTO user_telegram(user_telegram_id, user_name) " \
              "VALUES (%s, %s) RETURNING user_id"
INSERT_CHEQUE = "INSERT INTO cheque(cheque_fiscal_sign, cheque_json, cheque_user_id) " \
                "VALUES(%s, %s, %s) RETURNING cheque_id"

GET_USER_ID_BY_TELEGRAM_ID = "SELECT user_id FROM user_telegram WHERE user_telegram_id = %s"
GET_CHEQUE_ID_BY_FISCAL_SIGN = "SELECT cheque_id FROM cheque WHERE cheque_fiscal_sign = %s"
GET_USER_LIST = "SELECT * FROM user_telegram"
GET_CHEQUE_AMOUNT_BY_USER_ID = "SELECT COUNT(*) FROM cheque WHERE cheque_user_id = %s"
GET_CHEQUES_BY_USER_ID = "SELECT cheque_json FROM cheque WHERE cheque_user_id = %s"
GET_LEADERBOARD = "SELECT U.user_name, COUNT(*) as cheque_amount FROM " \
                  "cheque C INNER JOIN user_telegram U ON C.cheque_user_id = U.user_id " \
                  "GROUP BY U.user_id ORDER BY cheque_amount LIMIT 10"


class DuplicateEntryError(Exception):
    def __init__(self, existing_entry_id: str):
        super().__init__("Entry already exists")
        self.existing_entry_id = existing_entry_id


print(os.getenv("db_host"))
print(os.getenv("db_name"))

db_connection = psycopg.connect(
    host=os.getenv("db_host"),
    port=5432,  # int(os.getenv("db_port")),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    dbname=os.getenv("db_name")
)


def insert_user(user_telegram_id: str, user_name: str) -> str:
    cursor = db_connection.cursor()

    try:
        cursor.execute(INSERT_USER, (user_telegram_id, user_name))

        db_connection.commit()
        user_id = cursor.fetchall()[0][0]

    except psycopg.errors.UniqueViolation:
        db_connection.rollback()
        user_id = get_user_id_by_telegram_id(user_telegram_id)
        cursor.close()

        raise DuplicateEntryError(user_id)

    cursor.close()

    return user_id


def insert_cheque(cheque_fiscal_sign: str, cheque_json: str, cheque_user_id: str) -> str:
    cursor = db_connection.cursor()

    try:
        cursor.execute(INSERT_CHEQUE, (cheque_fiscal_sign, cheque_json, cheque_user_id))
        db_connection.commit()

        cheque_id = cursor.fetchall()[0][0]

    except psycopg.errors.UniqueViolation:
        db_connection.rollback()

        cheque_id = get_cheque_id_by_fiscal_sign(cheque_fiscal_sign)
        cursor.close()

        raise DuplicateEntryError(cheque_id)

    cursor.close()

    return cheque_id


def get_user_id_by_telegram_id(user_telegram_id: str) -> str | None:
    cursor = db_connection.cursor()

    cursor.execute(GET_USER_ID_BY_TELEGRAM_ID, (user_telegram_id,))
    data = cursor.fetchall()

    if not data:
        return None

    user_id = str(data[0][0])

    cursor.close()

    return user_id


def get_cheque_id_by_fiscal_sign(cheque_fiscal_sign) -> str | None:
    cursor = db_connection.cursor()

    cursor.execute(GET_CHEQUE_ID_BY_FISCAL_SIGN, (cheque_fiscal_sign,))
    data = cursor.fetchall()

    if not data:
        return None

    cheque_id = str(data[0][0])

    cursor.close()

    return cheque_id


def get_cheque_amount_by_user_id(user_id: str) -> str:
    cursor = db_connection.cursor()

    cursor.execute(GET_CHEQUE_AMOUNT_BY_USER_ID, (user_id,))
    cheque_id = cursor.fetchall()[0][0]

    cursor.close()

    return cheque_id


def get_user_list() -> list:
    cursor = db_connection.cursor()

    cursor.execute(GET_USER_LIST)
    users = cursor.fetchall()

    cursor.close()

    user_list = []
    for user in users:
        user_list.append({"user_id": user[0],
                          "telegram_user_id": user[1],
                          "user_name": user[2]})

    return user_list


def get_cheques_by_user_id(user_id: str) -> list:
    cursor = db_connection.cursor()

    cursor.execute(GET_CHEQUES_BY_USER_ID, (user_id,))
    cheques = cursor.fetchall()

    cursor.close()

    cheque_list = [cheque[0] for cheque in cheques]

    return cheque_list


def get_leaderboard() -> list:
    cursor = db_connection.cursor()

    cursor.execute(GET_LEADERBOARD)
    leaderboard = cursor.fetchall()

    cursor.close()

    formatted_leaderboard = []
    for row in leaderboard:
        formatted_leaderboard.append({"user_name": row[0],
                                      "cheque_amount": row[1]})

    return formatted_leaderboard

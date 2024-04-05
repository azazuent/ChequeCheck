import os
import requests

api_url = os.getenv("cheque_api_url")
api_token = os.getenv("cheque_api_token")


class QrCodeNotDetectedException(Exception):
    def __init__(self):
        super().__init__("No QR-code detected")


class RickrollException(Exception):
    def __init__(self):
        super().__init__("RICKROLL DETECTED")


def get_cheque_info_by_qr(cheque) -> str:

    files = {"qrfile": cheque}

    data = {'token': api_token}

    response = requests.post(url=api_url, data=data, files=files)

    return response.text

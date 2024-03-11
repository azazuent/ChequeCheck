import os
import requests
from qreader import QReader

api_url = os.getenv("cheque_api_url")
api_token = os.getenv("cheque_api_token")


class QrCodeNotDetectedException(Exception):
    def __init__(self):
        super().__init__("No QR-code detected")


class RickrollException(Exception):
    def __init__(self):
        super().__init__("RICKROLL DETECTED")


def get_cheque_info_by_qr(qrcode) -> str:
    qreader = QReader()

    qrraw = qreader.detect_and_decode(qrcode)

    if not qrraw:
        raise QrCodeNotDetectedException

    if qrraw[0] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ":
        print("RICKROLL DETECTED")
        raise RickrollException

    data = {'token': api_token, 'qrraw': qrraw}

    response = requests.post(url=api_url, data=data)

    return response.text

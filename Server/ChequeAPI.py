import os

import requests
import cv2

api_url = os.getenv("cheque_api_url")
api_token = os.getenv("cheque_api_token")


class QrCodeNotDetectedException(Exception):
    def __init__(self):
        super().__init__("No QR-code detected")


def get_cheque_info_by_qr(qrcode) -> str:
    qcd = cv2.QRCodeDetector()

    retval, qrraw, points, straight_qrcode = \
        qcd.detectAndDecodeMulti(qrcode)

    if not retval:
        raise QrCodeNotDetectedException

    data = {'token': api_token, 'qrraw': qrraw}

    request = requests.post(url=api_url, data=data)

    return request.text

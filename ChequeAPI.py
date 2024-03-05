import requests
import cv2
import json

api_url = 'https://proverkacheka.com/api/v1/check/get'
token = {'token': '26161.p2739hUKJxksGx09Q'}


class QrCodeNotDetectedException(Exception):
    def __init__(self):
        super().__init__("No QR-code detected")


def get_cheque_info_by_qr(qrcode):
    qcd = cv2.QRCodeDetector()

    retval, qrraw, points, straight_qrcode = \
        qcd.detectAndDecodeMulti(qrcode)

    if not retval:
        raise QrCodeNotDetectedException

    data = token | {'qrraw': qrraw}

    r = requests.post(url=api_url, data=data)

    d = json.loads(r.text)

    return d

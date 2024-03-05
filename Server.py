import cv2
import numpy as np
from flask import Flask, render_template, request
from ChequeAPI import get_cheque_info_by_qr

app = Flask(__name__)


@app.route("/")
def get_submit_page():
    return render_template("submit_cheque.html")


@app.route("/upload", methods=['POST'])
def upload():
    try:
        # process db interaction here
        #request.files['img'].save("cheques/lastcheck") # ignore for now
        html = get_cheque_info_by_qr(cv2.imread("cheques/lastcheck"))['data']['html']
        return html
    except Exception as e:
        return f"There was an issue submitting your cheque: {str(e)}"

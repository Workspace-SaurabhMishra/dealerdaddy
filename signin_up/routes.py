import os
import sys

from flask import Flask, request
from views.email_submit import EmailSubmit
from views.mobile_submit import MobileSubmit
from model.all_model import init_database_connection, User
from views.session_id_generator import SessionId
from views.email_verification import EmailVerification
from views.mobile_verification import MobileVerification


app = Flask(__name__)
init_database_connection()


# Todo: Think about if request is from app and there is issue within the request(e.g. method=GET)

@app.route("/sessionId", methods=["POST", "GET"])
def session_id():
    process = SessionId()
    return process.response


@app.route("/signin", methods=["POST"])
def sign_in():
    return "Signin Endpoint"


@app.route("/signup", methods=["POST"])
def sign_up():
    return "Signup Endpoint"


@app.route("/email/submission", methods=["POST"])
def email_submission():
    req_payload = request.get_json(force=True)
    process = EmailSubmit(payload=req_payload)
    return process.response


@app.route("/email/verification", methods=["POST"])
def email_verification():
    req_payload = request.get_json(force=True)
    process = EmailVerification(payload=req_payload)
    return process.response


@app.route("/mobile/submission", methods=["POST"])
def mobile_submission():
    req_payload = request.get_json(force=True)
    process = MobileSubmit(payload=req_payload)
    return process.response


@app.route("/mobile/verification", methods=["POST"])
def mobile_verification():
    req_payload = request.get_json(force=True)
    process = MobileVerification(payload=req_payload)
    return process.response


if __name__ == "__main__":
    host = "0.0.0.0"
    app.run(host=host, port=4200, debug=True)

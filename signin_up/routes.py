from flask import Flask, request
from views.email_submit import EmailSubmit
from views.mobile_submit import MobileSubmit
from model.all_model import init_database_connection
from views.session_id_generator import SessionId
from views.email_verification import EmailVerification
from views.mobile_verification import MobileVerification

app = Flask(__name__)
init_database_connection()


# Todo: Think about if request is from app and there is issue within the request(e.g. method=GET)

@app.route("/get/session_id", methods=["POST", "GET"])
def session_id():
    process = SessionId()
    return process.response


@app.route("/submit/email", methods=["POST"])
def email_submission():
    req_payload = request.get_json(force=True)
    process = EmailSubmit(request_payload=req_payload)
    return process.response


@app.route("/verify/email", methods=["POST"])
def email_verification():
    req_payload = request.get_json(force=True)
    process = EmailVerification(payload=req_payload)
    return process.response


@app.route("/submit/mobile", methods=["POST"])
def mobile_submission():
    req_payload = request.get_json(force=True)
    process = MobileSubmit(payload=req_payload)
    return process.response


@app.route("/verify/mobile", methods=["POST"])
def mobile_verification():
    req_payload = request.get_json(force=True)
    process = MobileVerification(payload=req_payload)
    return process.response


@app.route("/submit/password", methods=["POST"])
def password_submission():
    pass


@app.route('/submit/detail', methods=["POST"])
def details_submission():
    pass


@app.route("/resource/protected")
def protected():
    return "Protected Resource"


if __name__ == "__main__":
    host = "0.0.0.0"
    app.run(host=host, port=4200, debug=True)

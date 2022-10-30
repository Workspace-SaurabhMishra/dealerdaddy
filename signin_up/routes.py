from flask import Flask, request
from signin_up.views.email_submit import EmailSubmit
from signin_up.views.mobile_submit import MobileSubmit
from signin_up.model.all_model import initDatabaseConnection, User
from signin_up.views.session_id_generator import SessionId

app = Flask(__name__)
initDatabaseConnection()


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
    pass


@app.route("/mobile/submission", methods=["POST"])
def mobile_submission():
    req_payload = request.get_json(force=True)
    process = MobileSubmit(payload=req_payload)
    return process.response


@app.route("/mobile/verification", methods=["POST"])
def mobile_verification():
    pass


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4200, debug=False)

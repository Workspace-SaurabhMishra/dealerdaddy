from flask import Flask, request
from views.generate_refresh_token import GenerateRefreshToken
from views.verify_refresh_token import VerifyTokens

app = Flask(__name__)


@app.route("/refreshToken/generate",methods=["GET"])
def create_refresh_token():
    process = GenerateRefreshToken()
    return process.response


@app.route("/accessToken/verify",methods=["POST"])
def verify_access_token():
    req_payload = request.get_json(force=True)
    process = VerifyTokens(payload=req_payload)
    return process.response


if __name__ == "__main__":
    host = "0.0.0.0"
    app.run(host=host, port=4201, debug=True)

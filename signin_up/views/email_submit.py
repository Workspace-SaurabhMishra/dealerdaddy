import json
import smtplib
import random
import string
import typing
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Response
from marshmallow import Schema, fields, validate, utils

from signin_up.model.all_model import User


def email_payload_validator(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            EmailRequestSchema().load(self.payload)
        except Exception as e:
            self.response = Response(json.dumps("{0}".format(e)),
                                     status=400,
                                     mimetype='application/json')
            return
        function(self)

    return wrapper


def error_control(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            function(self)
        except Exception as e:  # Todo: implement for every case and every status code
            print(e)
            self.response = Response(json.dumps({"response": str(e)}),
                                     status=400,
                                     mimetype='application/json')

    return wrapper


def duplicate_user(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        self.session_user = User.objects(user_id=self.session_id)
        if len(self.session_user) == 0:
            self.response = Response(json.dumps({"response": "invalid process"}), status=400,
                                     mimetype="application/json")
            # {reminder}report false signup attempt
            return
        else:
            temp = User.objects(email=self.email)
            if len(temp) == 1:
                self.response = Response(json.dumps({"response": "email address exist"}), status=400,
                                         mimetype="application/json")
            elif len(temp) == 2:
                pass
                # {reminder} report duplicate data in DB
            else:
                function(self)

    return wrapper


class CustomStringField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs) -> typing.Any:
        if not isinstance(value, (str, bytes)) or value == "":
            raise self.make_error("invalid")
        try:
            return utils.ensure_text_type(value)
        except UnicodeDecodeError as error:
            raise self.make_error("invalid_utf8") from error


class EmailRequestSchema(Schema):
    session_id = CustomStringField(required=True)
    email = CustomStringField(required=True)
    # Todo: Do something about empty string


class EmailSubmit:
    def __init__(self, payload):
        self.session_user = None
        self.payload = payload
        self.email = payload.get('email')
        self.session_id = payload.get('session_id')
        self.otp = ''.join(random.choices(string.digits, k=4))
        self.response = Response(json.dumps({"response": "Something went wrong"}), status=500,
                                 mimetype="application/json")
        self.engine()

    @error_control
    @email_payload_validator
    @duplicate_user
    def engine(self):
        self.send_email()
        self.persist_email()

    def send_email(self):
        sender_email = "contact@dealerdaddy.in"
        sender_password = "callmesaurabh"  # Todo: implement dotenv
        email_html = f'''
                <html>
                <body>
                <Center>
                <div style="
                    padding:40px;
                    background-color:rgb(255, 153, 194);
                    width:400px;
                    height: 250px;
                    border-radius: 20px;">
                  <h2>
                    Hello
                  </h2>
                  <h3>
                    Please use the below code below for CardUp signup process.
                  </h3>
                  <h1 style="color:black;">{self.otp}</h1>
                   <h3> If you didn't request this email, you can ignore this email.<h3>
                  <h4>Team CardUp</h4>
                  </div>
                </Center>
                </body>
                </html>
                '''

        email_message = MIMEMultipart()
        email_message['From'] = sender_email
        email_message['To'] = self.email
        email_message['Subject'] = 'CardUp Account Setup'
        email_message.attach(MIMEText(email_html, "html"))
        email_string = email_message.as_string()

        server = smtplib.SMTP('smtpout.secureserver.net', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, self.email, email_string)
        server.quit()
        self.response = Response(json.dumps({
            "response": "email sent"
        }), status=200, mimetype="application/json")

    def persist_email(self):
        print(self.session_user)
        x = self.session_user[0]
        x["email"] = self.email
        x.save()

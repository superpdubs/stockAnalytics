import validators
from models import *
from app import session


class RegisterValidator:

        def validate(self, user):
            if user['firstname'] and user['lastname'] and user['password'] and user['cpass'] and user['email'] and user['vcode']:
               if session.get(user['email']) == user['vcode']:
                   message = None
                   # clear user vcode in session
                   session.pop(user['email'])
               else:
                   message =  'Incorrect verification code'
            else:
                message = "Please complete all the personal details"

            return message


class LoginValidator:

    def validate(self, user):
        message = None
        if user['email']:
            if user['password']:
                to_match_user = User.query.filter(User.email == user['email']).first()
                if to_match_user is not None:
                    to_match_Password = to_match_user.user_pass
                    if user['password'] == to_match_Password:
                        message = None
                    else:
                        message = "Email and password doesn't match"
                else:
                    message = "This email doesn't exist"
            else:
                message = "Please input your password"
        else:
            message = "Please input your email"

        return message


class EmailValidator:

    def validate(self,thisemail):
        if validators.email(thisemail):
            to_get_email = User.query.filter(User.email == thisemail).first()
            if to_get_email is not None:
                return "This email already exist"
            else:
                return None
        else:
            return "Please input a value Email address"

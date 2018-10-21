import validators
from models import *
from codegenerator import Encryption
from app import session
encryption = Encryption()

class RegisterValidator:
    def validate(self, user):
        # TODO: More robust checking
        if user['firstname'] and user['lastname'] and user['password'] and user['cpass'] and user['email']:
            return None
        else:
            return "Please complete all the personal details"


class UpdateValidator:
    def validate(self, user):
        if user['firstname'] and user['lastname']:
            return None
        else:
            return "Please complete all the personal details"


class PasswordValidator:
    def validate(self, user):
        to_match_user = User.query.filter(User.email == user['email']).first()
        if to_match_user is None:
            return "Email not found"
        to_match_Password = to_match_user.user_pass
        if user['oldpass'] != encryption.decrpty_Code(to_match_Password):
            return "Incorrect password"
        if len(user['password']) < 6 or len(user['password']) > 11:
            return "Password must be 6-11 characters"
        return None


class LoginValidator:

    def validate(self, user):
        message = None
        if user['email']:
            if user['password']:
                to_match_user = User.query.filter(User.email == user['email']).first()
                if to_match_user is not None:
                    to_match_Password = to_match_user.user_pass
                    if user['password'] == encryption.decrpty_Code(to_match_Password):

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
                return "Email address taken"
            else:
                return None
        else:
            return "Invalid email address"

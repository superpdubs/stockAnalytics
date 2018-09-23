import validators
from models import *

class RegisterValidator:

        def validate(self, user):
            emailvalidator = EmailValidator()
            message = None
            if validators.length(user['firstname'],min=1):
                if validators.length(user['lastname'],min=1):
                    if validators.email(user['email']):
                        if not emailvalidator.exist(user['email']):
                            if validators.length(user['password'], min=6, max=12):
                                if user['confirmPass'] == user['password']:
                                            pass
                                else:
                                    message = "The confirm password doesn't match"
                            else:
                                message = "The length of password doesn't match"
                        else:
                            message = "This email already exist"
                    else:
                        message = "Please input a correct format email"
                else:
                    message = "Last name cannot be empty"
            else:
                message = "First name cannot be empty"

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
                        message = 'Congratulations! Login successfully'
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
            return "This email format is uncorrect"

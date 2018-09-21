import validators
from models import *

class RegisterValidator:

        def validate(self, user):
            message = None
            if validators.length(user['name'], min=4, max=11):
                if validators.email(user['email']):
                    if validators.length(user['password'], min=6, max=12):
                        if user['confirmPass'] == user['password']:
                            to_find_username = User.query.filter(User.user_name == user['name']).first()
                            if to_find_username is None:
                                to_find_useremail = User.query.filter(User.email == user['email']).first()
                                if to_find_useremail is None:
                                    pass
                                else:
                                    message = "This email already exists"
                            else:
                                message = "This User name already exists"
                        else:
                            message = "The confirm password doesn't match"
                    else:
                        message = "The length of password doesn't match"
                else:
                    message = "The email format is not correct"
            else:
                message = "The length of user name doesn't match"

            return message


class LoginValidator:

    def validate(self, user):
        message = None
        if user['name']:
            if user['password']:
                to_match_user = User.query.filter(User.user_name == user['name']).first()
                if to_match_user is not None:
                    to_match_Password = to_match_user.user_pass
                    if user['password'] == to_match_Password:
                        message = 'Congratulations! Login successfully'
                    else:
                        message = "User name and password doesn't match"
                else:
                    message = "This username doesn't exist"
            else:
                message = "Please input your password"
        else:
            message = "Please input your username"

        return message


class EmailValidator:

    def exist(self,thisemail):
        to_get_email = User.query.filter_by(User.email==thisemail).first()
        if to_get_email is not None:
            return True
        else:
            return False

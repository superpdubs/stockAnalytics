import validators


class UserValidator:

        def validate(self, user):
            message = None
            if validators.length(user['name'], min=4, max=11):
                if validators.email(user['email']):
                    if validators.length(user['password'], min=6, max=12):
                        if user['confirmPass'] == user['password']:
                            pass
                        else:
                            message = "The confirm password doesn't match"
                    else:
                        message = "The length of password doesn't match"
                else:
                    message = "The email format is not correct"
            else:
                message = "The length of user name doesn't match"

            return message



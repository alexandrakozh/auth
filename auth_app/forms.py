from flask.wtf import Form, TextField, PasswordField, validators
from .models import User


class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not User:
            self.username.errors.append('Unknown user')
            return False
        if not user.verify_password(self.password.data):
            self.password.errors.append('Unknown password')
            return False
        self.user = user
        return True


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.DataRequired(),
                                              validators.EqualTo('confirm',
                                              message='Passwords must match')
                                              ])
    confirm = PasswordField('Repeat Password')

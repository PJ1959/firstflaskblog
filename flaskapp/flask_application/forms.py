from mongoengine import DoesNotExist, MultipleObjectsReturned

from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed

from wtforms import (TextField, PasswordField, validators,
                     ValidationError)

from flask.ext.login import login_user

from .models import User

IMAGES = ['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp']


class RegistrationForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=32)])
    name = TextField('Fullname', [validators.Length(min=6, max=64)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=32),
                                        validators.Email()])
    password = PasswordField('New Password')

    def validate_password(form, field):
        try:
            user = User.objects.get(email=form.email.data)
            if user.password == form.password.data:
                user.authenticated = True
                user.save()
                login_user(user)
            else:
                raise ValidationError('Invalid username or password')
        except (DoesNotExist, MultipleObjectsReturned):
            raise ValidationError('Invalid username or password')


class SearchForm(Form):
    search = TextField('Search', [validators.InputRequired()])


msg = 'This field is required'


class CarForm(Form):
    manufacturer = TextField('Manufacturer',
                             [validators.Length(max=32),
                              validators.InputRequired()])
    model = TextField('Model', [validators.Length(max=32),
                                validators.InputRequired()])
    year = TextField('Year', [validators.Length(min=4, max=4),
                              validators.InputRequired()])
    photo = FileField(u'Photo', [FileAllowed(IMAGES, 'Only images allowed')])
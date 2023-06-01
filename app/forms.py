from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Это имя занято, попробуйте другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот email занят, попробуйте другой.')


class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Update')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None and username.data != current_user.username:
            raise ValidationError('Это имя занято, попробуйте другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and email.data != current_user.email:
            raise ValidationError('Этот email занят, попробуйте другой.')

class UpdatePassword(FlaskForm):
    old_password = StringField('Old password', validators=[DataRequired()])
    new_password = StringField('Old password', validators=[DataRequired()])
    confirm_password = StringField('Old password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Save')

    def validate_old_password(self, old_password):
        if not current_user.check_password(old_password.data):
            raise ValidationError('Вы ввели неверный пароль!')
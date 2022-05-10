from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from blog.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


class RegisterForm(FlaskForm):

    def validate_username(self, user_to_check):
        user = User.query.filter_by(username=user_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('Email already exists! Please try a different email')

    username = StringField(label='Username:', validators=[Length(min=7, max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6, max=60), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sing in')


class UpdateProfileForm(FlaskForm):
    username = StringField(label='Username:', validators=[Length(min=7, max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    picture = FileField(label='Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField(label='Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists! Please try a different email')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists! Please try a different username')


class ResetForm(FlaskForm):
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Reset Password')

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user is None:
            raise ValidationError('There is no account with the email.')


class ResetPasswordForm(FlaskForm):
    password1 = PasswordField(label='Password:', validators=[Length(min=6, max=60), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Reset Password')

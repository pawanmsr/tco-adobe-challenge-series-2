from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
from wtforms.validators import NumberRange

from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename

from wtforms import SelectField
from wtforms.validators import Optional

class RegisterForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired()
        ]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Log In')

class UploadForm(FlaskForm):
    upload = FileField(
        'Upload PDF',
        validators=[
            FileAllowed(['pdf'], message='Please upload PDFs only!'),
            FileRequired()
        ]
    )
    submit = SubmitField('Upload')

class ViewForm(FlaskForm):
    filename = SelectField(
        'Filename',
        choices=[],
        validators=[
            Optional()
        ]
    )
    submit = SubmitField('View')

class MergeForm(FlaskForm):
    first_filename = SelectField(
        'Filename',
        choices=[],
        validators=[
            DataRequired()
        ]
    )
    second_filename = SelectField(
        'Filename',
        choices=[],
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Merge')

class DeleteForm(FlaskForm):
    filename = SelectField(
        'Filename',
        choices=[],
        validators=[
            DataRequired()
        ]
    )
    page = IntegerField(
        'Page',
        validators=[
            InputRequired(),
            NumberRange(min=1, max=None, message="Please enter a positive integer.")
        ]
    )
    submit = SubmitField('Delete')

class ReorderForm(FlaskForm):
    filename = SelectField(
        'Filename',
        choices=[],
        validators=[
            DataRequired()
        ]
    )
    pages = StringField(
        'Pages (Enter comma seperated numbers)',
        validators=[
            InputRequired()
        ]
    )
    submit = SubmitField('Reorder')
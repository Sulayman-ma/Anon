from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import PasswordField



class SearchForm(FlaskForm):
    search = StringField(render_kw={
        'placeholder': 'Search user by plate number or email',
        'class': 'u-full-width',
        'required': 'required',
        'style': 'width: 70%;'
    })
    query = SubmitField()


class Login(FlaskForm):
    user_id = StringField(render_kw={
        'placeholder': 'User ID',
        'required': 'required'
    })
    password = PasswordField(render_kw={
        'placeholder': 'Password',
        'required': 'required'
    })
    login = SubmitField()
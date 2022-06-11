from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, EmailField


class RegForm(FlaskForm):
    # User information
    # ------------------------------------- #
    fname = StringField(render_kw={
        'placeholder': 'First Name',
        'required': 'required',
        'class': ['u-full-width']
    })
    mname = StringField(render_kw={
        'placeholder': 'Middle Name',
        'class': 'u-full-width'
    })
    lname = StringField(render_kw={
        'placeholder': 'Last Name',
        'required': 'required',
        'class': 'u-full-width'
    })
    phone = StringField(render_kw={
        'placeholder': 'Phone',
        'required': 'required',
        'class': 'u-full-width'
    })
    state = StringField(render_kw={
        'placeholder': 'State of Origin',
        'required': 'required',
        'class': 'u-full-width'
    })
    address = StringField(render_kw={
        'placeholder': 'Address',
        'required': 'required',
        'class': 'u-full-width'
    })
    gender = RadioField(choices=[('male','Male'),('female','Female')])
    email = EmailField(render_kw={
        'placeholder': 'Email',
        'required': 'required',
        'class': 'u-full-width'
    })
    
    # Next of Kin Information
    # ------------------------------------- #
    nk_name = StringField(render_kw={
        'placeholder': 'Full Name(last name prio)',
        'required': 'required',
        'class': 'u-full-width'
    })
    nk_relation = StringField(render_kw={
        'placeholder': 'Relationship',
        'required': 'required',
        'class': 'u-full-width'
    })
    nk_address = StringField(render_kw={
        'placeholder': 'Address',
        'required': 'required',
        'class': 'u-full-width'
    })
    
    # Car Information
    # ------------------------------------- #
    plate_number = StringField(render_kw={
        'placeholder': 'Plate Number',
        'required': 'required',
        'class': 'u-full-width'
    })
    model = StringField(render_kw={
        'placeholder': 'Model',
        'required': 'required',
        'class': 'u-full-width'
    })
    color = StringField(render_kw={
        'placeholder': 'Color',
        'required': 'required',
        'class': 'u-full-width'
    })

    submit = SubmitField()  
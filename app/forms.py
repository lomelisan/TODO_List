from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message='Campo Requerido')])
    password = PasswordField('Clave', validators=[DataRequired(message='Campo Requerido')])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(message='Campo Requerido')])
    email = StringField('Email', validators=[DataRequired(message='Campo Requerido'), Email(message='Dirección invalida')])
    password = PasswordField('Clave', validators=[DataRequired(message='Campo Requerido')])
    password2 = PasswordField(
        'Repetir clave', validators=[DataRequired(message='Campo Requerido'), EqualTo('password', message='Ambas claves deben coincidir')])
    submit = SubmitField('Registrarme')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Por favor use otro nombre de usuario.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor use otra dirección de email.')

class CreateTaskForm(FlaskForm):
    body = TextAreaField(('Halgo por hacer'), validators=[DataRequired(message='Campo Requerido')])
    submit = SubmitField('Enviar')

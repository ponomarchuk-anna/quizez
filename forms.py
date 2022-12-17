from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class QuizForm(FlaskForm):
    name = StringField(
        'Название квиза',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    counter = StringField(
        'Введите количество вопросов',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    submit = SubmitField(
        'Далее',
        render_kw={'class': 'btn btn-success'},
        )


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя', validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    password = PasswordField(
        'Пароль', validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    remember_me = BooleanField(
        'Запомнить меня', default=True,
        render_kw={'class': 'form-check-input'},
        )
    submit = SubmitField(
        'Войти',
        render_kw={'class': 'btn btn-success'},
        )


class RegForm(FlaskForm):
    username = StringField(
        'Имя пользователя', validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    password = PasswordField(
        'Пароль', validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    password2 = PasswordField(
        'Подтвердите пароль', validators=[DataRequired(), EqualTo('password')],
        render_kw={'class': 'form-control'},
        )
    submit = SubmitField(
        'Зарегистрироваться',
        render_kw={'class': 'btn btn-success'},
        )

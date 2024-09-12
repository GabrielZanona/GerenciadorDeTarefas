from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=1, max=150)])
    description = TextAreaField('Descrição', validators=[DataRequired(message="A descrição é obrigatória."), Length(min=1)])
    status = SelectField('Status', choices=[('Pendente', 'Pendente'), ('Em Andamento', 'Em Andamento'),('Concluída', 'Concluída')], default='Pendente')
    shared_with = SelectMultipleField('Compartilhar com', coerce=int)
    submit = SubmitField('Criar Tarefa')

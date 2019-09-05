"""
Модуль в котором создаются формы.
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired
from app.models import Group


def select_active_group(groups):
    lst = []
    for i in groups:
        lst.append((i.name, i.name))
    return lst


class CreateGroup(FlaskForm):
    """
    Форма для создания новой рабочей группы.
    
    :param FlaskForm: класс с которого наследуем.
    :type FlaskForm: class
    """
    groupname = StringField("Название группы", validators=[DataRequired()])
    lora_id = SelectField("Lora ID", choices=[('57651140987083', '57651140987083'), ('52016726902762', '52016726902762'), ('82676944256537', '82676944256537')])
    submit = SubmitField("Создать")


class DeleteGroup(FlaskForm):
    """
    Форма для удаления рабочей грппы, точнее ее деактивации, в базе она все равно сохраниться.
    
    :param FlaskForm: [description]
    :type FlaskForm: [type]
    """
    group_list = SelectField("Активные группы", validators=[InputRequired()])
    submit = SubmitField("Удалить")

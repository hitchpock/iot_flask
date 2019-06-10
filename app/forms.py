from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired
from app.models import Group


def select_active_group(groups):
    lst = []
    for i in groups:
        lst.append((i.name, i.name))
    return lst


class CreateButton(FlaskForm):
    groupname = StringField("Название группы", validators=[DataRequired()])
    lora_id = SelectField("Lora ID", choices=[('57651140987083', '57651140987083'), ('52016726902762', '52016726902762'), ('82676944256537', '82676944256537')])
    submit = SubmitField("Создать")


class DeleteGroup(FlaskForm):
    group_list = SelectField("Активные группы", validators=[InputRequired()])
    submit = SubmitField("Удалить")

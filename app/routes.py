"""
Можно сказать, что основной блок, происходит работа со всеми вкладками на станице, весь основной функционал.
"""
from flask import render_template, redirect, url_for
from flask import Markup
from app import app, db
from app.models import Worker, Group, EnterGroup
from app.forms import CreateGroup, DeleteGroup
from datetime import datetime


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    Главная страничка, на которой отобржаются все рабочие с коментариями про укрытие.
    """
    workers = Worker.query.all()
    return render_template('index.html', title='Home', data=workers)


@app.route('/group_list', methods=['GET', 'POST'])
def group_list():
    """
    Список групп с участниками и комментариями.
    """
    groups = Group.query.filter(Group.active == True).all()
    for g in groups:
        g.checking()
    return render_template('group_list.html', lst=groups)


@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    """
    Создание новой группы.
    """
    form = CreateGroup()    # Фигачим форму добавления группы на страницу.
    enter_group = Worker.query.filter(Worker.uid == EnterGroup.uid).all()
    if form.validate_on_submit():
        # Если нажали на кнопку
        group = Group(name=form.groupname.data, lora_id=form.lora_id.data)      # Берем имя и id лоры из табицы
        for worker_l in enter_group:
            group.workers_list.append(worker_l)     # Копирование рабочих из входной группы в обычную
        db.session.add(group)       # Что-то тип добавления изменений в бд
        ws = EnterGroup.query.all()
        for i in ws:
            db.session.delete(i)    # Очистка входной группы
        db.session.commit()     # Сохранение изменений в бд
        return redirect(url_for('group_list'))
    return render_template('create_group.html', data=enter_group, form=form)


@app.route('/delete_group', methods=['GET', 'POST'])
def delete_group():
    """
    Удаление(деактивация) группы.
    """
    db_group_list = Group.query.filter(Group.active==True).all()    # Берем все активные группы
    group_list = [(i.name, i.name) for i in db_group_list]          # и кидаем в селект, чтобы можно было выбрать
    form = DeleteGroup()    # Кидаем форму на страницу.
    form.group_list.choices = group_list
    if form.validate_on_submit():   # Еслм нажали кнопку delete
        gl = form.group_list.data       # Выбираем имя из селектора
        group = Group.query.filter(Group.name == gl).first()    # Достаем группу по выбранному имени
        group.active = False    # Ставим маркер активности в False
        group.endtime = datetime.utcnow()   # Записываем время окончания работ группы
        db.session.commit()     # Сохраняем изменения в бд
        return redirect(url_for('delete_group'))
    return render_template('delete_group.html', form=form)


@app.route('/chart', methods=['GET', 'POST'])
def chart():
    """
    Функция для сбора инфы для построения графиков. Уже сам не помню как, но я умудрился сделать ее рабочей.
    Вроде на грфике показывается сколько человек было на какой-то площадке за такое то число.
    """
    groups = Group.query.all()
    groups_dict = {}
    second_lst = []
    for group in groups:
        if groups_dict.get(group.lora_id) is not None:
            groups_dict[group.lora_id]['date'].append(datetime.strftime(group.dtime, "%d-%m-%Y"))
            groups_dict[group.lora_id]['count'].append(len(group.workers_list))
        else:
            groups_dict[group.lora_id] = {'date': [datetime.strftime(group.dtime, "%d-%m-%Y")],\
                'count': [len(group.workers_list)]}
    for k, v in groups_dict.items():
        second_lst.append({'number': k, 'data': v})
    return render_template('chart.html', dct=second_lst)

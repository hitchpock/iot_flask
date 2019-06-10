from flask import render_template, redirect, url_for
from flask import Markup
from app import app, db
from app.models import Worker, Group, EnterGroup
from app.forms import CreateButton, DeleteGroup
from datetime import datetime


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    workers = Worker.query.all()
    return render_template('index.html', title='Home', data=workers)


@app.route('/group_list', methods=['GET', 'POST'])
def group_list():
    groups = Group.query.filter(Group.active == True).all()
    for g in groups:
        g.checking()
    return render_template('group_list.html', lst=groups)


@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    form = CreateButton()
    enter_group = Worker.query.filter(Worker.uid == EnterGroup.uid).all()
    if form.validate_on_submit():
        group = Group(name=form.groupname.data, lora_id=form.lora_id.data)
        for worker_l in enter_group:
            group.workers_list.append(worker_l)
        db.session.add(group)
        ws = EnterGroup.query.all()
        for i in ws:
            db.session.delete(i)
        db.session.commit()
        return redirect(url_for('group_list'))
    return render_template('create_group.html', data=enter_group, form=form)


@app.route('/delete_group', methods=['GET', 'POST'])
def delete_group():
    db_group_list = Group.query.filter(Group.active==True).all()
    group_list = [(i.name, i.name) for i in db_group_list]
    form = DeleteGroup()
    form.group_list.choices = group_list
    if form.validate_on_submit():
        gl = form.group_list.data
        group = Group.query.filter(Group.name == gl).first()
        group.active = False
        group.endtime = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('delete_group'))
    return render_template('delete_group.html', form=form)


@app.route('/chart', methods=['GET', 'POST'])
def chart():
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

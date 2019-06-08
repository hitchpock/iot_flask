from flask import render_template, redirect, url_for
from app import app, db
from app.models import Worker, Group, EnterGroup
from app.forms import CreateButton, DeleteGroup
from datetime import datetime


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    user = {'username': 'Начальник'}
    workers = Worker.query.all()
    return render_template('index.html', title='Home', user=user, data=workers)


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

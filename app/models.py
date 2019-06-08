from app import db
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True)
    workers_list = db.relationship('Worker', secondary='links', cascade='save-update')
    dtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    button = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    lora_id = db.Column(db.String(14), index=True, unique=True)
    endtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def __init__():
        self.check = checking()
    
    def checking(self):
        
        def foo(lst):
            for i in lst:
                if i.insafe == False:
                    return False
            return True
        
        x = self.workers_list
        self.check = foo(x)

    def __repr__(self):
        return "<Group {}>".format(self.name)
    


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64), index=True, unique=True)
    uid = db.Column(db.String(14), index=True, unique=True)
    insafe = db.Column(db.Boolean, default=False)
    group_list = db.relationship('Group', secondary='links')

    def __repr__(self):
        return "<Worker {}>".format(self.fullname)


class Links(db.Model):
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), primary_key=True)


class EnterGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(14), index=True, unique=True)

    def __repr__(self):
        return "<Idworker {}>".format(self.uid)

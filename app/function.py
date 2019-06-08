from app.models import Worker, Group, EnterGroup

def select_worker_from_enter():
    worker_list = Worker.query.filter(Worker.uid == EnterGroup.uid)
    for i in worker_list:
        print(i.fullname)

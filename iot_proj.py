from app import app, db
from app.models import Worker, Group, EnterGroup


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Worker': Worker, 'Group': Group}

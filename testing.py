from app import app, db
from app.models import Group
g = Group.query.filter(Group.name == 'second group').all()[0]
g.active = True
db.session.commit()
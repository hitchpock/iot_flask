"""
Обязательный файл для того чтобы работать как с модулем. У всех модулей есть __init__.py
Просто подключаем все что есть.
"""
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from app import routes, models
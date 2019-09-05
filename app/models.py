"""
Модуль в котором создаем представления для БД, все происзодит в ORM "режиме".
Для просмотра использовал DB Browser for SQLite.
"""
from app import db
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Group(db.Model):
    """
    Класс для представления таблицы групп. С db.Model наследуемся.
    """
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(256), index=True)    # Название группы(видимо какие-то кодовые имена состоящие из даты или еще чего то)
    workers_list = db.relationship('Worker', secondary='links', cascade='save-update')      # Список всех рабочих в группе
    dtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # Дата и время создания группы
    button = db.Column(db.Boolean, default=False)       # По всей видимости это выполняло функцию поля active, но при удалении оно не захотело удалять и осталось как живой труп в коде.
    active = db.Column(db.Boolean, default=True)    # Показывает находится группа на площадке или нет, то есть активна или нет, после удаления грппы она деактивируется.
    lora_id = db.Column(db.String(14), index=True)      # id Лоры, чтобы понимать с какой площадки поступает инфа.
    endtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)   # Время деактивации, ведется подсчет времени, чтобы высчитывать зп, крч аналитика
    
    def checking(self):
        """
        Проверяет все ли рабочие находятся в укрытии.
        
        :return: False - если кто-то не в укрытии, True - если в укрытии.
        :rtype: Boolean
        """
        
        def foo(lst):
            """
            Сама функция проверки.
            
            :param lst: Список рабочих.
            :type lst: list
            :return: True/False
            :rtype: Boolean
            """
            for i in lst:
                if i.insafe == False:
                    return False
            return True
        
        x = self.workers_list
        self.check = foo(x)     # Либо все в укрытии, либо кто-то не в укрытии

    def __repr__(self):
        return "<Group {}>".format(self.name)
    


class Worker(db.Model):
    """
    Класс для представления таблицы рабочих.
    """
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64), index=True, unique=True)    # Полное имя рабочего
    uid = db.Column(db.String(14), index=True, unique=True)     # Свой собственный id(для карточки, которую прикладывает).
    insafe = db.Column(db.Boolean, default=False)       # В безопасности или нет
    group_list = db.relationship('Group', secondary='links')    # Список групп в которыйх он когда либо был, для аналитики.

    def __repr__(self):
        return "<Worker {}>".format(self.fullname)


class Links(db.Model):
    """
    Вспомогательный класс для связи многие-ко-многим. Соединяет множество групп с можеством рабочих.
    """
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), primary_key=True)


class EnterGroup(db.Model):
    """
    Вроде это некий костыль, когда создаем группу, то она сначала добавляется сюда, и только потом инфа из нее копируется в WorkGroup.
    
    :param db: [description]
    :type db: [type]
    :return: [description]
    :rtype: [type]
    """
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(14), index=True, unique=True)

    def __repr__(self):
        return "<Idworker {}>".format(self.uid)

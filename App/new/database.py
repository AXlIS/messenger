from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, MetaData, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import and_, exists
from icecream import ic
from datetime import datetime
from hashlib import pbkdf2_hmac

Base = declarative_base()

Friends = Table("Friends", Base.metadata,
                Column("left", Integer, ForeignKey("users.id")),
                Column("right", Integer, ForeignKey("users.id"))
                )


class Client(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(128))

    lines = relationship("ClientHistory", backref="client_ids")
    friends = relationship("Client",
                           secondary=Friends,
                           primaryjoin=id == Friends.c.left,
                           secondaryjoin=id == Friends.c.right,
                           backref="lefts",
                           lazy='subquery'
                           )

    # def __init__(self, login, password):
    #     self.login = login
    #     self.password = password

    def __str__(self):
        return f'Client(id={self.id}; login={self.login}, friends={self.friends})'

    def __repr__(self):
        return f'Client(id={self.id}; login={self.login}, friends={self.friends})'


class ClientStorage:
    def __init__(self, session):
        self.session = session

    def add_client(self, login, password, friends):
        try:
            with self.session.begin():
                self.session.add(Client(login=login, password=password, friends=friends))
        except:
            print('Имя должно быть уникальным!')

    def find(self, login):
        criteria = exists().where(and_(Client.login == login))
        return self.session.query(Client).filter(criteria).first() != None


class ClientHistory(Base):
    __tablename__ = 'connect_history'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    ip = Column(String(32))
    time = Column(DateTime)  # default=datetime.utcnow
    status = Column(String(6))

    def __repr__(self):
        return f'ClientHistory(id={self.id};' \
               f' client_id={self.client_id};' \
               f' time={self.time};' \
               f' ip={self.ip}' \
               f' status={self.status})'


class ClientHistoryStorage:

    def __init__(self, session):
        self.session = session

    def add_line(self, ip, client_id, status):
        date = datetime(
            datetime.now().year,
            datetime.now().month,
            datetime.now().day,
            datetime.now().hour,
            datetime.now().minute,
            datetime.now().second
        )

        with self.session.begin_nested():
            self.session.add(
                ClientHistory(ip=ip, client_id=client_id, time=date, status=status)
            )


if __name__ == '__main__':
    engine = create_engine("sqlite:///database.db", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        client_storage = ClientStorage(session)
        history_storage = ClientHistoryStorage(session)
        # history_storage.add_line(ip='124.0.4.1', client_id=4, status='login')
        # history_storage.add_line(ip='123.0.3.1', client_id=3, status='login')
        # history_storage.add_line(ip='122.0.2.1', client_id=2, status='login')
        # history_storage.add_line(ip='123.0.3.1', client_id=3, status='exit')
        # history_storage.add_line(ip='122.0.2.1', client_id=2, status='exit')
        # history_storage.add_line(ip='127.0.0.1', client_id=1, status='login')
        # history_storage.add_line(ip='127.0.0.1', client_id=1, status='exit')
        # history_storage.add_line(ip='124.0.4.1', client_id=4, status='exit')
        # client_storage.add_client('Igor', '12345')
        # client_storage.add_client('Oleg', password='12345')
        # for i in session.query(Client.password, Client.login).all():
        #     print(i)
        # history_storage.add_line(ip='127.0.0.1', client_id=2, status='login')
        # history_storage.add_line(ip='127.0.0.1', client_id=2, status='exit')
        # ic(client_storage.find('Igor'))
        # client_storage.add_client(login='Igor', password='12345', friends=[])
        # client_storage.add_client(login='Oleg', password='12345', friends=[user1])
        # user2 = session.query(Client).filter(Client.login == 'Oleg').first()
        # client = session.query(Client).filter(Client.login == 'Igor').first()
        # print(client)
        # lines = client.lines
        # for line in lines:
        # #     print(line)
        # print(user2)
        # client_storage.add_client(login='Artem', password='23cvsv', friends=[])
        # client_storage.add_client(login='Vera', password='5634fd', friends=[])
        # client_storage.add_client(login='Sasha', password='dfg47', friends=[])
        # user1 = session.query(Client).filter(Client.id == 1).first()
        # user2 = session.query(Client).filter(Client.id == 3).first()
        # user3 = session.query(Client).filter(Client.id == 4).first()
        #
        # user1.friends = [user2, user3]
        # ic(user1)
        # ic(user2)
        # users = session.query(Client).all()
        # for user in users:
        #     ic(type(user.password))
        #     user.password = pbkdf2_hmac(hash_name='sha256', password=user.password.encode('utf-8'),
        #                                 salt=user.login.encode('utf-8'), iterations=100)
        #     ic(user.password)

        session.commit()
        users = session.query(Client).all()
        for user in users:
            ic(user)

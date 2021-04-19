from icecream import ic
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from pymongo import MongoClient

Base = declarative_base()

Friends = Table("Friends", Base.metadata,
                Column("left", Integer, ForeignKey("users.id")),
                Column("right", Integer, ForeignKey("users.id"))
                )


class Client(Base):
    """Client Database"""

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
        return f'Client(id={self.id}; ' \
               f'login={self.login}, ' \
               f'friends={self.friends})'

    def __repr__(self):
        return f'Client(id={self.id}; ' \
               f'login={self.login}, ' \
               f'friends={self.friends})'


class ClientStorage:
    """Class for work with client database"""

    def __init__(self, session):
        self.session = session

    def add_client(self, login, password, friends):
        """Adding a client to the database

        :type login: str
        :param login: Client's login
        :type password: str
        :param password: Client's password
        :type friends: list
        :param friends: Client's friends
        """
        try:
            with self.session.begin():
                self.session.add(
                    Client(login=login,
                           password=password,
                           friends=friends))
        except ValueError:
            print('Имя должно быть уникальным!')

    def friends(self, id):
        """Retrieving a list of user's friends

        :type id: int
        :param id: Client's id
        """
        return [friend for friend in
                self.session.query(Client)
                    .filter(Client.id == id).one().friends]

    def find(self, id):
        """Search user

        :type id: int
        :param id: Client's id
        """
        return self.session.query(Client).filter(Client.id == id).first()


class ClientHistory(Base):
    """User history"""
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
    """Working with the history of user actions"""

    def __init__(self, session):
        self.session = session

    def add_line(self, ip, client_id, status):
        """Adding a position

        :param ip: Client's ip
        :type ip: str
        :param client_id: Client's id
        :type client_id: int
        :param status: Client's status
        :type status: str
        """
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
                ClientHistory(ip=ip,
                              client_id=client_id,
                              time=date,
                              status=status)
            )


class MongoStorage:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client["messenger"]
        self.dict = db["messages"]

    def add(self, data):
        time = datetime.now()
        data["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.dict.insert_one(data)

    def get_messages(self, login, to):
        messages = self.dict.find({'$or': [
            {'$and': [{'from': login}, {'to': to}]},
            {'$and': [{'from': to}, {'to': login}]}
        ]})
        return [item for item in messages]


if __name__ == '__main__':
    engine = create_engine("sqlite:///database.db", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    mongo = MongoStorage()
    messeges = mongo.get_messages('Igor', 'Vera')
    ic(messeges)

    with Session() as session:
        client_storage = ClientStorage(session)
        history_storage = ClientHistoryStorage(session)

        session.commit()

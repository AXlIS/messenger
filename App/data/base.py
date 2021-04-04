from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, exists
from icecream import ic
from sqlalchemy.exc import IntegrityError

Base = declarative_base()


class Client(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(128))

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __str__(self):
        return f'Client(id={self.id}; login={self.login})'

    def __repr__(self):
        return f'Client(id={self.id}; login={self.login})'


class ClientStorage:
    def __init__(self, session):
        self.session = session

    def add_client(self, login, password):
        try:
            with self.session.begin():
                self.session.add(Client(login=login, password=password))
        except ValueError as e:
            raise ValueError

    def find(self, login):
        criteria = exists().where(and_(Client.login == login))
        return self.session.query(Client).filter(criteria).first() != None


if __name__ == '__main__':
    engine = create_engine("sqlite:///db.db", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        client_storage = ClientStorage(session)
        # client_storage.add_client('Oleg', password='12345')
        # for i in session.query(Client.password, Client.login).all():
        #     print(i)
        ic(client_storage.find('Igor'))

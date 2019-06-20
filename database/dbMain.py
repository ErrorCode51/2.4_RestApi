import sqlalchemy
from database.dbModels import Base
import database.dbModels as dbModels
from sqlalchemy.orm import sessionmaker

# define the type of datebase and creates a connection to it
engine =  sqlalchemy.create_engine('sqlite:///test.db', echo=True) # sqlite database in the root dir, writes the db operations to the terminal
# get the database model and write the tables to the database
from database.dbModels import Base
Base.metadata.create_all(engine)

Session = sessionmaker(bind= engine)

def selectObjectById(table, id):
    session = Session()
    return session.query(table).filter(table.id == id).first()


def selectObjectByIdUsingSession(table, id, session):
    return session.query(table).filter(table.id == id).first()


# Inserts an object and returns the given id
def insertDbObject(object):
    session = Session()
    session.add(object)
    session.flush()
    session.commit()
    return object.id
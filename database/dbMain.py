import sqlalchemy
from database.dbModels import Base
from sqlalchemy.orm import sessionmaker
import database.dbModels as dbModels

# define the type of datebase and creates a connection to it
engine =  sqlalchemy.create_engine('sqlite:///test.db', echo=True) # sqlite database in the root directory, writes the db operations to the terminal
# get the database model and write the tables to the database
Base.metadata.create_all(engine)
Session = sessionmaker(bind= engine)


def selectObjectById(table, id):
    session = Session()
    return session.query(table).filter(table.id == id).first()


def selectObjectByIdUsingSession(table, id, session):
    return session.query(table).filter(table.id == id).first()


def selectAllObjectByType(table):
    session = Session()
    return session.query(table)


# Inserts an object and returns the given id
def insertDbObject(object):
    session = Session()
    session.add(object)
    session.flush()
    session.commit()
    return object.id


def getUserByEmail(email):
    session = Session()
    return session.query(dbModels.user).filter(dbModels.user.email == email).first()


def getUserByEmailUsingSession(email, session):
    return session.query(dbModels.user).filter(dbModels.user.email == email).first()


def deleteObjectByID(table, id):
    session = Session()
    session.query(table).filter(table.id == id).delete()
    session.commit()


def getRevokedTokenByJti(jti):
    session = Session()
    return session.query(dbModels.refoked_token).filter(dbModels.refoked_token.jti == jti).first()


def getProjectsByOwnerID(id):
    session = Session()
    return session.query(dbModels.project).filter(dbModels.project.ownerId == id)

def getProjectsByParticipant(id):
    session = Session()
    u = selectObjectById(dbModels.user, id)
    return u.projects
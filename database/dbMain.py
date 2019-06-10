import sqlalchemy
from database.dbModels import Base
from sqlalchemy.orm import sessionmaker

# define the type of datebase and creates a connection to it
engine =  sqlalchemy.create_engine('sqlite:///test.db', echo=True) # sqlite database in the root dir, writes the db operations to the terminal
# get the database model and write the tables to the database
from database.dbModels import Base
Base.metadata.create_all(engine)

# Selects the data of the given type with the given id
def selectObjectById(table, id):
    type = table.__table__
    query = type.select().where(type.c.id == id)
    return engine.connect().execute(query).first()

def execInsertQuery(query):
    return engine.connect().execute(query).inserted_primary_key

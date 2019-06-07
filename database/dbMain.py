import sqlalchemy

# define the type of datebase and creates a connection to it
engine =  sqlalchemy.create_engine('sqlite:///test.db', echo=True) # sqlite database in the root dir, writes the db operations to the terminal
# get the database model and write the tables to the database
from database.dbModels import meta, exampleTable
meta.create_all(engine)

# write some data to the db for testing purposes
# ins = exampleTable.insert().values(data = 'Dit is data')
# conn = engine.connect()
# result = conn.execute(ins)

# Selects the data of the given type with the given id
def selectById(type, id):
    query = type.select().where(type.c.id == id)
    return engine.connect().execute(query).first()

# Selects all stored objects of the given type
def selectAllOffType(type):
    query = type.select()
    return engine.connect().execute(query)
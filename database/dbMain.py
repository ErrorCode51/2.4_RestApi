import sqlalchemy

# define the type of datebase and creates a connection to it
engine =  sqlalchemy.create_engine('sqlite:///test.db', echo=True) # sqlite database at TODO, and writes the db operations to the terminal
# get the database model and write the tables to the database
from database.dbModels import meta, exampleTable
meta.create_all(engine)

# write some data to the db for testing purposes
ins = exampleTable.insert().values(data = 'Dit is data')
conn = engine.connect()
result = conn.execute(ins)

def getData():
    query = exampleTable.select()
    return engine.connect().execute(query)


# In this file, the database model is defined
from sqlalchemy import MetaData, Table, Column, Integer, String

meta = MetaData()

exampleTable = Table(
    'exampleTable', meta,
    Column('id', Integer, primary_key=True),
    Column('data', String) #just a random word to test the db
)
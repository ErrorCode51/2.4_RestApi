# In this file, the database model is defined
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

meta = MetaData()

# een voorbeeld om de database mee te testen, wordt niet gebruikt in het eindproduct
# TODO: verwijderen
exampleTable = Table(
    'exampleTable', meta,
    Column('id', Integer, primary_key=True),
    Column('data', String) #just a random word to test the db
)

# a user account
user = Table(
    'user', meta,
    Column('id', Integer, primary_key=True),
    Column('userName', String(32), nullable=False),
    Column('email', String, nullable=False),
    Column('passwordHash', String, nullable=False),
    Column('profilePic', String)
)

post = Table(
    'post', meta,
    Column('id', Integer),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('title', String(128)),
    Column('message', String(1024))
)
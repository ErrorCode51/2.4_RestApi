# In this file, the database model is defined
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# a user account
class user(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    userName = Column(String(32), nullable=False)
    email = Column(String, nullable=False)
    passwordHash = Column(String, nullable=False)
    profilePic = Column(String)


# a post made by a user, similar to posts on traditional social media
class post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(128))
    message = Column(String(1024))


project_participation = Table(
    'project_participation', Base.metadata,
    Column('project_id', Integer, ForeignKey('project.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)

class project(Base):
    __tablename__  = 'project'
    id = Column(Integer, primary_key=True)                                  # a unique id
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)       # the owner of the project, will be set to the user that created the project by default
    name =Column(String, nullable=False)                                    # the name of the project
    description = Column(String)                                            # (optional), a description of the project
    participants = relationship('user', secondary= project_participation)   # the participants fo this project

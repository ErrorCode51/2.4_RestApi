# In this file, the database model is defined
from sqlalchemy import Table, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# a member of a project (not the owner)
project_participation = Table('project_participation', Base.metadata,
    Column('project_id', Integer, ForeignKey('project.id'), primary_key= True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key= True)
)

# a contact (similar to a friend on facebook or a contact on linkedin)
contact = Table('contact', Base.metadata,
        Column('user1_id', Integer, ForeignKey('user.id')),
        Column('user2_id', Integer, ForeignKey('user.id'))
)


# a post in a project, similar to a post in a facebook group
post_in_project = Table('post_in_project', Base.metadata,
        Column('post', Integer, ForeignKey('post.id')),
        Column('project', Integer, ForeignKey('project.id'))
)


# a user account
class user(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    userName = Column(String(32), nullable=False)
    email = Column(String, nullable=False, unique= True)
    passwordHash = Column(String, nullable=False)
    profilePic = Column(String)
    projects = relationship('project', secondary= project_participation)
    contacts = relationship('user', secondary= contact, primaryjoin=id==contact.c.user1_id, secondaryjoin=id==contact.c.user2_id)


# a post made by a user, similar to posts on traditional social media
class post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(128))
    message = Column(String(1024))


class project(Base):
    __tablename__  = 'project'
    id = Column(Integer, primary_key=True)                                  # a unique id
    ownerId = Column(Integer, ForeignKey('user.id'), nullable=False)        # the id of the owner of the project, will be set to the user that created the project by default
    name = Column(String, nullable=False)                                   # the name of the project
    description = Column(String)                                            # (optional), a description of the project
    participants = relationship('user', secondary= project_participation)   # the participants of this project
    # posts = relationship('post', backref= 'project')
    # TODO: link posts to projects

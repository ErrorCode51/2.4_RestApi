from flask import abort, Blueprint, request
import database.dbMain as dbMain
import database.dbModels as dbModels
import hashlib
import sqlalchemy

postBP = Blueprint('postBP', __name__)

@postBP.route('/user/', methods=['post'])
def postUser():
    return '/user/' +\
           str(dbMain.execInsertQuery(dbModels.user.__table__.insert().values(userName= request.form.get('username'),
                                                                          email= request.form.get('email'),
                                                                          passwordHash = hashlib.sha1(bytes(request.form.get('password'), 'utf-8')).hexdigest(),
                                                                          profilePic = None  #TODO: dit implementeren
                                                                         )
                                      )
               [0]), 201

@postBP.route('/project/', methods=['post'])
def postProject():
    return '/project/' +\
           str(dbMain.execInsertQuery(dbModels.project.__table__.insert().values(ownerId= int(request.form.get('owner_id')),
                                                                          name= request.form.get('project_name'),
                                                                          description = request.form.get('description')
                                                                         )
                                      )
               [0]), 201


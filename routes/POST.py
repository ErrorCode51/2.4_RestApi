from flask import abort, Blueprint, request
import database.dbMain as dbMain
import database.dbModels as dbModels
import hashlib
import sqlalchemy

postBP = Blueprint('postBP', __name__)

@postBP.route('/user/', methods=['post'])
def postUser():
    return '/user/' +\
           str(dbMain.insertDbObject(dbModels.user(userName= request.form.get('username'),
                                                   email= request.form.get('email'),
                                                   passwordHash = hashlib.sha1(bytes(request.form.get('password'), 'utf-8')).hexdigest(),
                                                   profilePic = None  #TODO: dit implementeren
                                                   )
                                     )
               ), 201

@postBP.route('/project/', methods=['post'])
def postProject():
    return '/project/' +\
           str(dbMain.insertDbObject(dbModels.project(ownerId= int(request.form.get('owner_id')),
                                                      name= request.form.get('project_name'),
                                                      description = request.form.get('description')
                                                      )
                                     )
               ), 201

@postBP.route('/project/<project_id>/participant/', methods=['post'])
def addParticipantToProject(project_id):
    s = dbMain.Session()
    p = dbMain.selectObjectByIdUsingSession(dbModels.project, project_id, s)
    u = dbMain.selectObjectByIdUsingSession(dbModels.user, int(request.form.get('user_id')), s)
    p.participants.append(u)
    s.commit()
    return '/project/' + str(project_id), 205


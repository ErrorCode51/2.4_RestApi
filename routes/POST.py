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


@postBP.route('/user/<user_id>/contact/', methods=['post'])
def addPContacts(user_id):
    contactID = int(request.form.get('contact_id'))
    s = dbMain.Session()
    u1 = dbMain.selectObjectByIdUsingSession(dbModels.user, user_id, s)
    u2 = dbMain.selectObjectByIdUsingSession(dbModels.user, contactID, s)
    if u2 not in u1.contacts and user_id != contactID:
        print('inside if statement')
        u1.contacts.append(u2)
        u2.contacts.append(u1)
        s.commit()
        return '/user/' + str(user_id), 205
    return '/user/' + str(user_id), 409


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


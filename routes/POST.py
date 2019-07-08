from flask import abort, Blueprint, request
import database.dbMain as dbMain
import database.dbModels as dbModels
import routes.account as account
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_refresh_token_required

postBP = Blueprint('postBP', __name__)

@postBP.route('/user', methods=['post'])
@jwt_refresh_token_required
def postUser():
    return '/user/' +\
           str(dbMain.insertDbObject(dbModels.user(userName= request.form.get('username'),
                                                   email= request.form.get('email'),
                                                   passwordHash = account.genPasswordHash(request.form.get('password')),
                                                   profilePic = None  #TODO: dit implementeren
                                                   )
                                     )
               ), 201


@postBP.route('/user/<user_id>/contact', methods=['post'])
@jwt_refresh_token_required
def addPContacts(user_id):
    s = dbMain.Session()
    u1 = dbMain.selectObjectByIdUsingSession(dbModels.user, user_id, s)
    u2 = dbMain.getUserByEmailUsingSession(get_jwt_identity(), s)
    if u2 not in u1.contacts and u1.id != u2.id:
        u1.contacts.append(u2)
        u2.contacts.append(u1)
        s.commit()
        s.expunge_all()
        s.close()
        return '/user/' + str(user_id), 205
    s.expunge_all()
    s.close()
    return '/user/' + str(user_id), 409


@postBP.route('/project', methods=['post'])
@jwt_refresh_token_required
def postProject():
    return '/project/' +\
           str(dbMain.insertDbObject(dbModels.project(ownerId= dbMain.getUserByEmail(get_jwt_identity()).id,
                                                      name= request.form.get('project_name'),
                                                      description = request.form.get('description')
                                                      )
                                     )
               ), 201

@postBP.route('/project/<project_id>/participant', methods=['post'])
@jwt_refresh_token_required
def addParticipantToProject(project_id):
    s = dbMain.Session()
    p = dbMain.selectObjectByIdUsingSession(dbModels.project, project_id, s)
    u = dbMain.getUserByEmailUsingSession(get_jwt_identity(), s)
    if p.ownerId != u.id and u not in p.participants:
        p.participants.append(u)
        s.commit()
    s.expunge_all()
    s.close()
    return '/project/' + str(project_id), 205

@postBP.route('/post', methods=['post'])
@jwt_refresh_token_required
def addPost():
    post = dbModels.post(user_id= dbMain.getUserByEmail(get_jwt_identity()).id,
                         title= request.form.get('title'),
                         message= request.form.get('message'))
    s = dbMain.Session()
    s.add(post)
    if request.form.get('project_id'):
        p = dbMain.selectObjectByIdUsingSession(dbModels.project, int(request.form.get('project_id')), s)
        p.posts.append(post)
    s.flush()
    s.commit()
    s.expunge_all()
    s.close()

    return '/post/' + str(post.id), 201


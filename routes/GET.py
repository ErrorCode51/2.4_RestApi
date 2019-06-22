from flask import abort, Blueprint
import database.dbMain as dbMain
import database.dbModels as dbModels
import sqlalchemy

getBP = Blueprint('getBP', __name__) # a blueprint to add all routes to, so the Flask instance can import them in one line of code

def genUserJson(user):
    if not isinstance(user, dbModels.user):
        raise AttributeError('Input is not a user object')
    return ('{"id": ' + str(user.id)
            + ', "userName": "' + user.userName
            + '", "email": "' + user.email
            + '", "passwordHash": "' + user.passwordHash
            + '", "profilePic": ' + (lambda pp: 'null' if pp == None else ('"' + pp + '"'))(user.profilePic)
            + ' }')

@getBP.route('/user/<id>/', methods=['get'])
def getUserByName(id):
    data = dbMain.selectObjectById(dbModels.user, id)
    try:
        return(genUserJson(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except AttributeError:
        abort(404)

@getBP.route('/user/email/<email>/', methods=['get'])
def getUserByEmail(email):
    data = dbMain.getUserByEmail(email)
    try:
        return(genUserJson(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except AttributeError:
        abort(404)


@getBP.route('/user/username/<username>/', methods=['get'])
def getUserById(username):
    data = dbMain.getUserByUserName(username)
    try:
        return(genUserJson(data)), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except AttributeError:
        abort(404)


@getBP.route('/project/<id>', methods=['get'])
def getProjectByID(id):
    project = dbMain.selectObjectById(dbModels.project, id)
    try:
        json = '{"id": ' + str(project.id) \
            + ', "ownerId": ' + str(project.ownerId) \
            + ', "name": "' + project.name \
            + '", "description": "' + project.description + '", '
        if project.participants:
            json += '"participants": [' \
            + ', '.join([str(u.id) for u in project.participants]) \
            + ']'
        else:
            json += '"participants": null'
        json += '}'
        return json, 200, {'Content-Type': 'application/json; charset=utf-8'}
    except AttributeError as e:
        print(e)
        abort(404)

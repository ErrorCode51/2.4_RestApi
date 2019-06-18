from flask import abort, Blueprint
import database.dbMain as dbMain
import database.dbModels as dbModels
import sqlalchemy

getBP = Blueprint('getBP', __name__) # a blueprint to add all routes to, so the Flask instance can import them in one line of code

@getBP.route('/user/<id>/', methods=['get'])
def getUserById(id):
    data = dbMain.selectObjectById(dbModels.user, id)
    print(data)
    try:
        return('{"id": ' + str(data.id)
            + ', "userName": "' + data.userName
            + '", "email": "' + data.email
            + '", "passwordHash": "' + data.passwordHash
            + '", "profilePic": ' + (lambda pp: 'null' if pp == None else ('"' + pp + '"'))(data.profilePic)
            + ' }'), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except AttributeError:
        abort(404)

@getBP.route('/project/<id>', methods=['get'])
def getProjectByID(id):
    project = dbMain.selectObjectById(dbModels.project, id)
    try:
        json = '{"id": ' + str(project.id) \
            + ', "ownerId": ' + str(project.ownerId) \
            + ', "name": "' + project.name \
            + '", "description": "' + project.description \
            + '", "participants": ['
        if len(project.participants) != 0:
            json += ', '.join([p.user.id for p in project.participants])
        json += ']'
        json += '}'
        return json, 200, {'Content-Type': 'application/json; charset=utf-8'}
    except AttributeError as e:
        print(e)
        abort(404)

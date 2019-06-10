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
            + ' }')
    except AttributeError:
        abort(404)

@getBP.route('/project/<id>', methods=['get'])
def getProjectByID(id):
    project = dbMain.selectObjectById(dbModels.project, id)
    try:
        json = '{"id": ' + str(project.id) \
            + ', "owner_id": ' + str(project.owner_id) \
            + ', "name": "' + project.name \
            + '", "description": ' + project.description
        if project.participants: # if the list of participants is not empty
            json += ', "participants": ['
            ', '.join([p.user.id for p in project.participants])
            json += ']'
        json += '}'
        return json
    except AttributeError:
        abort(404)

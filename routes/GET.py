from flask import abort, Blueprint
import database.dbMain as dbMain
import database.dbModels as dbModels

bp = Blueprint('bp', __name__) # a blueprint to add all routes to, so the Flask instance can import them in one line of code

@bp.route('/<id>/', methods=['get'])
def exampleDataById(id):
    data = dbMain.selectById(dbModels.exampleTable, id)
    try:
        return('{"id": ' + str(data.id) + ', "data": "' + data.data + '" }')
    except AttributeError:
        abort(404)

@bp.route('/', methods=['get'])
def allExampleData():
    data = dbMain.selectAllOffType(dbModels.exampleTable)
    try:
        json = '{['
        json += ','.join(['{"id": ' + str(d.id) + ', "data": "' + d.data + '" }' for d in data])
        json += ']}'
        return json
    except AttributeError as e:
        print(e)
        abort(404)

@bp.route('/user/<id>/', methods=['get'])
def userById(id):
    data = dbMain.selectById(dbModels.user, id)
    try:
        return('{"id": ' + str(data.id) + ', "userName": "' + data.userName + ', "email": "' + data.email + ', "passwordHash": "' + data.passwordHash + ', "profilePic": "' + data.profilePic + '" }')
    except AttributeError:
        abort(404)
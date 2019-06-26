from flask import abort, Blueprint, jsonify
import database.dbMain as dbMain
import database.dbModels as dbModels
import sqlalchemy

getBP = Blueprint('getBP', __name__) # a blueprint to add all routes to, so the Flask instance can import them in one line of code

def copy_without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


def toJson(jsonDict):
    jsonDict = copy_without_keys(jsonDict, ['_sa_instance_state'])
    return jsonify(jsonDict)


def getUserDict(user):
    if not isinstance(user, dbModels.user):
        raise AttributeError('Input is not a user object')
    userDict = user.__dict__
    userDict['profilePic'] = user.profilePic
    userDict['contacts'] = (lambda contacts: None if not contacts else [c.id for c in contacts])(user.contacts)
    userDict = copy_without_keys(userDict, ['_sa_instance_state'])
    return userDict


def genUserJson(user):
    if not isinstance(user, dbModels.user):
        raise AttributeError('Input is not a user object')
    userDict = getUserDict(user)
    return toJson(userDict)


@getBP.route('/user/<id>/', methods=['get'])
def getUserByID(id):
    data = dbMain.selectObjectById(dbModels.user, id)
    try:
        return(genUserJson(data), 200)
    except AttributeError as e:
        print(e)
        abort(404)


@getBP.route('/user/email/<email>/', methods=['get'])
def getUserByEmail(email):
    data = dbMain.getUserByEmail(email)
    try:
        return(genUserJson(data), 200)
    except AttributeError:
        abort(404)


@getBP.route('/user/all/', methods=['get'])
def getAllUsers():
    try:
        users = dbMain.selectAllObjectByType(dbModels.user)
        return(toJson({'users': [getUserDict(u) for u in users]}))
    except AttributeError as e:
        print(e)
        abort(404)


@getBP.route('/user/username/<username>/', methods=['get'])
def getUserByName(username):
    data = dbMain.getUserByUserName(username)
    try:
        return(genUserJson(data)), 200
    except AttributeError:
        abort(404)


@getBP.route('/post/<post_id>/', methods=['get'])
def getPostByID(post_id):
    data = dbMain.selectObjectById(dbModels.post, post_id)
    try:
        return(toJson(data.__dict__), 200)
    except AttributeError as e:
        print(e)
        abort(404)


@getBP.route('/project/<id>/', methods=['get'])
def getProjectByID(id):
    print('/project/<id>/')
    project = dbMain.selectObjectById(dbModels.project, id)
    projectDict = project.__dict__
    projectDict['participants'] = (lambda participants: None if not participants else [p.id for p in participants])(project.participants)
    print(project)
    try:
        return toJson(project.__dict__), 200
    except AttributeError as e:
        print(e)
        abort(404)

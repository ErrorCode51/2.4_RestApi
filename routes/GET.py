from flask import abort, Blueprint, jsonify
import database.dbMain as dbMain
import database.dbModels as dbModels
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_refresh_token_required
import authentication

getBP = Blueprint('getBP', __name__) # a blueprint to add all routes to, so the Flask instance can import them in one line of code

def copy_without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


def toJsonResponse(jsonDict):
    jsonDict = copy_without_keys(jsonDict, ['_sa_instance_state'])
    return jsonify(jsonDict)


def getUserDict(user, fullData=False):
    if not isinstance(user, dbModels.user):
        raise AttributeError('Input is not a user object')
    userDict = user.__dict__
    userDict['profilePic'] = user.profilePic
    userDict['contacts'] = (lambda contacts: None if not contacts else [c.id for c in contacts])(user.contacts)
    userDict = copy_without_keys(userDict, ['_sa_instance_state'])
    if not fullData:
        userDict = copy_without_keys(userDict, ['email', 'passwordHash'])
    return userDict


def genUserJson(user, fullData=False):
    if not isinstance(user, dbModels.user):
        raise AttributeError('Input is not a user object')
    userDict = getUserDict(user, fullData)
    return toJsonResponse(userDict)


@getBP.route('/user/<id>/', methods=['get'])
@jwt_refresh_token_required
def getUserByID(id):
    data = dbMain.selectObjectById(dbModels.user, id)
    getFullData = False
    if get_jwt_identity() == data.userName:
        getFullData = True
    try:
        return(genUserJson(data, getFullData), 200)
    except AttributeError as e:
        print(e)
        abort(404)


@getBP.route('/user/email/<email>/', methods=['get'])
@jwt_refresh_token_required
def getUserByEmail(email):
    data = dbMain.getUserByEmail(email)
    getFullData = False
    if get_jwt_identity() == data.userName:
        getFullData = True
    try:
        return(genUserJson(data), 200)
    except AttributeError:
        abort(404)


@getBP.route('/user/all/', methods=['get'])
@jwt_refresh_token_required
def getAllUsers():
    try:
        if not authentication.isAdmin(get_jwt_identity()):
            abort(403)
        users = dbMain.selectAllObjectByType(dbModels.user)
        return(toJsonResponse({'users': [getUserDict(u) for u in users]}))
    except AttributeError as e:
        print(e)
        abort(404)


@getBP.route('/post/<post_id>/', methods=['get'])
@jwt_refresh_token_required
def getPostByID(post_id):
    data = dbMain.selectObjectById(dbModels.post, post_id)
    try:
        return(toJsonResponse(data.__dict__), 200)
    except AttributeError as e:
        print(e)
        abort(404)


@getBP.route('/project/<id>/', methods=['get'])
@jwt_refresh_token_required
def getProjectByID(id):
    project = dbMain.selectObjectById(dbModels.project, id)
    projectDict = project.__dict__
    projectDict['participants'] = (lambda participants: None if not participants else [p.id for p in participants])(project.participants)
    projectDict['posts'] = (lambda posts: None if not posts else [p.id for p in posts])(project.posts)
    try:
        return toJsonResponse(project.__dict__), 200
    except AttributeError as e:
        print(e)
        abort(404)


@getBP.route('/project/all', methods= ['get'])
@jwt_refresh_token_required
def getAllProjects():
    projectsRaw = dbMain.selectAllObjectByType(dbModels.project)
    projects = []
    for p in projectsRaw:
        projectDict = p.__dict__
        projectDict = copy_without_keys(projectDict, ['_sa_instance_state'])
        owner = dbMain.selectObjectById(dbModels.user, p.ownerId)
        projectDict["owner"] = getUserDict(owner)
        projects.append(projectDict)
    return toJsonResponse({'projects': projects})

@getBP.route('/project/test', methods= ['get'])
def createTestProject():
    dbMain.insertDbObject(dbModels.project(ownerId=int(1),
                                           name= 'Test Project',
                                           description='This is a project'
                                           )
                          )
    return 'Created test project'

@getBP.route('/project/mine', methods= ['get'])
@jwt_refresh_token_required
def getAllUsersProjects():
    owner = dbMain.getUserByEmail(get_jwt_identity())
    projectsRaw = dbMain.getProjectsByOwnerID(owner.id)
    projects = []
    for p in projectsRaw:
        projectDict = p.__dict__
        projectDict = copy_without_keys(projectDict, ['_sa_instance_state'])
        projectDict["owner"] = getUserDict(owner)
        projects.append(projectDict)
    return toJsonResponse({'projects': projects})
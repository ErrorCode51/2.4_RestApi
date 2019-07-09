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


def getUserDict(user, fullData=False, getPosts=False):
    if not isinstance(user, dbModels.user):
        raise AttributeError('Input is not a user object')
    userDict = user.__dict__
    if not fullData:
        userDict = copy_without_keys(userDict, ['email', 'passwordHash'])
    userDict = copy_without_keys(userDict, ['_sa_instance_state'])
    if getPosts:
        userDict['posts'] = [{'id': p.id, 'title': p.title, 'message': p.message} for p in user.posts]
    userDict['profilePic'] = user.profilePic
    userDict['contacts'] = (lambda contacts: None if not contacts else [{'user_id': c.id, 'name': (c.firstName + ' ' + c.lastName)} for c in contacts])(user.contacts)
    return userDict


def genUserJson(user, fullData=False, getPosts=False):
    if not isinstance(user, dbModels.user):
        raise AttributeError('Input is not a user object')
    userDict = getUserDict(user, fullData, getPosts)
    return toJsonResponse(userDict)


@getBP.route('/user/<id>', methods=['get'])
@jwt_refresh_token_required
def getUserByID(id):
    data = dbMain.selectObjectById(dbModels.user, id)
    getFullData = False
    if get_jwt_identity() == data.email:
        getFullData = True
    try:
        user = dbMain.getUserByEmail(get_jwt_identity())

        d = getUserDict(data, getFullData, True)
        d['isContact'] = (data.id in [c.id for c in user.contacts])

        return jsonify(d)
    except AttributeError as e:
        print(e)
        abort(404)


@getBP.route('/user/email/<email>', methods=['get'])
@jwt_refresh_token_required
def getUserByEmail(email):
    data = dbMain.getUserByEmail(email)
    getFullData = False
    if get_jwt_identity() == data.email:
        getFullData = True
    try:
        return(genUserJson(data, getFullData, True), 200)
    except AttributeError:
        abort(404)


@getBP.route('/user/all', methods=['get'])
@jwt_refresh_token_required
def getAllUsers():
    try:
        users = dbMain.selectAllObjectByType(dbModels.user)
        return(toJsonResponse({'users': [getUserDict(u, False, True) for u in users]}))
    except AttributeError as e:
        print(e)
        abort(404)

@getBP.route('/user', methods=['get'])
@jwt_refresh_token_required
def getUserFromJWT():
    data = dbMain.getUserByEmail(get_jwt_identity())
    try:
        return (genUserJson(data, True, True), 200)
    except AttributeError:
        abort(404)


def genPostDict(post):
    postDict = post.__dict__
    postDict = copy_without_keys(postDict, ['_sa_instance_state'])
    postDict['author'] = getUserDict(dbMain.selectObjectById(dbModels.user, post.user_id))
    return postDict



@getBP.route('/post/<post_id>', methods=['get'])
@jwt_refresh_token_required
def getPostByID(post_id):
    data = dbMain.selectObjectById(dbModels.post, post_id)
    try:
        return(toJsonResponse(data.__dict__), 200)
    except AttributeError as e:
        print(e)
        abort(404)


def getProjectDict(project):
    projectDict = project.__dict__
    projectDict = copy_without_keys(projectDict, ['_sa_instance_state'])
    owner = dbMain.selectObjectById(dbModels.user, project.ownerId)
    projectDict["owner"] = getUserDict(owner)
    projectDict["participants"] = (lambda participants: None if not participants else [getUserDict(u) for u in participants])(project.participants)
    projectDict["posts"] = (lambda posts: None if not posts else [genPostDict(p) for p in posts])(project.posts)
    return projectDict


@getBP.route('/project/<id>', methods=['get'])
@jwt_refresh_token_required
def getProjectByID(id):
    project = dbMain.selectObjectById(dbModels.project, id)
    user = dbMain.getUserByEmail(get_jwt_identity())
    try:
        d = getProjectDict(project)
        d['isParticipating'] = (user.id in [u.id for u in project.participants])
        d['isOwner'] = (user.id == project.ownerId)
        return jsonify(d)
    except AttributeError as e:
        print(e)
        abort(404)


@getBP.route('/project/all', methods= ['get'])
@jwt_refresh_token_required
def getAllProjects():
    projectsRaw = dbMain.selectAllObjectByType(dbModels.project)
    projects = []
    for p in projectsRaw:
        projects.append(getProjectDict(p))
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
        projects.append(getProjectDict(p))
    return toJsonResponse({'projects': projects})

@getBP.route('/project/participating', methods= ['get'])
@jwt_refresh_token_required
def getParticipatingProjects():
    owner = dbMain.getUserByEmail(get_jwt_identity())
    projectsRaw = dbMain.getProjectsByOwnerID(owner.id)
    projectsRaw2 = dbMain.getProjectsByParticipant(owner.id)
    projects = []
    for p in projectsRaw:
        projects.append(getProjectDict(p))
    for p in projectsRaw2:
        projects.append(getProjectDict(p))
    return toJsonResponse({'projects': projects})
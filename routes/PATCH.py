from flask import abort, Blueprint, request, jsonify
import database.dbMain as dbMain
import database.dbModels as dbModels
import hashlib

patchBP = Blueprint('patchBP', __name__)

@patchBP.route('/user/<id>/', methods=['patch'])
def patchUserByID(id):
    try:
        s = dbMain.Session()
        u = dbMain.selectObjectByIdUsingSession(dbModels.user, id, s)
        data = request.form
        print(data)
        if 'username' in data:
            u.userName = data.get('username')
        if 'email' in data:
            u.email = data.get('email')
        if 'password' in data:
            u.passwordHash = hashlib.sha1(bytes(data.get('password'), 'utf-8')).hexdigest()
        if 'profile_pic' in data:
            u.profilePic = data.get('profile_pic')
        s.commit()
        return '', 204
    except AttributeError as e:
        print(e)
        abort(404)

@patchBP.route('/post/<id>/', methods=['patch'])
def patchPostByID(id):
    try:
        print('patch post:', id)
        s = dbMain.Session()
        p = dbMain.selectObjectByIdUsingSession(dbModels.post, id, s)
        data = request.form
        print(data)
        if 'title' in data:
            p.title = data.get('title')
        if 'message' in data:
            p.message = data.get('message')
        s.commit()
        return '', 204
    except AttributeError:
        abort(404)

@patchBP.route('/project/<id>/', methods=['patch'])
def deleteProjectByID(id):
    try:
        print('patch post:', id)
        s = dbMain.Session()
        p = dbMain.selectObjectByIdUsingSession(dbModels.project, id, s)
        data = request.form
        print(data)
        if 'project_name' in data:
            p.name = data.get('project_name')
        if 'description' in data:
            p.description = data.get('description')
        if 'owner_id' in data:
            p.ownerId = int(data.get('owner_id'))
        s.commit()
        return '', 204
    except AttributeError:
        abort(404)
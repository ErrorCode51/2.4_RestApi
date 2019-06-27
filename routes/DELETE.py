from flask import abort, Blueprint, jsonify
import database.dbMain as dbMain
import database.dbModels as dbModels

deleteBP = Blueprint('deleteBP', __name__)

@deleteBP.route('/user/<id>/', methods=['delete'])
def deleteUserByID(id):
    try:
        dbMain.deleteObjectByID(dbModels.user, id)
        return '', 204
    except AttributeError:
        abort(404)

@deleteBP.route('/post/<id>/', methods=['delete'])
def deletePostByID(id):
    try:
        dbMain.deleteObjectByID(dbModels.post, id)
        return '', 204
    except AttributeError:
        abort(404)

@deleteBP.route('/project/<id>/', methods=['delete'])
def deleteProjectByID(id):
    try:
        dbMain.deleteObjectByID(dbModels.project, id)
        return '', 204
    except AttributeError:
        abort(404)
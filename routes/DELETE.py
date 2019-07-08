from flask import abort, Blueprint
import database.dbMain as dbMain
import database.dbModels as dbModels
from flask_jwt_extended import get_jwt_identity, jwt_refresh_token_required

deleteBP = Blueprint('deleteBP', __name__)

@deleteBP.route('/user/<id>/', methods=['delete'])
@jwt_refresh_token_required
def deleteUserByID(id):
    try:
        dbMain.deleteObjectByID(dbModels.user, id)
        return '', 204
    except AttributeError as e:
        print(e)
        abort(404)

@deleteBP.route('/post/<id>/', methods=['delete'])
@jwt_refresh_token_required
def deletePostByID(id):
    try:
        dbMain.deleteObjectByID(dbModels.post, id)
        return '', 204
    except AttributeError:
        abort(404)

@deleteBP.route('/project/<id>/', methods=['delete'])
@jwt_refresh_token_required
def deleteProjectByID(id):
    try:
        dbMain.deleteObjectByID(dbModels.project, id)
        return '', 204
    except AttributeError:
        abort(404)

@deleteBP.route('/user/<user_id>/contact', methods=['delete'])
@jwt_refresh_token_required
def removeContact(user_id):
    print('remove contact')
    s = dbMain.Session()
    contact = dbMain.getUserByEmailUsingSession(get_jwt_identity(), s)
    if user_id == contact.id:
        abort(400)
    user = dbMain.selectObjectByIdUsingSession(dbModels.user, user_id, s)
    if contact not in user.contacts:
        abort(404)
    user.contacts.remove(contact)
    contact.contacts.remove(user)
    s.commit()
    return '/user/' + str(user_id), 205
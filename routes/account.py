from flask import jsonify, make_response, Flask, Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_raw_jwt, jwt_refresh_token_required, jwt_required
import hashlib
import database.dbMain as dbMain
import database.dbModels as dbModels

accountBP = Blueprint('accountBP', __name__)

def genPasswordHash(password):
    passwordHash = hashlib.sha1(bytes(request.form.get('password'), 'utf-8')).hexdigest()

@accountBP.route("/login", methods=["POST"])
def login_function():
    # Retrieves password from database. If password and user exist, hashes entered password and checks it against
    # password in database. If everything is correct, creates access- and refresh tokens and returns it to front-end
    # If anything goes wrong, a general error message is returned so user can't check if useraccounts exist
    try:
        username = request.form['username']
        password = request.form['password']
        user = dbMain.getUserByEmail(username)
        hashedPass = genPasswordHash(password)
        if hashedPass != user.passwordHash:
            response_object = incorrect_password()
            return make_response(jsonify(response_object)), 200

    except:
        response_object = general_fail_response()
        return make_response(jsonify(response_object)), 200

    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    response_object = succesfully_logged_in(user, access_token, refresh_token)
    return make_response(jsonify(response_object)), 200


@accountBP.route("/register", methods=["POST"])
def register_function(user, password, first_name, last_name, job, skill):
    # Checks if user already exists in database. If so, returns error message.
    #  Next, it hashes the password
    # and enters account information in database. It will then return a success message to the front end. If anything
    # goes wrong, either in the SQL or in token creation, it will generate an error message
    user = request.form['username']
    password = request.form['password']
    first_name = request.form['firstname']
    last_name = request.form['lastname']
    job = request.form['job']
    skill = request.form['skill']

    data = dbMain.getUserByEmail(user)
    if data:
        response_object = user_exists()
        return make_response(jsonify(response_object)), 200

    try:
        dbMain.insertDbObject(dbModels.user(email= user,
                                            passwordHash= genPasswordHash(password),
                                            firstName= first_name,
                                            lastName= last_name,
                                            job= job,
                                            skill= skill))

        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        response_object = successfully_registered(access_token, refresh_token)
        return make_response(jsonify(response_object)), 200

    except:
        response_object = general_fail_response()
        return make_response(jsonify(response_object)), 200

@accountBP.route("/verifyLogin", methods=["POST"])
@jwt_refresh_token_required
def verify_login():
    # Since this method is only reachable if you're logged in, will return success manage if you access it.
    response_object = {
        'status': 'Success',
        'message': "Login verified"
    }
    return make_response(jsonify(response_object)), 200

def refresh_token_function(current_user):
    # Refreshes token
    access_token = create_access_token(identity=current_user)
    response_object = {
        'status': 'Success',
        'message': access_token
    }
    return make_response(jsonify(response_object)), 200


@accountBP.route("/logout/access", methods=["POST"])
@jwt_required
def logout_access_function():
    # Adds login token to revoked tokens in database and logs user out
    jti = get_raw_jwt()['jti']
    try:
        add_token(jti)
        response_object = {
            'status': 'Success',
            'message': 'Access token has been revoked'
        }
        return make_response(jsonify(response_object)), 200
    except:
        response_object = {
            'status': 'Fail',
            'message': 'Something went wrong'
        }
        return make_response(jsonify(response_object)), 200

@accountBP.route("/logout/refresh", methods=["POST"])
@jwt_refresh_token_required
def logout_refresh_function():
    # Adds login token to revoked tokens in database and logs user out
    jti = get_raw_jwt()['jti']
    try:
        add_token(jti)
        response_object = {
            'status': 'Success',
            'message': 'Refresh token has been revoked'
        }
        return make_response(jsonify(response_object)), 200
    except:
        response_object = {
            'status': 'Fail',
            'message': 'Something went wrong'
        }
        return make_response(jsonify(response_object)), 200


def incorrect_password():
    # Generates generic incorrect password responseObject
    response_object = {
        'status': 'Fail',
        'message': "Gebruiker bestaat niet en/of er is een verkeerd wachtwoord ingevoerd."
    }
    return response_object


def succesfully_logged_in(user, access_token, refresh_token):
    # Generates a 'success' responseObject
    response_object = {
        'status': 'Success',
        'message': "U bent nu ingelogd als {}".format(user),
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return response_object


def user_exists():
    # Will return 'userExists' responseObject
    response_object = {
        'status': 'Fail',
        'message': 'Gebruiker bestaat al.',
    }
    return response_object


def successfully_registered(access_token, refresh_token):
    # Generates a 'succes' responseObject and the two login_tokens
    response_object = {
        'status': 'success',
        'message': 'Registreren gelukt! Er is een email verzonden naar uw adres waarmee u uw account kunt activeren.',
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return response_object


def general_fail_response():
    # Generates generic failure responseObject
    response_object = {
        'status': 'Fail',
        'message': "Er is iets verkeerd gegaan."
    }
    return response_object


def add_token(token):
    # Adds revoked token to database
    dbMain.insertDbObject(dbModels.refoked_token(jti= token))
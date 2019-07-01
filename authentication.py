from flask_jwt_extended import verify_jwt_in_request, JWTManager
import configparser

def setupAuth(app):
    global c
    c = configparser.ConfigParser()
    c.read('auth.conf')
    app.config['JWT_SECRET_KEY'] = c.get('Auth', 'Secret_Key')
    app.config['JWT_HEADER_NAME'] = c.get('Auth', 'Header_Name')
    jwt = JWTManager(app)

def isAdmin(name):
    return name in [i.strip() for i in c.get('Auth', 'Admins')]
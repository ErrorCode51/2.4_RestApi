from flask_jwt_extended import verify_jwt_in_request, JWTManager
import configparser
import datetime

jwt = None

def setupAuth(app):
    global c
    c = configparser.ConfigParser()
    c.read('auth.conf')
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['JWT_SECRET_KEY'] = c.get('Auth', 'Secret_Key')
    app.config['JWT_HEADER_NAME'] = c.get('Auth', 'Header_Name')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=18)
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    global jwt
    jwt = JWTManager(app)

def isAdmin(name):
    return name in [i.strip() for i in c.get('Auth', 'Admins')]
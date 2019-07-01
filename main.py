from flask import Flask
import authentication
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
authentication.setupAuth(app)


from routes.GET import getBP
from routes.POST import postBP
from routes.DELETE import deleteBP
from routes.PATCH import patchBP
from routes.account import accountBP

app.register_blueprint(getBP)
app.register_blueprint(postBP)
app.register_blueprint(deleteBP)
app.register_blueprint(patchBP)
app.register_blueprint(accountBP)


app.run()

# TODO: security with JWT's or api keys
# TODO: add documentation
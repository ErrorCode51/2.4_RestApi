from flask import Flask
from routes.GET import getBP
from routes.POST import postBP
from routes.DELETE import deleteBP
from routes.PATCH import patchBP
import authentication

app = Flask(__name__)
app.register_blueprint(getBP)
app.register_blueprint(postBP)
app.register_blueprint(deleteBP)
app.register_blueprint(patchBP)

authentication.setupAuth(app)

app.run()

# TODO: security with JWT's or api keys
# TODO: add documentation
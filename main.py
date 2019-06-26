from flask import Flask
from routes.GET import getBP
from routes.POST import postBP

app = Flask(__name__)
app.register_blueprint(getBP)
app.register_blueprint(postBP)

app.run()
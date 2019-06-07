from flask import Flask
import routes.GET as get

app = Flask(__name__)
app.register_blueprint(get.bp)
app.run()
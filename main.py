from flask import Flask, abort
import database.dbMain as dbMain

app = Flask(__name__)

# TODO: routes in een apart bestand zetten
@app.route('/<id>/')
def hello_world(id):
    data = dbMain.getData(id)
    try:
        return('{"id": ' + str(data.id) + ', "data": "' + data.data + '" }')
    except AttributeError:
        abort(404)

app.run()
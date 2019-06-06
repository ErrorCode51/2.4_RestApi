from flask import Flask
import database.dbMain as dbMain

app = Flask(__name__)

# TODO: routes in een apart bestand zetten
@app.route('/')
def hello_world():
    data = dbMain.getData()
    string = ""
    for d in data:
        string += d.data
    return(string)

app.run()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from flask_pymongo import PyMongo
from bson.json_util import loads, dumps
from needed_functions import *
from secret import *

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "secret!"
#app.config["MONGO_URI"] = "mongodb://localhost:27017/MESSAGE"
app.config["MONGO_URI"] = f"mongodb+srv://{username}:{secret}@samiz-depression.crz8nwr.mongodb.net/MESSAGE"
socketio = SocketIO(app=app)
mongo = PyMongo(app=app)


#######Message plot#####
@app.route("/")
def main_page():
    return render_template("index.html")


@socketio.on("join")
def status(e):
    messages = mongo.db.ALL.find(projection={"_id":False})
    messages = loads(dumps(messages))
    emit('status', messages)
    print("Past message sending...")
    print("Passed...")

@socketio.on("message")
def message_handeler(message):
    print(message)
    ques = question_mark_traker(data=message)
    if  ques == True:
        emit("message", message, broadcast=True)
        mongo.db.ALL.insert_one(message)
        print("Succesfully insert....")
        print("Present message sending...") 
        print("Passed...")
    else:
        emit('message', {"dep":2,"msg":"In your text, first sentence should contain a question of more than three words for depressed message. On the otherhand, solution needs more than three words for the first line."}, broadcast=True)

######Model building plot####
@app.route("/data_for_Model")
def data_for_model():
    return render_template("data_collection.html")

@socketio.on("depression", namespace='/data_for_Model')
def depression(message_depressed):
    emit("depression", message_depressed['msg'], broadcast=True)
    mongo.db.DEPRESSION_DATA.insert_one(message_depressed)
    print("passed....")
    


if __name__ == "__main__":
    socketio.run(app, port=1235)
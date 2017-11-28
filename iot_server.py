import pyrebase
import json
config = {
    'apiKey': "AIzaSyBzAIpzG7fZPYZdqyuKBFsfzoFZj7wwDzY",
    'authDomain': "pjnw2017.firebaseapp.com",
    'databaseURL': "https://pjnw2017.firebaseio.com",
    'projectId': "pjnw2017",
    'storageBucket': "pjnw2017.appspot.com",
    'messagingSenderId': "360303746926"
  }
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def push_data(data):
    djs = json.loads(data)
    if str(type(djs)) == "<class 'dict'>":
        if 'location' in djs.keys():
            db.child("Logging").child(djs['location']).push(djs)
            return djs
    else:
        return False
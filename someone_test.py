from flask import render_template, request, Flask
from pymongo import MongoClient
import re

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client["test"]

list_collections = []
list_collections = db.collection_names()
print(list_collections)


@app.route('/', methods=['post', 'get'])
def index():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_passwd = request.form.get('password')
        print(user_email, user_passwd)
        new_collection = re.sub(r"[@.]", "", user_email)
        print(new_collection)
        if new_collection in db.collection_names():
            return {"false email"}
        else:
            users = db[new_collection]
            req = {
                "username": new_collection,
                "email": user_email,
                "password": user_passwd
            }
            users.db.insert_one(req)
            global list_collections
            list_collections = db.collection_names()
            print(list_collections)
        return {"status": "ok", "username": new_collection}
    return render_template('reg.html')


# @app.route('/auth', methods=['post', 'get'])
# def auth():
#     if request.method == 'post':
#         user_email = requests.args.get('email')
#         user_passwd = requests.args.get('password')
#         get_collections = re.sub(r"[@.]", "", user_email)
#         if get_collections in db.collection_names():
if __name__ == '__main__':
    app.run(debug=True)

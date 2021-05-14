from flask import Flask, request, render_template
from certificate import certificate
from dogovor import dogovor
from pymongo import MongoClient
from bson import ObjectId
import re

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client["test"]
user = db.users
post = db.posts

list_collections = []
list_collections = db.collection_names()
# print(list_collections)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/gen_certificate', methods=['post', 'get'])
def gen_certificate():
    d1 = 0
    d2 = 0
    if request.method == 'POST':
        name = request.form.get('program')
        fio = request.form.get('FullName')
        d1 = request.form.get("date1")
        d2 = request.form.get("date2")
        choose = request.form.get("browser")
        certificate(name, fio, d1, d2, choose)
    return render_template("certificate.html")


@app.route('/gen_dogovor', methods=['post', 'get'])
def gen_dogovor():
    if request.method == 'POST':
        choose = request.form.get("browser")
        fio = request.form.get('fio')
        fio2 = request.form.get('fio2')
        klass = request.form.get('klass')
        programa = request.form.get('program')
        direction = request.form.get('direction')
        telephone = request.form.get('telephone')
        telephone2 = request.form.get('telephone2')
        date = request.form.get('date')
        dogovor(choose, fio, fio2, klass, programa, direction, date, telephone2, telephone)
    return render_template('dogovor.html')


@app.route('/reg', methods=['post', 'get'])
def reg():
    if request.method == 'POST':
        email = request.form.get('email')
        passwd = request.form.get('password')
        new_collection = re.sub(r"[@.]", "", email)
        print(new_collection)
        if new_collection in db.collection_names():
            return {"false email"}
        else:
            users = db[new_collection]
            req = {
                "username": new_collection,
                "email": email,
                "password": passwd
            }
            users.insert_one(req)
            global list_collections
            list_collections = db.collection_names()
            print(list_collections)
        return {"status": "ok", "email": new_collection}
    return render_template('registration.html')


@app.route('/auth', methods=['post', 'get'])
def auth():
    if request.method == 'POST':
        user_password = request.form.get('password')
        user_email = request.form.get('email')
        get_collections = re.sub(r"[@.]", "", user_email)
        print(user_password, user_email)
        if get_collections in db.collection_names():
            users = db[get_collections]
            print(users.email, users.password)
            if users.email == user_email and users.password == user_password:
                return "successfully"
            else:
                return "error"
        #     return "successfully"
        # else:
        #     return "wrong password or email"
    return render_template('auth.html')


@app.route('/view')
def view():
    return render_template('view.html', users=db.users.find())


@app.route('/del_user/<user_id>', methods=['post', 'get'])
def del_user(user_id):
    res = db.users.delete_one({"_id": ObjectId(user_id)})
    # print(res)
    users = db.users.find()
    return render_template('view.html', users=db.users.find())


print(db.collection_names())


if __name__ == '__main__':
    app.run(debug=True)

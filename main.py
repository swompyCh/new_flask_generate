from flask import Flask, request, render_template
from certificate import certificate
from dogovor import dogovor
from pymongo import MongoClient
from bson import ObjectId
import re



app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client["test"]

# list_collections = []
# list_collections = db.collection_names()
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
        user_email = request.form.get('email')
        user_passwd = request.form.get('pass')
        print(user_passwd, user_email)
        new_collection = re.sub(r"[@.]", "", user_email)
        if new_collection in db.collection_names():
            return {"status": "false_email"}
        else:
            users = db[new_collection]
            req = {
                "username": new_collection,
                "name": "",
                "email": user_email,
                "password": user_passwd
            }
            users.insert_one(req)
            global list_collections
            list_collections = db.collection_names()
            print(list_collections)
        return {"status": "ok", "username": new_collection}
    return render_template('registration.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_passwd = request.form.get('pass')
        get_collection = re.sub(r"[@.]", "", user_email)
        print(user_email, user_passwd)
        if get_collection in db.collection_names():
            users = db[get_collection]
            for user in users.find():
                print(user['password'], user['email'])
            for user in users.find():
                if user['email'] == user_email and user['password'] == user_passwd:
                    return "success"
                else:
                    return "error"
        else:
            render_template('auth.html')
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

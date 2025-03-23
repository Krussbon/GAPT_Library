from flask import Flask, render_template, request, redirect
import bcrypt
import os
import json

app = Flask(__name__)

# Create a dictionary for the pairs
empas = dict()
requests = dict()

# Load the existing database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.json')
with open(db_path, "r") as file:
    empas = json.load(file)
requests_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pending.json')
with open(requests_path, "r") as file:
    requests = json.load(file)

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        login_email = request.form.get('loginemail', '')
        login_pswd = request.form.get('loginpassword', '').encode("utf-8")
        
        if len(login_email) > 0:
            if login_email in empas.keys():
                if bcrypt.checkpw(login_pswd, empas[login_email].encode("utf-8")):
                    return redirect("/granted")
                else:
                    return redirect("/denied")
        
        signup_email = request.form.get('signupemail', '')
        signup_pswd = request.form.get('signuppassword', '').encode("utf-8")
        if len(signup_email) > 0:
            if signup_email in empas.keys():
                print("Account is already made")
            else:
                s = bcrypt.gensalt()
                requests[signup_email] = bcrypt.hashpw(signup_pswd, s).decode("utf-8")
                
                with open(requests_path, "w") as file:
                    json.dump(requests, file)
                print("Signup request added:", requests)

    return render_template("login.html")
@app.route("/repo")
def repo():
    return render_template("repository.html")
@app.route("/granted")
def granted():
    return render_template("granted.html")

@app.route("/denied")
def denied():
    return render_template("denied.html")
@app.route("/upload")
def upload():
    return render_template("Upload.html")
@app.route("/thx")
def thank_you():
    return render_template("thankyou.html")
@app.route("/thx4upl")
def thank_you_for_uploading():
    return render_template("thankyou4uploading.html")

@app.route("/access_request")
def access_request():
    return render_template("AccessRequests.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0")

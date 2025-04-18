from flask import Flask, render_template, request, redirect,abort,session
from flask_login import UserMixin

import os
import psycopg2
from dotenv import load_dotenv
import bcrypt
import os
import json
import secrets
from werkzeug.utils import secure_filename

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
app = Flask(__name__)
load_dotenv()
app.secret_key = os.environ.get('FLASK_SECRET_KEY',secrets.token_hex(64))
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5234,
        dbname="AcaRep",
        user="postgres",
        password=""  
            )
    print("✅ Connection successful")
except Exception as e:
    print(f"❌ Connection failed: {e}")
# Create a dictionary for the pairs
empas = dict()
requests = dict()
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres@localhost:5234/AcaRep'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
class File(db.Model):
    __tablename__ = "file"
    __table_args__ = {'schema': 'UMRepo'} 
    file_id = db.Column(db.Integer,primary_key=True,unique=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    uploader = db.Column(db.Integer,ForeignKey('UMRepo.User.user_id'))
    upload_date = db.Column(db.Date)
    cat_id = db.Column(db.Integer)
    accessibility = db.Column(db.String(50))
    path = db.Column(db.String(255))

    
class User(db.Model,UserMixin):
    __tablename__ = "User"
    __table_args__ = {'schema': 'UMRepo'} 
    user_id = db.Column(db.Integer,primary_key=True,unique=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    pass_hash= db.Column(db.Text)
    status = db.Column(db.String(20))
    RoleId = db.Column(db.Integer)
class Pending(db.Model,UserMixin):
    __tablename__ = "pending"
    __table_args__ = {'schema': 'UMRepo'} 
    user_id = db.Column(db.Integer,primary_key=True,unique=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    pass_hash= db.Column(db.Text)
    RoleId = db.Column(db.Integer)
REPO_FOLDER = os.getenv('REPO_FOLDER')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'pptx', 'zip'}
MAX_FILE_SIZE = 10 * 1024 * 1024 


# Load the existing database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.json')
with open(db_path, "r") as file:
    empas = json.load(file)
requests_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pending.json')
with open(requests_path, "r") as file:
    requests = json.load(file)
@app.route('/index')
def index():
    print(session)
    return render_template("index.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    
    if request.method == 'POST':
        login_email = request.form.get('loginemail', '')
        login_pswd = request.form.get('loginpassword', '').encode("utf-8")
        find_record = (f"""select * from "UMRepo"."User" where email=%s;""")
        cursor = conn.cursor()
        cursor.execute(find_record,(login_email,))
        ls = cursor.fetchone()
        print(ls)
        if len(login_email) > 0:
            
            if bcrypt.checkpw(login_pswd, ls[3].encode("utf-8")):
                session["user_id"]=ls[5]
                session["name"]=ls[0]
                session["surname"]=ls[1]
                session["email"]=ls[2]
                session["RoleID"]=ls[6]
                session.permanent=False
                print(session)
                return redirect("/granted")
            else:
                 return redirect("/denied")
        
        s = bcrypt.gensalt()
        signup_name = request.form.get('signupname', '')
        signup_surname = request.form.get('signupsurname', '')
        signup_email = request.form.get('signupemail', '')
        signup_hashpswd = bcrypt.hashpw(request.form.get('signuppassword', '').encode("utf-8"), s).decode("utf-8")
        if len(signup_email) > 0:
            if signup_email in empas.keys():
                print("Account is already made")
            else:
                new_record = (f"""Insert into "UMRepo"."pending"("Name","Surname","email","Pass_Hash","RoleID")
              
                values (%s,%s,%s,%s,%s);""")
        
        
                cursor=conn.cursor()
                role_id = 0
                if signup_email.split("@")[0].isalnum():
                    role_id=1
                else:
                    role_id=2
                insert_value=(signup_name,signup_surname,signup_email,signup_hashpswd,role_id)
                cursor.execute(new_record,insert_value)
                conn.commit()
                with open(requests_path, "w") as file:
                    json.dump(requests, file)
                print("Signup request added:", requests)

    return render_template("login.html")
@app.route("/repo")
def repo():
    find_record = (f"""select * from "UMRepo"."file" """)
    cursor = conn.cursor()
    cursor.execute(find_record)
    files = cursor.fetchall()
    return render_template("repository.html",files=files)
@app.route("/granted")
def granted():
    return render_template("granted.html")
@app.route("/denied")
def denied():
    return render_template("denied.html")
@app.route("/upload",methods=["POST","GET"])
def upload():
    if session['RoleID'] and (session['RoleID']==2 or session['RoleID']==3):
        if request.method == "GET":
            return render_template("Upload.html")
        if request.method == "POST":
            
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            cat_id = request.form.get('material_type', '').strip()
            
            accessibility = request.form.get('accessibility', '').strip()
            file = request.files['file']
            subject_category = request.form.get('subject_category','').strip()
            if 'file' not in request.files or request.files['file'].filename == '':
                return "No File Uploaded",400
            try:
                uploader_id = session['user_id']
            except ValueError:
                return "Invalid uploader ID", 400

                # Parse upload date
            try:
                    upload_date =request.form['upload_date']
            except ValueError:
                return "Invalid date format (YYYY-MM-DD required)", 400
            path = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
            
            new_record = (f"""Insert into "UMRepo"."file"(name,description,path,uploader,upload_date,visibility,cat_id,subject_category)
                
            values (%s,%s,%s,%s,%s,%s,%s,%s);""")
            
            
            cursor=conn.cursor()
            insert_value=(name,description,path,uploader_id,upload_date,accessibility,cat_id,subject_category)
            cursor.execute(new_record,insert_value)
            conn.commit()
            
            
            file.save(path)
            return redirect("/thx4upl")
    else:
        return abort(403)
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html',reason="Only teachers and librarians are allowed"),403
@app.route("/thx")
def thank_you():
    return render_template("thankyou.html")
@app.route("/thx4upl")
def thank_you_for_uploading():
    return render_template("thankyou4uploading.html")

@app.route("/access_request")
def access_request():
    if session['RoleID']  and session['RoleID']==3:
        cursor = conn.cursor()
        find_record = (f"""select * from "UMRepo"."pending";""")
        cursor.execute(find_record)
        pending = cursor.fetchall()
        print(pending)
        return render_template("AccessRequests.html",pending=pending)
    else:
        return abort(403)
@app.route("/handle_request",methods=["POST"])
def handle_request():
    id = request.form.get('request_id')
    action = request.form.get('action')
    
    select_record = (f"""select * from "UMRepo".pending where user_id = %s;""")
    new_record = (f"""Insert into "UMRepo"."User"("Name","Surname","email","Pass_Hash","RoleID")
            values (%s,%s,%s,%s,%s);""")
    del_record = (f"""Delete From "UMRepo"."pending" where user_id = %s;""")
    get_records = (f"""select * from "UMRepo"."pending";""")
    cursor = conn.cursor()
    cursor.execute(select_record,(id,))
    rec = cursor.fetchone()
    print(rec)
    if action =='accept':
        cursor.execute(new_record,(rec[0],rec[1],rec[2],rec[3],rec[5]))
        conn.commit()
    cursor.execute(del_record,(id,))
    conn.commit()
    cursor.execute(get_records)
    return redirect("/access_request")
if __name__ == '__main__':
    app.run(host="0.0.0.0")

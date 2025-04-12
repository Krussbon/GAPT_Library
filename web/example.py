from flask import Flask, render_template, request, redirect,jsonify
import os
import psycopg2
from dotenv import load_dotenv
import bcrypt
import os
import json
import time
import datetime
from werkzeug.utils import secure_filename
import logging
import psycopg2.sql
app = Flask(__name__)
load_dotenv()
# Create a dictionary for the pairs
empas = dict()
requests = dict()


REPO_FOLDER = os.getenv('REPO_FOLDER', 'repo')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'pptx', 'zip'}
MAX_FILE_SIZE = 10 * 1024 * 1024 
new_record = (f"""Insert into "UMRepo"."file"(Name,Description,Path,Uploader,upload_date,Visibility,cat_id)
              
values (%s,%s,%s,%s,{datetime.datetime.now()},%s,%s);""")

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
@app.route("/upload",methods=["POST","GET"])
def upload():
    if request.method == "GET":
        return render_template("Upload.html")

    data = request.form
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        file = request.files['file']
        logging.debug(f"Received data: {data}")
        filename = secure_filename(file.filename)
        filepath = os.path.join(REPO_FOLDER, filename)
        os.makedirs(REPO_FOLDER,exist_ok=True)
        file.save(filepath)
        with psycopg2.connect(os.getenv('DATABASE_URL')) as connection:
            with connection.cursor() as cursor:
                query=psycopg2.sql.SQL("""Insert into "UMRepo"."file"(Name,Description,Path,Uploader,upload_date,Visibility,cat_id)
                values (%s,%s,%s,%s,%s,%s,%s) RETURNING file_id, Name, Path;""")
                cursor.execute(query,(
                    data['name'],
                    data['description'],
                    filepath,
                    data['uploader'],
                    datetime.datetime.now(),
                    data['accessibility'],
                    data['subject_category'],
                ))
                
                result = cursor.fetchone()
                file_id,stored_name,path = result
                
                
                
                return jsonify({
                    "message": "Data retrieved successfully",
                    "file_id": file_id,
                    "stored_name": stored_name,
                    "path": path
                }), 200

    except psycopg2.errors.UniqueViolation as e:
        return jsonify({"error": "Duplicate entry"}), 409
    except psycopg2.errors.ForeignKeyViolation as e:
        return jsonify({"error": "Invalid reference"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
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

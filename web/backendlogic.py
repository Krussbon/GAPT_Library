from flask import Flask, render_template, request, redirect,abort,session,send_from_directory,url_for
from flask_login import UserMixin

import os
import psycopg2
from dotenv import load_dotenv
import bcrypt
import os
import json
import secrets
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
app = Flask(__name__)
load_dotenv()
app.secret_key = os.environ.get('FLASK_SECRET_KEY',secrets.token_hex(64))

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="acarep",
    user="postgres",
    password="0000"
)
print("✅ Connection successful")


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
class Favourite(db.Model):
    __tablename__ = "favourites"
    __table_args__ = {'schema': 'UMRepo'}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('UMRepo.User.user_id'))
    file_id = db.Column(db.Integer, ForeignKey('UMRepo.file.file_id'))

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
            if ls is None:
                return redirect("/denied")
            
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
                if any(char.isdigit() for char in signup_email.split('@')[0]):
                    role_id=1
                else:
                    role_id=2
                if signup_email.split('@')[1] != "um.edu.mt":
                    return redirect("/denied")
                insert_value=(signup_name,signup_surname,signup_email,signup_hashpswd,role_id)
                cursor.execute(new_record,insert_value)
                conn.commit()
                with open(requests_path, "w") as file:
                    json.dump(requests, file)
                print("Signup request added:", requests)
            return redirect("/thx")

    return render_template("login.html")
@app.route("/repo", methods=["POST", "GET"])
def repo():
    cursor = conn.cursor()

    # Fetch categories
    cursor.execute('SELECT * FROM "UMRepo"."Category"')
    categories = cursor.fetchall()

    favs = []
    user_id = session.get("user_id")
    files = []

    # Fetch user's favourite file_ids
    if user_id:
        cursor.execute('SELECT "file_id" FROM "UMRepo"."favourites" WHERE user_id = %s', (user_id,))
        favs = [row[0] for row in cursor.fetchall()]

    # Start base query
    base_query = '''
        SELECT file.*, u."Name"
        FROM "UMRepo"."file" AS file
        JOIN "UMRepo"."User" AS u ON u.user_id = file.uploader
    '''

    conditions = []
    values = []

    # Filters (POST search)
    if request.method == "POST":
        search = request.form.get("search_images")
        mat_type = request.form.get("material_type")
        is_favs = request.form.get("favourites") == 'on'

        if is_favs and user_id:
            base_query += ' JOIN "UMRepo"."favourites" fav ON fav.file_id = file.file_id'
            conditions.append("fav.user_id = %s")
            values.append(user_id)

        if search:
            conditions.append("levenshtein(file.name, %s) < 3")
            values.append(search)

        if mat_type:
            conditions.append("file.cat_id = %s")
            values.append(mat_type)

    # Visibility logic
    if not user_id:
        conditions.append('file.visibility = %s')
        values.append("Open Access")
    else:
        role = session.get("RoleID")
        if role == 3:
            pass  # Librarian sees all files
        elif role == 2:  # Teacher
            conditions.append('''(
                file.visibility = %s OR 
                file.visibility = %s OR 
                file.file_id IN (
                    SELECT file_id FROM "UMRepo"."file_access" WHERE user_id = %s
                ) OR 
                file.uploader = %s
            )''')
            values.extend(["Open Access", "University Only", user_id, user_id])
        else:  # Students
            conditions.append('''(
                file.visibility = %s OR 
                file.file_id IN (
                    SELECT file_id FROM "UMRepo"."file_access" WHERE user_id = %s
                )
            )''')
            values.extend(["Open Access", user_id])

    # Final query
    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    final_query = base_query + where_clause + ";"

    cursor.execute(final_query, tuple(values))
    files = cursor.fetchall()

    return render_template("repository.html", files=files, categories=categories, favs=favs)



@app.route("/granted")
def granted():
    return render_template("granted.html")
@app.route("/denied")
def denied():
    return render_template("denied.html")
@app.route('/assign_access/<int:file_id>', methods=["GET", "POST"])
def assign_access(file_id):
    if session.get('RoleID') < 2: 
        return abort(403)

    cursor = conn.cursor()

    if request.method == "POST":
        selected_users = request.form.getlist("allowed_users")
        for user_id in selected_users:
            cursor.execute('INSERT INTO "UMRepo"."file_access"(file_id, user_id) VALUES (%s, %s)', (file_id, user_id))
        conn.commit()
        return redirect('/repo')

    
    cursor.execute('SELECT user_id, "Name", "Surname" FROM "UMRepo"."User" WHERE "RoleID" = 1 OR "RoleID" = 2')
    students = cursor.fetchall()

    return render_template("assign_access.html", file_id=file_id, students=students)

@app.route("/upload",methods=["POST","GET"])
def upload():
    if session['RoleID'] and (session['RoleID']==2 or session['RoleID']==3):
        if request.method == "GET":
            return render_template("Upload.html")
        if request.method == "POST":
            
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            cat_id = int(request.form.get('material_type', '0').strip())
            
            accessibility = request.form.get('accessibility', '').strip()
            print(accessibility)
            file = request.files['file']
            subject_category = request.form.get('subject_category','').strip()
            if 'file' not in request.files or request.files['file'].filename == '':
                return "No File Uploaded",400
            # try:
            #     uploader_id = session['user_id']
            # except ValueError:
            #     return "Invalid uploader ID", 400

                # Parse upload date
            try:
                    upload_date =request.form['upload_date']
            except ValueError:
                return "Invalid date format (YYYY-MM-DD required)", 400
            path = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(name))
            
            new_record = (f"""Insert into "UMRepo"."file"(name,description,path,uploader,upload_date,visibility,cat_id,subject_category)
                
            values (%s,%s,%s,%s,%s,%s,%s,%s);""")
            uploader_id=session['user_id']
            
            cursor=conn.cursor()
            
            insert_value=(name,description,path,uploader_id,upload_date,accessibility,cat_id,subject_category)
            cursor.execute(new_record,insert_value)
            conn.commit()

            
            
            file.save(path)
            find_records=(f"""Select * from "UMRepo"."Attributes" where cat_id=%s """)
            new_record = (f"""Insert into "UMRepo"."file_attributes"(file_id,attr_id,value)
                          values(%s,%s,%s);""")
            attrs=[]
            cursor.execute(find_records,(cat_id,))
            recs = cursor.fetchall()
            cursor.execute("""select max(file_id) from "UMRepo"."file"  """)
            new_cat_id = int(request.form['material_type'])
            maximum = cursor.fetchone()[0]
            start = 1
            attrs = []

            if new_cat_id == 1:
                start = 1
                attrs = [request.form.get(k) for k in ["Course Name", "Lecturer Name", "Semester", "Year", "Topic"]]
            elif new_cat_id == 2:
                start = 6
                attrs = [request.form.get(k) for k in ["Course Name", "Assignment Number", "Due Date", "Instructor Name", "Year"]]
            elif new_cat_id == 3:
                start = 23
                attrs = [request.form.get(k) for k in ["Course Name", "Exam Type", "Year", "Due Date", "Instructor", "Duration"]]
            elif new_cat_id == 4:
                start = 39
                attrs = [request.form.get(k) for k in ["Title", "Authors", "Publication Year", "Journal/Conference Name"]]
            elif new_cat_id == 5:
                start = 11
                attrs = [request.form.get(k) for k in ["Experiment Title", "Subject", "Instructor", "Lab Partners"]]
            elif new_cat_id == 6:
                start = 16
                attrs = [request.form.get(k) for k in ["Title", "Student Name", "Supervisor", "Department", "Year", "Abstract", "Degree Level"]]
            elif new_cat_id == 7:
                start = 33
                attrs = [request.form.get(k) for k in ["Course Name", "Instructor", "Duration", "Topic", "Title"]]
            elif new_cat_id == 8:
                start = 28
                attrs = [request.form.get(k) for k in ["Title", "Speaker Name", "Course Name", "Date Presented", "Topic"]]
            cursor.execute('SELECT MAX(file_id) FROM "UMRepo"."file"')
            file_id = cursor.fetchone()[0]
            new_record = '''INSERT INTO "UMRepo"."file_attributes"(file_id, attr_id, value) VALUES (%s, %s, %s);'''
            for i, value in enumerate(attrs):
                cursor.execute(new_record, (file_id, start + i, value))

            conn.commit()
            


                

            print(recs)
            if accessibility == "Restricted":
                cursor.execute('SELECT MAX(file_id) FROM "UMRepo"."file" WHERE uploader = %s', (uploader_id,))
                file_id = cursor.fetchone()[0]
                return redirect(url_for('assign_access', file_id=file_id))

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

# @app.route("/access_request")
# def access_request():
#     if session['RoleID']  and session['RoleID']==3:
#         cursor = conn.cursor()
#         find_record = (f"""select * from "UMRepo"."pending";""")
#         cursor.execute(find_record)
#         pending = cursor.fetchall()
#         print(pending)
#         return render_template("AccessRequests.html",pending=pending)
#     else:
#         return abort(403)
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
@app.route('/403')
def forbidden():
    return render_template('403.html'), 403

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/help_page')
def help_page():
    return render_template('help.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/index')

@app.route('/download/<filepath>')
def download(filepath):
    filename = filepath.split("\\")[-1]
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/filter/<int:type>')
def filter(type):
    cursor = conn.cursor()
    filter_records = (f'Select * from "UMRepo"."file" WHERE cat_id = %s ')
    cursor.execute('select * from "UMRepo"."Category"')
    categories = cursor.fetchall()
    check = """SELECT "file_id" FROM "UMRepo"."favourites" WHERE user_id = %s"""
    cursor.execute(check, (session["user_id"],))
    favs = [row[0] for row in cursor.fetchall()]
    cursor.execute(filter_records,(type,))
    files = cursor.fetchall()
    return render_template("repository.html",files=files,categories=categories,favs=favs)
@app.route('/filter_favs')
def filter_favs():
    user_id = session.get("user_id")
    if not user_id:
        return abort(403)

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM "UMRepo"."Category"')
    categories = cursor.fetchall()

    # Only get favorites for the current user
    query = '''
        SELECT file.*, u."Name"
        FROM "UMRepo"."file" file
        JOIN "UMRepo"."favourites" fav ON fav.file_id = file.file_id
        JOIN "UMRepo"."User" u ON u.user_id = file.uploader
        WHERE fav.user_id = %s
    '''
    cursor.execute(query, (user_id,))
    files = cursor.fetchall()

    # Fetch user's favorites to highlight hearts
    fav_ids = [row[0] for row in files]  # or another query if needed

    return render_template("repository.html", files=files, categories=categories, favs=fav_ids)




@app.route('/toggle_favourite/<int:file_id>')
def toggle_favourite(file_id):
    if not session.get('user_id'):
        return abort(403)
    user_id = session.get('user_id')

    cursor = conn.cursor()
    check_query = '''SELECT 1 FROM "UMRepo"."favourites" WHERE user_id = %s AND file_id = %s'''
    cursor.execute(check_query, (user_id, file_id))
    is_fav = cursor.fetchone()

    if is_fav:
        delete_query = '''DELETE FROM "UMRepo"."favourites" WHERE user_id = %s AND file_id = %s'''
        cursor.execute(delete_query, (user_id, file_id))
    else:
        insert_query = '''INSERT INTO "UMRepo"."favourites"(user_id, file_id) VALUES (%s, %s)'''
        cursor.execute(insert_query, (user_id, file_id))

    conn.commit()
    return redirect(url_for('repo'))

@app.route("/access_request")
def access_request():
    if session.get('RoleID') != 3:
        return abort(403)

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM "UMRepo"."pending";')
    pending = cursor.fetchall()

    cursor.execute('SELECT * FROM "UMRepo"."User" WHERE user_id != %s;', (session["user_id"],))
    users = cursor.fetchall()

    return render_template("AccessRequests.html", pending=pending, users=users)


@app.route('/promote_demote', methods=['POST'])
def promote_demote():
    if session.get('RoleID') != 3:
        return abort(403)

    user_id = int(request.form.get("target_user_id"))
    action = request.form.get("action")

    if user_id == session.get("user_id"):
        return abort(403)

    cursor = conn.cursor()
    cursor.execute('SELECT "RoleID" FROM "UMRepo"."User" WHERE user_id = %s', (user_id,))
    current_role = cursor.fetchone()[0]

    new_role = None
    if action == "promote":
        if current_role == 1:
            new_role = 2
        elif current_role == 2:
            new_role = 3
    elif action == "demote":
        if current_role == 3:
            new_role = 2
        elif current_role == 2:
            new_role = 1

    if new_role:
        cursor.execute('UPDATE "UMRepo"."User" SET "RoleID" = %s WHERE user_id = %s', (new_role, user_id))
        conn.commit()

    return redirect("/access_request")


@app.route("/update_role", methods=["POST"])
def update_role():
    if session.get('RoleID') != 3:
        return abort(403)

    user_id = int(request.form.get("user_id"))
    action = request.form.get("action")

    # Prevent user from changing themselves
    if user_id == session.get("user_id"):
        return abort(403)

    cursor = conn.cursor()
    cursor.execute('SELECT "RoleID" FROM "UMRepo"."User" WHERE user_id = %s', (user_id,))
    current_role = cursor.fetchone()[0]

    # Role transition logic
    new_role = current_role
    if action == "promote":
        if current_role == 1:
            new_role = 2  # Student → Teacher
        elif current_role == 2:
            new_role = 3  # Teacher → Librarian
    elif action == "demote":
        if current_role == 2:
            new_role = 1  # Teacher → Student
        elif current_role == 3:
            new_role = 2  # Librarian → Teacher

    cursor.execute('UPDATE "UMRepo"."User" SET "RoleID" = %s WHERE user_id = %s', (new_role, user_id))
    conn.commit()
    return redirect("/access_request")

@app.route('/my_uploads')
def my_uploads():
    if session.get('RoleID') not in [2, 3]:
        return abort(403)  # Only teachers or librarians

    cursor = conn.cursor()
    cursor.execute('''
        SELECT file.*, c."cat_name"
        FROM "UMRepo"."file" file
        JOIN "UMRepo"."Category" c ON c.cat_id = file.cat_id
        WHERE file.uploader = %s;
    ''', (session["user_id"],))
    uploads = cursor.fetchall()
    print(uploads)
    return render_template('my_uploads.html', uploads=uploads)



   


    # # GET: Load file info
    # cursor.execute('''
    #     SELECT name, description, visibility FROM "UMRepo"."file" 
    #     WHERE file_id = %s AND uploader = %s
    # ''', (file_id, session["user_id"]))
    # file = cursor.fetchone()

    # return render_template('edit_upload.html', file=file, file_id=file_id)


    # # GET: Load file info
    # cursor.execute('''
    #     SELECT name, description, visibility FROM "UMRepo"."file" 
    #     WHERE file_id = %s AND uploader = %s
    # ''', (file_id, session["user_id"]))
    # file = cursor.fetchone()

    # return render_template('edit_upload.html', file=file, file_id=file_id)
    
@app.route('/edit_upload/<int:file_id>', methods=['GET', 'POST'])
def edit_upload(file_id):
    if session.get('RoleID') not in [2, 3]:
        return abort(403)

    cursor = conn.cursor()
    uploader_id = session['user_id']

    # Fetch all categories
    cursor.execute('SELECT cat_id, cat_name FROM "UMRepo"."Category"')
    categories = cursor.fetchall()

    # Fetch distinct subject categories
    cursor.execute('SELECT DISTINCT subject_category FROM "UMRepo"."file"')
    subject_categories = [row[0] for row in cursor.fetchall()]

    # Get current file details
    cursor.execute('''
        SELECT name, description, visibility, cat_id, subject_category 
        FROM "UMRepo"."file" 
        WHERE file_id = %s AND uploader = %s
    ''', (file_id, uploader_id))
    file = cursor.fetchone()

    if not file:
        return abort(404)

    name, description, visibility, cat_id, subject_category = file

    # Fetch and prepare all attribute fields
    attribute_map = {}
    for cid, _ in categories:
        cursor.execute('''
            SELECT a.attr_id, a.name, fa.value 
            FROM "UMRepo"."Attributes" a
            LEFT JOIN "UMRepo"."file_attributes" fa 
                ON a.attr_id = fa.attr_id AND fa.file_id = %s
            WHERE a.cat_id = %s
        ''', (file_id, cid))
        attrs = cursor.fetchall()
        attribute_map[str(cid)] = [
            {"id": attr[0], "name": attr[1], "value": attr[2] or ""}
            for attr in attrs
        ]

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        visibility = request.form['visibility']
        new_cat_id = int(request.form['material_type'])
        new_subject_category = request.form['subject_category']

        # Update file metadata
        cursor.execute('''
            UPDATE "UMRepo"."file"
            SET name = %s, description = %s, visibility = %s, cat_id = %s, subject_category = %s
            WHERE file_id = %s AND uploader = %s
        ''', (name, description, visibility, new_cat_id, new_subject_category, file_id, uploader_id))

        # Clear old attributes
        cursor.execute('DELETE FROM "UMRepo"."file_attributes" WHERE file_id = %s', (file_id,))

        # Parse and insert new attributes based on category
        start = 1
        attrs = []

        if new_cat_id == 1:
            start = 1
            attrs = [request.form.get(k) for k in ["Course Name", "Lecturer Name", "Semester", "Year", "Topic"]]
        elif new_cat_id == 2:
            start = 6
            attrs = [request.form.get(k) for k in ["Course Name", "Assignment Number", "Due Date", "Instructor Name", "Year"]]
        elif new_cat_id == 3:
            start = 23
            attrs = [request.form.get(k) for k in ["Course Name", "Exam Type", "Year", "Due Date", "Instructor", "Duration"]]
        elif new_cat_id == 4:
            start = 39
            attrs = [request.form.get(k) for k in ["Title", "Authors", "Publication Year", "Journal/Conference Name"]]
        elif new_cat_id == 5:
            start = 11
            attrs = [request.form.get(k) for k in ["Experiment Title", "Subject", "Instructor", "Lab Partners"]]
        elif new_cat_id == 6:
            start = 16
            attrs = [request.form.get(k) for k in ["Title", "Student Name", "Supervisor", "Department", "Year", "Abstract", "Degree Level"]]
        elif new_cat_id == 7:
            start = 33
            attrs = [request.form.get(k) for k in ["Course Name", "Instructor", "Duration", "Topic", "Title"]]
        elif new_cat_id == 8:
            start = 28
            attrs = [request.form.get(k) for k in ["Title", "Speaker Name", "Course Name", "Date Presented", "Topic"]]

        new_record = '''INSERT INTO "UMRepo"."file_attributes"(file_id, attr_id, value) VALUES (%s, %s, %s);'''
        for i, value in enumerate(attrs):
            cursor.execute(new_record, (file_id, start + i, value))

        conn.commit()

        # ✅ Redirect to assign access if visibility is set to Restricted
        if visibility == "Restricted":
            return redirect(url_for("assign_access", file_id=file_id))

        return redirect(url_for('my_uploads'))

    return render_template(
        'edit.html',
        file=[name, description, visibility],
        file_id=file_id,
        material_types=categories,
        file_cat_id=cat_id,
        subject_categories=subject_categories,
        file_subject=subject_category,
        attribute_map=attribute_map
    )



@app.route('/delete_upload/<int:file_id>', methods=['GET', 'POST'])
def delete_upload(file_id):
    if session.get('RoleID') not in [2, 3]:
        return abort(403)

    cursor = conn.cursor()

    try:
        # Step 1: Remove favorites related to this file
        cursor.execute('DELETE FROM "UMRepo"."favourites" WHERE file_id = %s', (file_id,))

        # Step 2: Remove access control records
        cursor.execute('DELETE FROM "UMRepo"."file_access" WHERE file_id = %s', (file_id,))

        # Step 3: Remove file attributes
        cursor.execute('DELETE FROM "UMRepo"."file_attributes" WHERE file_id = %s', (file_id,))

        # Step 4: Delete the actual file record
        cursor.execute('DELETE FROM "UMRepo"."file" WHERE file_id = %s AND uploader = %s', (file_id, session["user_id"]))

        conn.commit()

    except Exception as e:
        print("❌ Deletion failed:", e)
        conn.rollback()
        return "Could not delete file due to existing dependencies.", 500

    return redirect(url_for('my_uploads'))

@app.route('/get_attributes/<int:cat_id>')
def get_attributes(cat_id):
    cursor = conn.cursor()
    cursor.execute('SELECT attr_id, attr_name FROM "UMRepo"."Attributes" WHERE cat_id = %s', (cat_id,))
    attributes = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    return jsonify(attributes)
@app.route('/view/<int:file_id>')
def view(file_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT file.*, u."Name", u."Surname"
        FROM "UMRepo"."file" AS file
        JOIN "UMRepo"."User" AS u ON u.user_id = file.uploader
        WHERE file.file_id = %s 
    ''', (file_id,))
    file_info = cursor.fetchone()

    if not file_info:
        return abort(404)

    # Fetch attributes for the file
    cursor.execute('''
        SELECT a.name, fa.value 
        FROM "UMRepo"."Attributes" a
        JOIN "UMRepo"."file_attributes" fa ON a.attr_id = fa.attr_id
        WHERE fa.file_id = %s 
        Order By a.attr_id;
    ''', (file_id,))
    attributes = cursor.fetchall()
    print(file_info)
    print(attributes)
    return render_template("view.html", file_info=file_info, attributes=attributes)

if __name__ == '__main__':

    app.run(host="0.0.0.0")
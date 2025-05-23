# 📚 Academic Repository Website ACE

A platform for students and teachers to share, access, and interact with academic materials easily and securely.

 # Project Overview
 
The Academic Repository platform allows:

- Students to browse, view, and download study materials.

- Teachers to upload educational content and manage access to it.

- Librarians to approve new users and manage repository content.

- This project fosters academic collaboration by making learning resources organized and accessible.

# 🛠 Tech Stack

 Frontend: HTML + CSS + JavaScript (with Bootstrap for styling and AOS for animations)


 Backend: Python (with Flask). Flask handles routing, session management, user authentication, and database logic.


 Database: PostgreSQL (managed via psycopg2 for raw SQL queries and SQLAlchemy ORM for model-based interactions)


 Tools & Environment:


• Visual Studio Code (with extensions for Python, HTML, and PostgreSQL)


• GitHub for version control


• dotenv for managing environment variables securely


• bcrypt for password hashing and secure authentication


• Werkzeug for secure URL routing and request handling


• Jinja2 for dynamic HTML templating

# 🎯 Key Features

 Secure authentication and role-based access control.

 Material upload and download system.

 Content tagging and easy search.

 Separate roles for Students, Teachers, and Librarians.

 Responsive and user-friendly interface.

# 📋 How to Run the Project Locally

📋 How to Run the AcaRep Project Locally
This guide will walk you through running the AcaRep academic repository system on your local machine using Flask and PostgreSQL.

🛠 Step-by-Step Setup

✅ Step 1: Install Required Software

Make sure you have the following installed:

Python 3.x

PostgreSQL (e.g. version 17)

pgAdmin 4 (optional, for managing your database visually)

Git (to clone the project)

✅ Step 2: Restore the Database Using Acarep.sql

1. Download the Acarep.sql file
2. Open Command Prompt or PowerShell
Navigate to your PostgreSQL installation's bin directory:

bash
Copy
Edit
cd "C:\Program Files\PostgreSQL\<VERSION>\bin"
Replace <VERSION> with your PostgreSQL version (e.g. 17).

3. Create the database:
bash
Copy
Edit
.\createdb -U postgres AcaRep
4. Restore the database:
bash
Copy
Edit
.\psql -U postgres -p 5234 -d AcaRep -f "C:\Users\<YOUR_USER>\Downloads\Acarep.sql"
Replace <YOUR_USER> with your Windows username.

 PostgreSQL Password Note (IMPORTANT)
When prompted for a password, enter the one you set during PostgreSQL installation.
This is your own password – the project does not provide a default password.

If you forget it, you can reset it using:

sql
Copy
Edit
ALTER USER postgres WITH PASSWORD 'newpassword';
Run the above command from pgAdmin's Query Tool or psql.

To avoid hardcoding the password, store it in a .env file:

env
Copy
Edit
DB_PASS=yourpassword
Make sure your Python code uses:

python
Copy
Edit
import os
password = os.getenv("DB_PASS")

✅ Step 3: Clone the Project

Download or clone the project to your local directory:

bash
Copy
Edit
git clone <project-url>

✅ Step 4: Install Project Dependencies

Open a terminal inside the cloned project folder.

Create a virtual environment (recommended):

bash
Copy
Edit
python -m venv venv
Activate it:

bash
Copy
Edit
venv\Scripts\activate
Install required Python packages:

bash
Copy
Edit
pip install -r requirements.txt

✅ Step 5: Run the Application

Run the backend:

bash
Copy
Edit
python backendlogic.py
You should see two IP addresses in the terminal (e.g. http://127.0.0.1:5000)

Hold Ctrl + Left Click on one of them to open in your browser.

Append /index to the URL:

perl
Copy
Edit
http://127.0.0.1:5000/index
You should now see the homepage of AcaRep.

 Optional: Set Up the Database via pgAdmin

If you prefer a visual interface:

🟢 Step 1: Create the Database
Open pgAdmin

Expand Servers > PostgreSQL 17 > Databases

Right-click on Databases → Create → Database...

Name it acarep (case-sensitive)

Click Save

🟢 Step 2: Run the SQL File
Right-click acarep → Query Tool

Open Acarep.sql

Click ▶ (Run) or press F5

All tables, data, and schema will be imported.

 Required Python Packages

Installed automatically using:

bash
Copy
Edit
pip install -r requirements.txt

Feel free to contribute, report bugs, or ask questions. Good luck with your setup!




#  Thank you for checking out the Academic Repository Project!



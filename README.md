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

Step 1: Download the Acarep.sql file

Step 2: Open Command Prompt Or Powershell and go to path C:\Program Files\PostgreSQL\<VERSION>\bin
where VERSION is the number

Step 3: Copy .\createdb -U postgres AcaRep into your terminal and hit Enter

Step 4: Copy .\psql -U postgres -p 5234 -d AcaRep -f "C:\Users\<USER>\Downloads\AcaRep.sql" into your terminal and hit Enter

Step 5:Clone the project to your local directory

Step 6: In the cloned folder, run the file "backendlogic.py", It should give you two ip addresses in the terminal upon running 

Step 7: Hit ctrl+left click on one of the ip addresses and add /index at the end, doing so will take you to the website


 install 
- flask

- flask_login

- os

- psycopg2

- dotenv

- bcrypt

- os

- json

- secrets

- datetime 

- flask_sqlalchemy 

- sqlalchemy

- werkzeug.utils

  using the command prompt or powershell
  type

  ```pip install flask
flask_login 
os 
psycopg2 
dotenv 
bcrypt 
os 
json 
secrets 
datetime  
flask_sqlalchemy  
sqlalchemy
werkzeug.utils
#  Thank you for checking out the Academic Repository Project!



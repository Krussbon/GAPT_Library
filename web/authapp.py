import json
import os
import psycopg2
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
cursor = conn.cursor()
find_record = (f"""select * from "UMRepo"."pending";""")
cursor.execute(find_record)
pending = cursor.fetchall()
print(pending)
keys_to_remove = []
for record in pending:
    if input("Accept?: Y/N:").capitalize()=='Y':
        new_record = (f"""Insert into "UMRepo"."User"("Name","Surname","email","Pass_Hash","RoleID")
            values (%s,%s,%s,%s,%s);""")
        del_record = (f"""Delete From "UMRepo"."pending" where """)
        name = record[0]
        surname = record[1]
        email = record[2]
        pass_hash = record[3]
        role_id = record[6]
        values= (name,surname,email,pass_hash,role_id)
        cursor.execute(new_record,values)
        conn.commit()

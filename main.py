import mysql.connector
from mysql.connector import Error
import hashlib
import subprocess

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='users',
                                         user='root',
                                         password='')
    if connection.is_connected():
        #write code here
        print("----------------------------")
        username = input("Input your username: ")
        password = input("Input your password: ")
        print("----------------------------")
        passw = hashlib.md5(password.encode())
        sql_query = "SELECT * from login WHERE username = '" + username + "' AND password = '" + passw.hexdigest()  + "'"
        cursor = connection.cursor()
        cursor.execute(sql_query)

        row = cursor.fetchone()
        while row is not None:
            uid = row[0]
            hwid = row[3]
            row = cursor.fetchone()

        pchwid = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()


        if cursor.rowcount == 1:
            if pchwid == hwid:
                print("UID: " + str(uid))
                print("Username: " + username)
                print("HWID: " + hwid)
            else:
                print("Hwid missmatch.")



        else:
            print("Something went wrong, make sure u enter valid username and password")
except Error as err:
    print("Error while connecting to MySQL", err)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
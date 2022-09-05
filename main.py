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
        print("1. Make account")
        print("2. Login into account")
        choose = input()
        int(choose)
        cursor = connection.cursor()
        pchwid = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

        if int(choose) == 1:
            create_user = input("Input username: ")
            create_pass = input("Input password: ")
            sql = "INSERT INTO login (username, password, hwid) VALUES ('" + create_user +"', MD5('" + create_pass +"'), '" + pchwid + "')"
            cursor.execute(sql)
            connection.commit()
        elif int(choose) == 2:
            # write code here
            print("----------------------------")
            username = input("Input your username: ")
            password = input("Input your password: ")
            print("----------------------------")
            passw = hashlib.md5(password.encode())
            sql_query = "SELECT * from login WHERE username = '" + username + "' AND password = '" + passw.hexdigest() + "'"
            cursor = connection.cursor()
            cursor.execute(sql_query)

            row = cursor.fetchone()
            while row is not None:
                uid = row[0]
                hwid = row[3]
                row = cursor.fetchone()


            if cursor.rowcount == 1:
                if pchwid == hwid:
                    print("UID: " + str(uid))
                    print("Username: " + username)
                    print("HWID: " + hwid)
                else:
                    print("Hwid missmatch.")
            else:
                print("Invalid username/password, try again!")
        else:
            print("Something went wrong...")




    else:
            print("Something went wrong")
except Error as err:
    print("Error while connecting to MySQL", err)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

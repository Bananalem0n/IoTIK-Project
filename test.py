#from crypt import methods
from itertools import product   
from tkinter.messagebox import RETRY
from colorama import Cursor
from flask import Flask, jsonify, flash, redirect, render_template, request, url_for, Blueprint
import mysql.connector, urllib.request, json
from firebase import Firebase
import json
from collections import OrderedDict
from firebase_admin import db

application = Flask(__name__)
application.secret_key = "abc"

from firebase import Firebase

config = {
  "apiKey": "AIzaSyChlso6sL0PzWMKfgDjDaZ-MTzE0C26PPc",
  "authDomain": "pnj-iotik.firebaseapp.com",
  "databaseURL": "https://pnj-iotik-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "pnj-iotik.appspot.com",
}

firebase = Firebase(config)

auth = firebase.auth()
db = firebase.database()
user = auth.sign_in_with_email_and_password("caturraya2003@gmail.com","nasrulanakbaik")
refreshToken = auth.refresh(user['refreshToken'])

data = db.child('UsersData').child(user['localId']).child('project').child('20').get().val()


# sql boss
def getMysqlConnection():
    return  mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='iotik')

@application.route("/")
@application.route('/landingpage')
def landingpage():
    return render_template('landingpageiotik.html')

@application.route('/regist', methods=['GET', 'POST'])   
def regist():							
    if request.method == 'GET':
        return render_template('regist.html')	
    elif request.method =='POST':
        user = request.form['username']
        email = request.form['email']	
        notlpn = request.form['notlpn']		
        password = request.form['password']	
        confirmpassword = request.form['confirmpassword']

    	# cek password confirmation
        if password == confirmpassword:
            db = getMysqlConnection()
            try:
                cur = db.cursor()
                cur.execute("INSERT INTO `user` (`uname`, `upass`, `email`, `no_tlpn`) VALUES ('"+user+"', '"+password+"', '"+email+"', '"+notlpn+"');")
                db.commit()
                cur.close()
            except Exception as e:
                print("Error in SQL:\n",e)
            finally:
                db.close()
        else:
            flash('Password tidak sama', 'error')
        return render_template('login.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        cur.execute ("SELECT uname,upass FROM user union select name,pass from admin;")
        output = cur.fetchall()
        print(output)
        db.commit()
        
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()

    if request.method == 'GET':
        return render_template('login.html')

    elif request.method =='POST':
        user = request.form['username']			
        password = request.form['password']	

        for kolom in output:
            for i in range(len(kolom)):
                if str(user) == kolom[i]:
                    print(str(user))
                    if str(password) == kolom[i+1]:
                        print(str(password))
                        cur.close()
                        return redirect(url_for('index',username = str(user)))
                    else:
                        break
                elif str(user) == 'admin':
                    print(str(user))
                    if str(password) == 'admin':
                        print(str(password))
                        return redirect(url_for('index_admin'))
                    else:
                        cur.close()
                        break
        print('invalid username/password', 'error')
        return render_template('login.html')

# def get_user():
    # db = getMysqlConnection()
    # try:
    #     cur = db.cursor()
    #     cur.execute ("SELECT uname FROM `user` WHERE `username == '%username")
    #     output = cur.fetchall()
    #     print(output)
    #     db.commit()
    #     cur.close()
    # except Exception as e:
    #     print("Error in SQL:\n", e)

@application.route('/firedetector')
def firedetector():
    
    temp = data['temperature']
    humid = data['humidity']
    rain = data['rain-sensor']

    if rain == "0":
        rain = 'Tidak hujan'
    else:
        rain = 'Hujan'

    return render_template('firedetector.html',kalimat = [temp,humid,rain])

@application.route('/raindetector')
def raindetector():
    
    temp = data['temperature']
    humid = data['humidity']
    rain = data['rain-sensor']

    if rain == "0":
        rain = 'Tidak hujan'
    else:
        rain = 'Hujan'

    return render_template('raindetector.html',kalimat = [temp,humid,rain])

@application.route('/smartdoorlock')
def smartdoorlock():
    
    # temp = data['temperature']
    # humid = data['humidity']
    door = data['rain-sensor']

    if door == "0":
        door = 'Tidak terkunci'
    else:
        door = 'Terkunci'

    return render_template('smartdoorlock.html',kalimat = [door])

@application.route('/indexadmin')
def indexadmin():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from user"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
       db.close()
    return render_template('index_admin.html',kalimat=output_json)

#################
#  NAMBAH USER  #
#################
@application.route('/adduser', methods=['GET','POST'])
def adduser():
    print(request.method)
    if request.method == 'GET':
        return render_template('adduser.html')
    else: 
        request.method == 'POST'
        id_user = request.form['id_user']
        uname = request.form['uname']
        upass = request.form['upass']   
        email = request.form['email']
        no_telp = request.form['no_telp']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "Data Berhasil Ditambahkan"
            sqlstr = "INSERT INTO `user` (`id_user`, `uname`, `upass`, `email`, `no_telp`) VALUES ('"+id_user+"','"+uname+"','"+upass+"','"+email+"','"+no_telp+"')"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print('Error in SQL:\n', e)
        finally:
            db.close()
            return redirect(url_for('indexadmin')) 

#################
#   EDIT USER   #
#################
@application.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    if request.method == 'GET':
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            cur.execute ("SELECT * FROM user where id=%s", (id,))
            output = cur.fetchall()
            print(output)
            db.commit()
            cur.close()
            
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template('edituser.html', kalimat=output)
    elif request.method == 'POST':
        id_user = request.form['id_user']
        uname = request.form['uname']
        upass = request.form['upass']   
        email = request.form['email']
        no_telp = request.form['no_telp']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            cur.execute ("UPDATE `user` SET `id_user` = %s, `uname` = %s, `upass` = %s, `email` = %s, `no_telp` = %s WHERE `user`.`id_user` = %s",(id_user,uname,upass,email,no_telp,id,))
            output = cur.fetchall()
            print(output)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('index_admin'))

    return render_template('index_admin.html')

@application.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    db = getMysqlConnection()
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.execute("DELETE FROM user WHERE id=%s", (id, ))
        db.commit()
        cursor.close()

        return redirect(url_for('index_admin'))
    return render_template('index_admin.html')


@application.route('/index')
def index():
    return render_template('index.html')

@application.route('/index_admin')
def index_admin():
    return render_template('index_admin.html')

if __name__ == '__main__':
    application.run(debug=True)
#from crypt import methods
from itertools import product   
from tkinter.messagebox import RETRY
from colorama import Cursor
from flask import Flask, jsonify, flash, redirect, render_template, request, url_for, Blueprint
import mysql.connector, urllib.request, json, requests



application = Flask(__name__)
application.secret_key = "abc"


#mengubah kelvin ke celcius
def k2c(kelvin):
    c = float(kelvin) - 273.15
    return round (c)


#cuaca 
# def cuaca():
#     appid = 'cadb4f8880792c163567e70aa67d122f'
#     lat = '-6.36'
#     lon = '106.81'
#     url = 'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,daily&appid={appid}'
#     url = url.format(lat=lat, lon=lon, appid=appid)
#     mentah = urllib.request.urlopen
#     root = ET.fromstring(mentah.decode())

#     kota = root.findall('timezone')
#     temperature = root.findall('temperature')
#     tekanan = root.findall('pressure')
#     kelembapan = root.findall('humadity')

#     return render_template(kota=kota, temperature=temperature, tekanan=tekanan, kelembapan=kelembapan)


def getMysqlConnection():
    return  mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='iotik')

def database():
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        cur.execute ("SELECT * FROM `doorlock`")
        output = cur.fetchall()
        print(output)
        db.commit()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    print(output)


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
        password = request.form['password']	
        confirmpassword = request.form['confirmpassword']

    	# cek password confirmation
        if password == confirmpassword:
            db = getMysqlConnection()
            try:
                cur = db.cursor()
                cur.execute("INSERT INTO `user` (`uname`, `upass`) VALUES ('"+user+"', '"+password+"');")
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
        cur.execute ("SELECT * FROM `user`")
        output = cur.fetchall()
        print(output)
        db.commit()
        cur.close()
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
                        return redirect(url_for('index'))
                    else:
                        break
        print('invalid username/password', 'error')
        return render_template('login.html')


@application.route('/loginadmin')
def loginadmin():
    return render_template('loginadmin.html')

@application.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@application.route('/dashboardd')
def dashboardd():
    return render_template('dashboardd.html')

@application.route('/index')
def index():
    appid = 'cadb4f8880792c163567e70aa67d122f'
    lat = '-6.291744211707815'
    lon = '106.84260940551759'
    url = 'https://api.openweathermap.org/data/2.5/' + \
    'forecast?lat={lat}&lon={lon}&appid={appid}'
    r = requests.get(url.format(lat=lat, lon=lon, appid=appid)).json()

    print(r)
    weather = {
        'city' : r['city']['name'],
        # # 'temp' : r['current']['temp'],
        # 'suhu' : r['current']['humidity'],
        # 'kelembapan' : r['current']['pressure'],
    }

    jam = {
        'jam1' : r['list'][1]['dt_txt'],
        'jam2' : r['list'][2]['dt_txt'],
        'jam3' : r['list'][3]['dt_txt'],
        'jam4' : r['list'][4]['dt_txt'],
        'jam5' : r['list'][5]['dt_txt'],
        'jam6' : r['list'][6]['dt_txt'],
        'jam7' : r['list'][7]['dt_txt'],
    }

    temp = {
        'temp1' : r['list'][1]['main']['temp'],     
        'temp2' : r['list'][2]['main']['temp'],
        'temp3' : r['list'][3]['main']['temp'],
        'temp4' : r['list'][4]['main']['temp'],
        'temp5' : r['list'][5]['main']['temp'],
        'temp6' : r['list'][6]['main']['temp'],
        'temp7' : r['list'][7]['main']['temp'],
    }
  
    temperature = {
        'temperature' : k2c(temp['temp1']),
        'temperature2': k2c(temp['temp2']),
        'temperature3': k2c(temp['temp3']),
        'temperature4': k2c(temp['temp4']),
        'temperature5' : k2c(temp['temp5']),
        'temperature6' : k2c(temp['temp6']),
        'temperature7' : k2c(temp['temp7']),
    }
    fire = temperature['temperature'] * 2


    # temperature = k2c(temperature['temp1']) 

    return render_template('index.html', weather=weather, jam=jam, temperature=temperature, fire=fire)

@application.route('/temperature')
def temperature():
    return render_template('temperature.html')

@application.route('/doorlock')
def doorlock():
    db = getMysqlConnection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM doorlock")
    result = cursor.fetchall()
    r = result
    unlock = 1
    if unlock == 1:
        i = 'fa fa-unlock'
    else :
        i = 'fa fa-lock'
    return render_template('doorlock.html', r=r, i=i)

@application.route('/firedetector')
def firedetector():
    return render_template('firedetector.html')
# def getMethod(sqlstr):
#     db = getMysqlConnection()
#     try: 
#         cur = db.cursor()
#         print(sqlstr)
#         cur.execute(sqlstr)
#         output_json = cur.fetchall()
#     except Exception as e:
#         print("Error in SQL:\n", e)
#     finally:
#         db.close() 
#     return output_json

# def postMethod(sqlstr):
#     db = getMysqlConnection()
#     try:
#         cur = db.cursor()
#         print(sqlstr)
#         cur.execute(sqlstr)
#         db.commit()
#         cur.close()
#         print("Success")
#     except Exception as e:
#         print("Error in SQL:\n", e)
#     finally:
#         db.close()

# def getData(url):
#     response = urllib.request.urlopen(url)
#     content = response.read()
#     output = json.loads(content) 
#     return output

# @application.route('/api/')
# def my_api():
#     return render_template('api.html')

# @application.route('/api/v1/peminjaman')
# def api_peminjaman():
#     output_db = getMethod("SELECT * FROM `peminjaman`")
#     peminjaman = {}
#     peminjaman['peminjaman'] = []
#     for column in output_db:
#         content = {'id_peminjaman':column[0], 'tanggal_pinjam':column[1], 'tanggal_kembali':column[2], 'id_buku':column[3], 'id_anggota':column[4], 'id_petugas':column[5]}
#         peminjaman['peminjaman'].append(content)
#         content = {}
#     return jsonify(peminjaman) 

# @application.route('/peminjaman')  
# def peminjaman():
#     output = getData(f"http://127.0.0.1:5000/api/v1/peminjaman") 
#     print('Data berhasil didapatkan!', 'success')
#     return render_template('peminjaman.html', data=output['peminjaman'])

# # @application.route('/peminjaman')
# # def peminjaman():
# #     db = getMysqlConnection()
# #     try:
# #         sqlstr = "SELECT * from peminjaman"
# #         cur = db.cursor()
# #         cur.execute(sqlstr)
# #         output_json = cur.fetchall()
# #     except Exception as e:
# #         print("Error in SQL:\n", e)
# #     finally:
# #         db.close()
# #     return render_template('peminjaman.html',kalimat=output_json)

# @application.route('/api/v1/anggota')
# def api_anggota():
#     output_db = getMethod("SELECT * FROM `anggota`")
#     anggota = {}
#     anggota['anggota'] = []
#     for column in output_db:
#         content = {'id_anggota':column[0], 'kode':column[1], 'nama':column[2], 'jk':column[3], 'jurusan':column[4], 'no_telp':column[5], 'alamat':column[6]}
#         anggota['anggota'].append(content)
#         content = {}
#     return jsonify(anggota)

# @application.route('/anggota')  
# def anggota():
#     output = getData(f"http://127.0.0.1:5000/api/v1/anggota") 
#     flash('Data anggota berhasil didapatkan!', 'success')
#     return render_template('anggota.html', data=output['anggota'])

# @application.route('/anggota_id/<int:id>')
# def anggota_id(id):
#     output_db = getMethod("SELECT * FROM `anggota` WHERE `id_anggota`="+str(id))
#     anggota = {}
#     anggota['anggota'] = []
#     for column in output_db:
#         content = {'id_anggota':column[0], 'kode':column[1], 'nama':column[2], 'jk':column[3], 'jurusan':column[4], 'no_telp':column[5], 'alamat':column[6]}
#         anggota['anggota'].append(content)
#         content = {}
#     return jsonify(anggota)

# # @application.route('/anggota')
# # def anggota():
# #     db = getMysqlConnection()
# #     try:
# #         sqlstr = "SELECT * from anggota"
# #         cur = db.cursor()
# #         cur.execute(sqlstr)
# #         output_json = cur.fetchall()
# #     except Exception as e:
# #         print("Error in SQL:\n", e)
# #     finally:
# #         db.close()
# #     return render_template('anggota.html',kalimat=output_json)

# @application.route('/inputpeminjaman', methods=['GET', 'POST'])
# def inputpeminjaman():
#     print(request.method)
#     if request.method == 'GET':
#         id_buku_json = getMethod("SELECT id_buku, judul_buku FROM `buku`")
#         id_anggota_json = getMethod("SELECT id_anggota, nama_anggota FROM `anggota`")
#         id_petugas_json = getMethod("SELECT id_petugas, nama_petugas FROM `petugas`")
#         return render_template('inputpeminjaman.html',id_buku = id_buku_json, id_anggota = id_anggota_json, id_petugas = id_petugas_json)
#     elif request.method == 'POST':
#         id_peminjaman = request.form['idpeminjaman']
#         tanggal_pinjam = request.form['tanggalpeminjaman']
#         tanggal_kembali = request.form['tanggalpengembalian']
#         id_buku = request.form['idbuku']
#         id_anggota = request.form['idanggota']
#         id_petugas = request.form['idpetugas']
#         db = getMysqlConnection()
#         try:
#             cur = db.cursor()
#             sqlstr = "INSERT INTO `peminjaman` (`id_peminjaman`, `tanggal_pinjam`, `tanggal_kembali`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ('"+id_peminjaman+"', '"+tanggal_pinjam+"', '"+tanggal_kembali+"', '"+id_buku+"', '"+id_anggota+"', '"+id_petugas+"');"
#             print(sqlstr)
#             cur.execute(sqlstr)
#             db.commit()
#             cur.close()
#         except Exception as e:
#             print("Error in SQL:\n", e)
#         finally:
#             db.close()
#         return redirect(url_for('peminjaman'))

# @application.route('/update_pem/<int:peminjaman_id>', methods=['GET', 'POST'])
# def update_pem(peminjaman_id):
#     if request.method == 'GET':
#         db = getMysqlConnection()
#         try:
#             cur = db.cursor()
#             cur.execute ("SELECT * FROM peminjaman where id_peminjaman=%s", (peminjaman_id,))
#             output = cur.fetchall()
#             print(output)
#             db.commit()
#             cur.close()
#         except Exception as e:
#             print("Error in SQL:\n", e)
#         finally:
#             db.close()
#         id_buku_json = getMethod("SELECT id_buku, judul_buku FROM `buku`")
#         id_anggota_json = getMethod("SELECT id_anggota, nama_anggota FROM `anggota`")
#         id_petugas_json = getMethod("SELECT id_petugas, nama_petugas FROM `petugas`")
#         return render_template('updatepeminjaman.html', kalimat=output, id_buku = id_buku_json, id_anggota = id_anggota_json, id_petugas = id_petugas_json)	
#     elif request.method == 'POST':
#         tanggal_pinjam = request.form['tanggalpeminjaman']
#         tanggal_kembali = request.form['tanggalpengembalian']
#         id_buku = request.form['idbuku']
#         id_anggota = request.form['idanggota']
#         id_petugas = request.form['idpetugas']
#         db = getMysqlConnection()
#         try:
#             cur = db.cursor()
#             cur.execute ("UPDATE `peminjaman` SET `tanggal_pinjam` = %s, `tanggal_kembali` = %s, `id_buku` = %s, `id_anggota` = %s, `id_petugas` = %s WHERE `peminjaman`.`id_peminjaman` = %s",(tanggal_pinjam, tanggal_kembali, id_buku, id_anggota, id_petugas, peminjaman_id,))
#             output = cur.fetchall()
#             print(output)
#             db.commit()
#             cur.close()
#         except Exception as e:
#             print("Error in SQL:\n", e)
#         finally:
#             db.close()
#         return redirect(url_for('peminjaman'))
#     return render_template('peminjaman.html')

# @application.route('/delete_pem/<int:peminjaman_id>', methods=['GET', 'POST'])
# def delete_pem(peminjaman_id):
#     db = getMysqlConnection()
#     try:
#         cur = db.cursor()
#         cur.execute ("DELETE FROM peminjaman WHERE id_peminjaman=%s", (peminjaman_id,))
#         db.commit()
#         cur.close()
#     except Exception as e:
#         print("Error in SQL:\n", e)
#     finally:
#         db.close()
#     return redirect(url_for('peminjaman'))

if __name__ == '__main__':
    application.run(debug=True)
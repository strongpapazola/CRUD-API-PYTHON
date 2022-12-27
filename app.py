from flask import Flask, request, jsonify, make_response
import mysql.connector

app = Flask(__name__)

# MySQL configurations
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="crud_api_python"
)
cursor = mydb.cursor()

# Function to get all barang
@app.route('/barang', methods=['GET'])
def get_barang():
    cursor.execute("SELECT * FROM barang")
    result = cursor.fetchall()
    response = []
    for data in result:
        barang_dict = {
            'id_barang': data[0],
            'nama_barang': data[1],
            'harga_barang': data[2],
            'jumlah_barang': data[3],
        }
        response.append(barang_dict)
    return make_response(jsonify(response), 200)

# Function to get barang by id
@app.route('/barang/<id_barang>', methods=['GET'])
def get_barang_by_id(id_barang):
    cursor.execute("SELECT * FROM barang WHERE id_barang=%s", (id_barang,))
    result = cursor.fetchone()
    response = {
        'id_barang': result[0],
        'nama_barang': result[1],
        'harga_barang': result[2],
        'jumlah_barang': result[3],
    }
    return make_response(jsonify(response), 200)

# Function to add new barang
@app.route('/barang', methods=['POST'])
def add_barang():
    # Get data from request
    data = request.get_json()
    nama_barang = data['nama_barang']
    harga_barang = data['harga_barang']
    jumlah_barang = data['jumlah_barang']

    # Insert data to MySQL
    cursor.execute("INSERT INTO barang (nama_barang, harga_barang, jumlah_barang) VALUES (%s, %s, %s)", (nama_barang, harga_barang, jumlah_barang))
    mydb.commit()

    # Get last inserted data
    cursor.execute("SELECT * FROM barang WHERE id_barang=%s", (cursor.lastrowid,))
    result = cursor.fetchone()
    response = {
        'id_barang': result[0],
        'nama_barang': result[1],
        'harga_barang': result[2],
        'jumlah_barang': result[3],
    }
    return make_response(jsonify(response), 200)

# Function to update barang by id
@app.route('/barang/<id_barang>', methods=['PUT'])
def update_barang(id_barang):
    # Get data from request
    data = request.get_json()
    nama_barang = data['nama_barang']
    harga_barang = data['harga_barang']
    jumlah_barang = data['jumlah_barang']

    # Update data to MySQL
    cursor.execute("UPDATE barang SET nama_barang=%s, harga_barang=%s, jumlah_barang=%s WHERE id_barang=%s", (nama_barang, harga_barang, jumlah_barang, id_barang))
    mydb.commit()

    # Get last updated data
    cursor.execute("SELECT * FROM barang WHERE id_barang=%s", (id_barang,))
    result = cursor.fetchone()
    response = {
        'id_barang': result[0],
        'nama_barang': result[1],
        'harga_barang': result[2],
        'jumlah_barang': result[3],
    }
    return make_response(jsonify(response), 200)

# Function to delete barang by id
@app.route('/barang/<id_barang>', methods=['DELETE'])
def delete_barang(id_barang):
    cursor.execute("DELETE FROM barang WHERE id_barang=%s", (id_barang,))
    mydb.commit()
    response = {
        'id_barang': id_barang,
        'message': 'Data berhasil dihapus'
    }
    return make_response(jsonify(response), 200)
    

if "__main__" == __name__:
    app.run(debug=True)
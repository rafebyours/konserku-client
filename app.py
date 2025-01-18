from flask import Flask, render_template, jsonify, request, session
from pymongo import MongoClient
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId  # Perlu di-import untuk memproses ObjectId dari MongoDB
import datetime  # Import datetime untuk mendapatkan waktu
import pytz  # Import pytz untuk pengaturan zona waktu
import firebase_admin
from firebase_admin import credentials, db as firebase_db

app = Flask(__name__)
# Aktifkan CORS dengan pengaturan untuk cookie
CORS(app, supports_credentials=True)  # Memungkinkan Flask menerima cookies dari permintaan CORS

cred = credentials.Certificate('./cred/ticketconcert-59a85-firebase-adminsdk-lsifh-0e5d07ddac.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ticketconcert-59a85-default-rtdb.firebaseio.com/'  # Ganti dengan URL Realtime Database kamu
})


# Kunci rahasia untuk session
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia Anda

# Koneksi ke MongoDB
client = MongoClient("mongodb+srv://nrafli39:SurajaKids@ticketconcert.jp56z.mongodb.net/?retryWrites=true&w=majority&appName=ticketConcert")  # Ganti URL jika Anda menggunakan MongoDB Atlas
db = client["ticketConcert"]
users_collection = db["users"]
concerts_collection = db["concerts"]  # Koleksi konser
transactions_collection = db["transaction"]  # Koleksi transaksi

# Mendapatkan waktu dengan zona waktu Indonesia (Jakarta)
indonesia_tz = pytz.timezone('Asia/Jakarta')
current_time = datetime.datetime.now(indonesia_tz)

# Mengambil referensi untuk menulis dan membaca data dari database
firebase_ref = firebase_db.reference('/') 

# Endpoint Home
@app.route('/')
def home():
    return "<h1>Welcome to the Ticket Concert App</h1>"


# Endpoint untuk mendapatkan data pengguna
@app.route('/users')
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))  # Ambil semua data pengguna
    return jsonify(users)

# Endpoint untuk register pengguna
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not data.get('name') or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing fields"}), 400
    
    hashed_password = generate_password_hash(data['password'])

    # Simpan pengguna baru ke dalam database
    new_user = {
        "name": data["name"],
        "username": data["username"],
        "email": data["email"],
        "password": hashed_password
    }
    users_collection.insert_one(new_user)
    
    # Ambil data pengguna yang baru saja didaftarkan
    user = users_collection.find_one({"username": data['username']})

    # Menyimpan informasi pengguna dalam session
    session['user_id'] = str(user['_id'])  # Menyimpan user_id dalam session
    session['username'] = user['username']  # Menyimpan username dalam session
    session['name'] = user['name']  # Menyimpan nama dalam session
    
    return jsonify({"message": "User registered successfully", "name": user['name']}), 200

# Endpoint untuk login pengguna
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = users_collection.find_one({"username": data['username']})
    
    if user and check_password_hash(user['password'], data['password']):
        # Kembalikan informasi user ke frontend untuk disimpan di localStorage
        return jsonify({
            "message": "Login successful",
            "user_id": str(user['_id']),
            "username": user['username'],
            "name": user['name']
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Endpoint untuk mengambil profil pengguna
@app.route('/api/user-profile/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    
    if user:
        return jsonify({
            "name": user['name'],
            "username": user['username'],
            "email": user['email'],
            "profileImage": user.get('profileImage', '')  # Foto profil jika ada
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Endpoint untuk memperbarui profil pengguna
@app.route('/api/user-profile/<user_id>', methods=['PUT'])
def update_user_profile(user_id):
    data = request.json
    
    # Pastikan ada nama dan email dalam data permintaan
    if not data.get('name') or not data.get('email'):
        return jsonify({"error": "Missing name or email"}), 400
    
    # Validasi ID pengguna
    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    # Cari pengguna di database
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    
    if user:
        updated_user = {
            "name": data["name"],
            "username": data.get("username", user['username']),
            "email": data["email"],
            "profileImage": data.get("profileImage", user.get('profileImage'))  # Update foto profil jika ada
        }

        # Jika password baru disertakan, hash dan perbarui password
        if data.get('password'):
            updated_user["password"] = generate_password_hash(data["password"])
        
        # Update data pengguna
        users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})

        return jsonify({"message": "User profile updated successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Endpoint logout pengguna
@app.route('/logout', methods=['POST'])
def logout_user():
    session.clear()  # Menghapus session untuk logout
    return jsonify({"message": "Logout successful"}), 200

# Endpoint untuk mendapatkan data konser
@app.route('/api/concerts', methods=['GET'])
def get_concerts():
    concerts = list(concerts_collection.find({}))
    # Konversi ObjectId menjadi string
    for concert in concerts:
        concert['_id'] = str(concert['_id'])
    return jsonify(concerts)

# Endpoint untuk menambahkan konser baru
@app.route('/api/concerts', methods=['POST'])
def add_concert():
    data = request.json
    if not data.get('title') or not data.get('date') or not data.get('location') or not data.get('price'):
        return jsonify({"error": "Missing fields"}), 400
    
    new_concert = {
        "title": data["title"],
        "image": data.get("image", ""),
        "logo": data.get("logo", ""),
        "date": data["date"],
        "time": data.get("time", ""),
        "city": data.get("city", ""),
        "province": data.get("province", ""),
        "location": data["location"],
        "price": data["price"],
        "description": data.get("description", ""),
        "coordinates": data.get("coordinates", {}),
        "remaining_tickets": data.get("remaining_tickets", 0)
    }
    
    concerts_collection.insert_one(new_concert)
    
    return jsonify({"message": "Concert added successfully"}), 201

@app.route('/api/concerts/<id>', methods=['GET'])
def get_concert_by_id(id):
    concert = concerts_collection.find_one({"_id": ObjectId(id)})
    if concert:
        concert["_id"] = str(concert["_id"])  # Convert ObjectId to string
        return jsonify(concert)
    else:
        return jsonify({"message": "Concert not found"}), 404



@app.route('/api/concerts/<id>', methods=['PUT'])
def update_concert(id):
    try:
        # Ambil data yang dikirimkan melalui request
        data = request.json

        # Filter hanya field yang ingin diperbarui
        updated_fields = {
            key: value for key, value in data.items()
            if key in ["title", "image", "logo", "date", "time", "city", "province", "location", "price", "description", "coordinates", "remaining_tickets"]
        }

        if not updated_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        # Update data di database
        result = concerts_collection.update_one(
            {"_id": ObjectId(id)},  # Filter berdasarkan ID
            {"$set": updated_fields}  # Set data baru
        )

        # Periksa apakah dokumen berhasil diperbarui
        if result.matched_count > 0:
            return jsonify({"message": "Concert updated successfully"}), 200
        else:
            return jsonify({"message": "Concert not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Endpoint untuk menghapus konser berdasarkan ID
@app.route('/api/concerts/<id>', methods=['DELETE'])
def delete_concert(id):
    try:
        # Cek apakah ID yang diberikan valid
        if not ObjectId.is_valid(id):
            return jsonify({"message": "Invalid concert ID", "status": "error"}), 400
        
        # Cari konser berdasarkan ID
        concert = concerts_collection.find_one({"_id": ObjectId(id)})
        
        if not concert:
            return jsonify({"message": "Concert not found", "status": "error"}), 404
        
        # Hapus konser dari koleksi
        concerts_collection.delete_one({"_id": ObjectId(id)})
        
        return jsonify({"message": "Concert deleted successfully", "status": "success"}), 200
    
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500
    
# Endpoint untuk menyimpan transaksi
# Endpoint untuk menyimpan transaksi
@app.route("/api/transaction", methods=["POST"])
def create_transaction():
    try:
        # Ambil data dari request
        data = request.json
        
        # Data transaksi yang diterima dari frontend
        user_id = data["user_id"]
        concert_id = data["concert_id"]
        payment_method = data["payment_method"]
        quantity = data["quantity"]
        total_cost = data["total_cost"]
        
        # Ambil data konser berdasarkan concert_id
        concert = concerts_collection.find_one({"_id": ObjectId(concert_id)})
        
        if not concert:
            return jsonify({"message": "Concert not found", "status": "error"}), 404
        
        # Mengecek apakah tiket yang diminta tersedia
        if concert["remaining_tickets"] < quantity:
            return jsonify({"message": "Not enough tickets available", "status": "error"}), 400
        
        # Simpan transaksi ke MongoDB dengan status payment = 0 (belum dibayar)
        transaction = {
            "user_id": ObjectId(user_id),
            "concert_id": ObjectId(concert_id),
            "payment_method": payment_method,
            "quantity": quantity,
            "total_cost": total_cost,
            "status_payment": 0,  # Default: Belum Dibayar
            "created_at": current_time
        }
        
        # Menyimpan transaksi ke database
        transactions_collection.insert_one(transaction)

        # Update remaining_tickets di konser dengan mengurangi jumlah yang dibeli
        new_remaining_tickets = concert["remaining_tickets"] - quantity
        concerts_collection.update_one(
            {"_id": ObjectId(concert_id)},
            {"$set": {"remaining_tickets": new_remaining_tickets}}
        )

        return jsonify({"message": "Transaction created and concert updated successfully", "status": "success"}), 201
    
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


@app.route("/api/transactions/<user_id>", methods=["GET"])
def get_transactions_by_user(user_id):
    """
    Mengambil semua transaksi berdasarkan user_id dan menyusun dari yang terbaru ke yang terlama.
    """
    if not ObjectId.is_valid(user_id):
        return jsonify({"message": "Invalid user ID", "status": "error"}), 400
    
    try:
        # Mengambil transaksi berdasarkan user_id dan mengurutkan berdasarkan created_at secara descending
        transactions = list(transactions_collection.find({"user_id": ObjectId(user_id)}).sort("created_at", -1))

        # Jika tidak ada transaksi ditemukan untuk user_id
        if not transactions:
            return jsonify({"message": "No transactions found for this user", "status": "error"}), 404
        
        # Konversi setiap ObjectId dalam transaksi menjadi string
        transactions = [convert_objectid_to_str(transaction) for transaction in transactions]

        # Menambahkan detail konser dan pengguna ke setiap transaksi
        for transaction in transactions:
            # Mendapatkan detail konser berdasarkan concert_id
            concert = concerts_collection.find_one({"_id": ObjectId(transaction['concert_id'])})
            if concert:
                transaction['concert_details'] = {
                    "title": concert['title'],
                    "location": concert['location'],
                    "date": concert['date'],
                    "price": concert['price'],
                    "remaining_tickets": concert['remaining_tickets']
                }
            else:
                # Jika konser tidak ditemukan
                transaction['concert_details'] = "Concert details not found."
            
            # Mendapatkan detail pengguna berdasarkan user_id
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            if user:
                transaction['user_details'] = {
                    "name": user.get('name', 'Name not available'),  # Default jika 'name' tidak ada
                    "email": user.get('email', 'Email not available'),  # Default jika 'email' tidak ada
                    "phone": user.get('phone', 'Phone not available')  # Default jika 'phone' tidak ada
                }
            else:
                # Jika pengguna tidak ditemukan
                transaction['user_details'] = "User details not found."

        return jsonify({"data": transactions, "status": "success"}), 200

    except Exception as e:
        # Mengembalikan pesan error jika terjadi exception
        return jsonify({"message": str(e), "status": "error"}), 500



def convert_objectid_to_str(data):
    """
    Fungsi untuk mengonversi ObjectId menjadi string pada semua field '_id' dalam data.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, (dict, list)):
                convert_objectid_to_str(value)
    elif isinstance(data, list):
        for item in data:
            convert_objectid_to_str(item)
    return data

@app.route('/api/transactions', methods=['GET'])
def get_all_transactions():
    """
    Mengambil semua transaksi yang ada dan menambahkan detail konser serta detail pengguna terkait.
    Data diurutkan berdasarkan waktu terbaru (created_at descending).
    """
    try:
        # Mengambil semua transaksi dan mengurutkan berdasarkan created_at secara descending
        transactions = list(transactions_collection.find().sort("created_at", -1))

        # Mengonversi ObjectId menjadi string untuk setiap transaksi
        transactions = convert_objectid_to_str(transactions)

        # Menambahkan detail konser dan pengguna ke setiap transaksi
        for transaction in transactions:
            # Cek apakah detail konser ada dengan konversi concert_id ke ObjectId
            concert = concerts_collection.find_one({"_id": ObjectId(transaction['concert_id'])})
            if concert:
                transaction['concert_details'] = {
                    "title": concert['title'],
                    "location": concert['location'],
                    "date": concert['date'],
                    "price": concert['price'],
                    "remaining_tickets": concert['remaining_tickets']
                }
            else:
                # Jika konser tidak ditemukan
                transaction['concert_details'] = "Concert details not found."

            # Cek apakah detail pengguna ada dengan konversi user_id ke ObjectId
            user = users_collection.find_one({"_id": ObjectId(transaction['user_id'])})
            if user:
                transaction['user_details'] = {
                    "name": user.get('name', 'Name not available'),  # Default jika 'name' tidak ada
                    "email": user.get('email', 'Email not available'),  # Default jika 'email' tidak ada
                    "phone": user.get('phone', 'Phone not available')  # Default jika 'phone' tidak ada
                }
            else:
                # Jika pengguna tidak ditemukan
                transaction['user_details'] = "User details not found."

        return jsonify({"data": transactions, "status": "success"}), 200
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


@app.route("/api/ticket/<transaction_id>", methods=["GET"])
def get_transaction_details(transaction_id):
    if not ObjectId.is_valid(transaction_id):
        return jsonify({"message": "Invalid transaction ID", "status": "error"}), 400

    try:
        # Ambil data transaksi berdasarkan transaction_id
        transaction = transactions_collection.find_one({"_id": ObjectId(transaction_id)})

        if not transaction:
            return jsonify({"message": "Transaction not found", "status": "error"}), 404

        # Konversi ObjectId menjadi string untuk transaksi
        transaction = convert_objectid_to_str(transaction)

        # Mendapatkan detail konser berdasarkan concert_id
        concert = concerts_collection.find_one({"_id": ObjectId(transaction['concert_id'])})
        if concert:
            transaction['concert_details'] = {
                "title": concert['title'],
                "location": concert['location'],
                "date": concert['date'],
                "price": concert['price'],
                "remaining_tickets": concert['remaining_tickets']
            }
        else:
            transaction['concert_details'] = "Concert details not found."

        # Mendapatkan detail pengguna berdasarkan user_id
        user = users_collection.find_one({"_id": ObjectId(transaction['user_id'])})
        if user:
            transaction['user_details'] = {
                "name": user.get('name', 'Name not available'),
                "email": user.get('email', 'Email not available'),
                "phone": user.get('phone', 'Phone not available')
            }
        else:
            transaction['user_details'] = "User details not found."

        return jsonify({"data": transaction, "status": "success"}), 200

    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


# Endpoint untuk memperbarui transaksi tertentu (PATCH)
@app.route("/api/ticket/<transaction_id>", methods=["PATCH"])
def patch_transaction_details(transaction_id):
    # Ambil data yang ingin diperbarui
    data = request.json
    
    # Validasi jika tidak ada data yang dikirimkan
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Validasi apakah transaction_id valid
    if not ObjectId.is_valid(transaction_id):
        return jsonify({"error": "Invalid transaction ID"}), 400

    # Ambil data transaksi berdasarkan transaction_id
    transaction = transactions_collection.find_one({"_id": ObjectId(transaction_id)})
    
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    # Buat dictionary untuk pembaruan
    update_data = {}

    # Periksa setiap field yang bisa diperbarui
    if 'status_payment' in data:
        update_data['status_payment'] = data['status_payment']
    
    if 'quantity' in data:
        # Pastikan jumlah tiket yang baru valid
        if data['quantity'] < 0:
            return jsonify({"error": "Quantity must be greater than or equal to 0"}), 400
        update_data['quantity'] = data['quantity']
    
    if 'payment_method' in data:
        update_data['payment_method'] = data['payment_method']
    
    # Jika tidak ada data yang akan diperbarui
    if not update_data:
        return jsonify({"error": "No valid fields to update"}), 400

    # Update transaksi di MongoDB
    transactions_collection.update_one({"_id": ObjectId(transaction_id)}, {"$set": update_data})

    # Jika status pembayaran diperbarui, mungkin perlu mengupdate status tiket juga
    if 'status_payment' in update_data and update_data['status_payment'] == 1:
        concert_id = transaction['concert_id']
        quantity_purchased = transaction['quantity']
        
        # Update jumlah tiket yang tersisa di konser
        concert = concerts_collection.find_one({"_id": ObjectId(concert_id)})
        if concert:
            remaining_tickets = concert['remaining_tickets'] + quantity_purchased  # Tambahkan kembali tiket yang tersedia
            concerts_collection.update_one(
                {"_id": ObjectId(concert_id)},
                {"$set": {"remaining_tickets": remaining_tickets}}
            )
    
    return jsonify({"message": "Transaction updated successfully"}), 200


# Endpoint untuk menghapus transaksi
@app.route("/api/transactions/<transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    if not ObjectId.is_valid(transaction_id):
        return jsonify({"message": "Invalid transaction ID", "status": "error"}), 400
    
    try:
        # Cari transaksi berdasarkan transaction_id
        transaction = transactions_collection.find_one({"_id": ObjectId(transaction_id)})
        
        if not transaction:
            return jsonify({"message": "Transaction not found", "status": "error"}), 404
        
        # Ambil data konser untuk update remaining_tickets
        concert_id = transaction['concert_id']
        quantity_purchased = transaction['quantity']
        
        # Hapus transaksi dari database
        transactions_collection.delete_one({"_id": ObjectId(transaction_id)})

        # Update remaining_tickets pada konser yang terkait
        concert = concerts_collection.find_one({"_id": ObjectId(concert_id)})
        if concert:
            remaining_tickets = concert['remaining_tickets'] + quantity_purchased  # Kembalikan tiket yang dibeli
            concerts_collection.update_one(
                {"_id": ObjectId(concert_id)},
                {"$set": {"remaining_tickets": remaining_tickets}}
            )

        return jsonify({"message": "Transaction deleted successfully", "status": "success"}), 200
    
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


@app.route('/update_realtime', methods=['POST'])
def update_data():
    try:
        # Mengambil data yang dikirimkan oleh client
        data = request.get_json()
        
        # Pastikan data yang diperlukan ada
        if 'message1' not in data or 'message2' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Update data hanya pada fields yang diperlukan di Firebase Realtime Database
        firebase_ref.update({
            'messages/message1': data['message1'],
            'messages/message2': data['message2']
        })

        return jsonify({"message": "Data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

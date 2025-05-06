from flask import Flask, request, jsonify
import sqlite3
import bcrypt

app = Flask(__name__)

# DB setup
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

# Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    # Validate required fields
    if not email or not password or not name:
        return jsonify({'error': 'Missing fields: email, password, or name'}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert user into the db
        cursor.execute(
            'INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)',
            (email, hashed_password.decode('utf-8'), name)
        )
        conn.commit()

        return jsonify({'message': 'User registered successfully!'}), 201

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400

    finally:
        conn.close()

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Verify password hash
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Return user_id directly
        return jsonify({
            'user_id': user['id'],
            'message': 'Login successful'
        }), 200

    except Exception as e:
        return jsonify({'error': 'Server error'}), 500

    finally:
        conn.close()

# User Details Endpoint
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch user by ID
        cursor.execute('SELECT id, email, name FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Convert the SQLite Row object to a dictionary
        user_data = {
            'id': user['id'],
            'email': user['email'],
            'name': user['name']
        }

        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({'error': 'Server error'}), 500

    finally:
        conn.close()

# Home route
@app.route('/')
def hello_world():
    return 'Hello, Account Service!'

if __name__ == '__main__':
    app.run(debug=True)
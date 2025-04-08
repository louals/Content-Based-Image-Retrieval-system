import sqlite3
import bcrypt
import pickle
import face_recognition


def get_db_connection():
    return sqlite3.connect("users.db", check_same_thread=False)


def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        face_encoding BLOB
    )
    """)
    conn.commit()
    conn.close()


def add_user(username, email, password, face_encoding):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  
    face_encoding_blob = pickle.dumps(face_encoding)

    try:
        cursor.execute("INSERT INTO users (username, email, password, face_encoding) VALUES (?, ?, ?, ?)", 
                      (username, email, hashed_password, face_encoding_blob))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  

def user_exists(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None



def face_exists(new_encoding):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT face_encoding FROM users")
    all_face_encodings = cursor.fetchall()
    conn.close()

    for encoding in all_face_encodings:
        stored_encoding = pickle.loads(encoding[0])
        match = face_recognition.compare_faces([stored_encoding], new_encoding)
        if match[0]:
            return True  

    return False 


create_table()
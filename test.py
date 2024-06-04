import mysql.connector
from mysql.connector import errorcode
from passlib.hash import sha256_crypt

hostname = "127.0.0.1"
db = "passionduzen"
username = "root"
password = "1234567"

# Function to hash a password
def hash_password(password):
    return sha256_crypt.hash(password)

# Function to connect to the database
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=db
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Username or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)
        return None


# Function to fetch password from the database and hash it
# Function to fetch password from the database and hash it
def hash_passwords_in_database():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT user_id, password_hash FROM users"  # Replace 'id' with 'user_id'
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                user_id, password = row
                hashed_password = hash_password(password)
                update_query = "UPDATE users SET password_hash = %s WHERE user_id = %s"  # Replace 'id' with 'user_id'
                cursor.execute(update_query, (hashed_password, user_id))
            conn.commit()
            print("Passwords hashed and updated successfully.")
        except mysql.connector.Error as err:
            print("Error hashing passwords:", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

# Call the function to hash passwords in the database
hash_passwords_in_database()

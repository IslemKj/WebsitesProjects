import mysql.connector
from mysql.connector import errorcode
from flask_mail import Message, Mail




# MYSQL CONFIG VARIABLES
hostname = "127.0.0.1"
db = "passionduzen"
username = "root"
password = "1234567"

def getConnection():
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


def get_available_slots():
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM slots WHERE available = 1"
            cursor.execute(query)
            slots = cursor.fetchall()
            return slots
        except mysql.connector.Error as err:
            print("Error fetching available slots:", err)
        finally:
            cursor.close()
            conn.close()
    return []

def insert_booking(full_name, email, phone, slot_id, message, reference_number):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO bookings (full_name, email, phone, slot_id, message, reference_number, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """
            data = (full_name, email, phone, slot_id, message, reference_number)
            cursor.execute(query, data)
            conn.commit()
        except mysql.connector.Error as err:
            print("Error inserting booking:", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            


def get_password_hash(email):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT password_hash FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print("Error fetching password hash:", err)
        finally:
            cursor.close()
            conn.close()
    return None






def get_services():
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM services"
            cursor.execute(query)
            services = cursor.fetchall()
            return services
        except mysql.connector.Error as err:
            print("Error fetching services:", err)
        finally:
            cursor.close()
            conn.close()
    return []

def get_service_by_id(service_id):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM services WHERE id = %s"
            cursor.execute(query, (service_id,))
            service = cursor.fetchone()
            return service
        except mysql.connector.Error as err:
            print("Error fetching service by ID:", err)
        finally:
            cursor.close()
            conn.close()
    return None

def insert_service(service_name, description, duration, price):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO services (service_name, description, duration, price) VALUES (%s, %s, %s, %s)"
            data = (service_name, description, duration, price)
            cursor.execute(query, data)
            conn.commit()
        except mysql.connector.Error as err:
            print("Error inserting service:", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def update_service(service_id, service_name, description, duration, price):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE services SET service_name = %s, description = %s, duration = %s, price = %s WHERE id = %s"
            data = (service_name, description, duration, price, service_id)
            cursor.execute(query, data)
            conn.commit()
        except mysql.connector.Error as err:
            print("Error updating service:", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def delete_service(service_id):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM services WHERE service_id = %s"
            cursor.execute(query, (service_id,))
            conn.commit()
            print("Service deleted successfully!")
        except mysql.connector.Error as err:
            print("Error deleting service:", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def get_slots():
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM slots"
            cursor.execute(query)
            slots = cursor.fetchall()
            return slots
        except mysql.connector.Error as err:
            print("Error fetching slots:", err)
        finally:
            cursor.close()
            conn.close()
    return []

def get_slot_by_id(slot_id):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM slots WHERE id = %s"
            cursor.execute(query, (slot_id,))
            slot = cursor.fetchone()
            return slot
        except mysql.connector.Error as err:
            print("Error fetching slot by ID:", err)
        finally:
            cursor.close()
            conn.close()
    return None

def insert_slot(service_id, slot_date, slot_time, available):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO slots (service_id, slot_date, slot_time, available) VALUES (%s, %s, %s, %s)"
            data = (service_id, slot_date, slot_time, available)
            cursor.execute(query, data)
            conn.commit()
        except mysql.connector.Error as err:
            print("Error inserting slot:", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def update_slot(slot_id, service_id, slot_date, slot_time, available):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE slots SET service_id = %s, slot_date = %s, slot_time = %s, available = %s WHERE id = %s"
            data = (service_id, slot_date, slot_time, available, slot_id)
            cursor.execute(query, data)
            conn.commit()
        except mysql.connector.Error as err:
            print("Error updating slot:", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def delete_slot(slot_id):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM slots WHERE slot_id = %s"
            cursor.execute(query, (slot_id,))
            conn.commit()
            print("Slot deleted successfully!")
        except mysql.connector.Error as err:
            print("Error deleting slot:", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def get_bookings():
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM bookings"
            cursor.execute(query)
            bookings = cursor.fetchall()
            return bookings
        except mysql.connector.Error as err:
            print("Error fetching bookings:", err)
        finally:
            cursor.close()
            conn.close()
    return []

def get_booking_by_id(booking_id):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM bookings WHERE id = %s"
            cursor.execute(query, (booking_id,))
            booking = cursor.fetchone()
            return booking
        except mysql.connector.Error as err:
            print("Error fetching booking by ID:", err)
        finally:
            cursor.close()
            conn.close()
    return None

def insert_booking(full_name, email, phone, slot_id, message, reference_number):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO bookings (full_name, email, phone, slot_id, message, reference_number, created_at) VALUES (%s, %s, %s, %s, %s, %s, NOW())"
            data = (full_name, email, phone, slot_id, message, reference_number)
            cursor.execute(query, data)
            conn.commit()
            print("Booking inserted successfully!")
        except mysql.connector.Error as err:
            print("Error inserting booking:", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def update_booking(booking_id, full_name, email, phone, slot_id, message):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE bookings SET full_name = %s, email = %s, phone = %s, slot_id = %s, message = %s WHERE id = %s"
            data = (full_name, email, phone, slot_id, message, booking_id)
            cursor.execute(query, data)
            conn.commit()
        except mysql.connector.Error as err:
            print("Error updating booking:", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

def delete_booking(booking_id):
    conn = getConnection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM bookings WHERE id = %s"
            cursor.execute(query, (booking_id,))
            conn.commit()
            print("Booking deleted successfully!")
        except mysql.connector.Error as err:
            print("Error deleting booking:", err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            
            
            
            
            

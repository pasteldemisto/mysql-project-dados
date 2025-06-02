import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def connect():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
        )

        if connection.is_connected():
            print("Connected to MySQL Server version:", connection.get_server_info())
            return connection

    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None

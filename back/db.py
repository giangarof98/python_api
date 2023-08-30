import mysql.connector;
from dotenv import load_dotenv
import os;

load_dotenv()

db_config= {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("password"),
    "database": os.getenv("database"),
}
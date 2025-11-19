import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

TABLES = {}

TABLES['sessions'] = (
    "CREATE TABLE IF NOT EXISTS sessions ("
    "session_id int NOT NULL AUTO_INCREMENT,"
    "account_id int NOT NULL,"
    "token varchar(255) NOT NULL,"
    "created_at timestamp NOT NULL,"
    "updated_at timestamp NOT NULL,"
    "PRIMARY KEY (session_id),"
    "FOREIGN KEY (account_id) REFERENCES accounts (account_id) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

TABLES['accounts'] = (
    "CREATE TABLE IF NOT EXISTS accounts ("
    "account_id int NOT NULL AUTO_INCREMENT,"
    "username varchar(255) NOT NULL,"
    "hashed_password varchar(255) NOT NULL," # NOTE: type may need to be changed later
    "email varchar(255) NOT NULL,"
    "created_at timestamp NOT NULL,"
    "role varchar(255) NOT NULL,"
    "PRIMARY KEY (account_id)"
    ") ENGINE=InnoDB"
)

TABLES['orders'] = (
    "CREATE TABLE IF NOT EXISTS orders ("
    "order_id int NOT NULL AUTO_INCREMENT,"
    "account_id int NOT NULL,"
    "total_cost decimal(10,2) NOT NULL,"
    "payment_status varchar(255) NOT NULL,"
    "created_at timestamp NOT NULL,"
    "PRIMARY KEY (order_id),"
    "FOREIGN KEY (account_id) REFERENCES accounts (account_id) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

TABLES["order_items"] = (
    "CREATE TABLE IF NOT EXISTS order_items ("
    "order_item_id int NOT NULL AUTO_INCREMENT,"
    "order_id int NOT NULL,"
    "book_id int NOT NULL,"
    "item_price decimal(10,2) NOT NULL," # NOTE: removed item_type from current schema
    "PRIMARY KEY (order_item_id),"
    "FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE,"
    "FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

TABLES["books"] = (
    "CREATE TABLE IF NOT EXISTS books ("
    "book_id int NOT NULL AUTO_INCREMENT,"
    "title varchar(255) NOT NULL,"
    "author varchar(255) NOT NULL,"
    "synopsis TEXT NOT NULL,"
    "price_buy decimal(10,2) NOT NULL,"
    "price_rent decimal(10,2) NOT NULL,"
    "created_at timestamp," # NOTE: This can be null
    "PRIMARY KEY (book_id)"
    ") ENGINE=InnoDB"
)

TABLES["genres"] = (
    "CREATE TABLE IF NOT EXISTS genres ("
    "genre_id int NOT NULL AUTO_INCREMENT,"
    "name varchar(255) NOT NULL,"
    "PRIMARY KEY (genre_id)"
    ") ENGINE=InnoDB"
)

# FIXME: need to make another table to allow many-to-many with books and genres
TABLES["book_genres"] = (
    "CREATE TABLE IF NOT EXISTS book_genres ("
    "book_id int NOT NULL,"
    "genre_id int NOT NULL,"
    "PRIMARY KEY (book_id, genre_id),"
    "FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,"
    "FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)



TABLES["notifications"] = (
    "CREATE TABLE IF NOT EXISTS notifications ("
    "notification_id int NOT NULL AUTO_INCREMENT,"
    "account_id int NOT NULL,"
    "message TEXT NOT NULL," # TODO: look over this and ensure it's what we want
    "sent_at timestamp NOT NULL,"
    "PRIMARY KEY (notification_id),"
    "FOREIGN KEY (account_id) REFERENCES accounts (account_id) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

TABLES["reviews"] = (
    "CREATE TABLE IF NOT EXISTS reviews ("
    "review_id int NOT NULL AUTO_INCREMENT,"
    "account_id int NOT NULL,"
    "book_id int NOT NULL,"
    "review_content TEXT NOT NULL,"
    "created_at timestamp NOT NULL,"
    "PRIMARY KEY (review_id),"
    "FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE,"
    "FOREIGN KEY (account_id) REFERENCES accounts (account_id) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

cnx = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exist".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()





import bcrypt
import random
from pandas import read_csv
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector
from mysql.connector import Error

CUSTOMER_PASSWORD = os.getenv("CUSTOMER1_PASS")
MANAGER_PASSWORD = os.getenv("MANAGER1_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

# --------- PASSWORD HASHING ----------
def hash_pw(plain):
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

books_df = read_csv("data/books.csv")

# --------- SQL LINES STORAGE ----------
seed_sql = []

# --------- INSERT USERS WITH HASHED PASSWORDS ----------
seed_sql.append(f"""
INSERT INTO accounts (username, hashed_password, email, created_at, role) VALUES
('customer1', '{hash_pw(CUSTOMER_PASSWORD)}', 'zanirpirani@gmail.com', NOW(), 'customer'),
('manager1', '{hash_pw(MANAGER_PASSWORD)}', 'zanirandzishan@gmail.com', NOW(), 'manager');
""")

# --------- GENRE + BOOK MAPPING SETUP ----------
genres_index = {}       # genre_name -> genre_id
genre_id_counter = 1
book_id_counter = 1

# --------- BOOKS + GENRES + M2M (ALL BOOKS) ----------
inserted_pairs = set()   # <-- ADDED: keeps track of (book_id, genre_id)

for _, row in books_df.iterrows():
    title = row["Book Title"].replace("'", "''")
    author = row["Book Author"].replace("'", "''")
    synopsis = row["Summary"].replace("'", "''")

    price_buy = round(random.uniform(5, 30), 2)
    price_rent = round(price_buy * 0.25, 2)

    # insert book
    seed_sql.append(
        f"INSERT INTO books (book_id, title, author, synopsis, price_buy, price_rent, created_at) "
        f"VALUES ({book_id_counter}, '{title}', '{author}', '{synopsis}', {price_buy}, {price_rent}, NOW());"
    )

    # handle genres (row["Genres"] is a LIST)
    for g in row["Genres"]:
        clean_g = g.replace("'", "''")

        # Insert genre only once
        if g not in genres_index:
            genres_index[g] = genre_id_counter
            seed_sql.append(
                f"INSERT INTO genres (genre_id, name) VALUES ({genre_id_counter}, '{clean_g}');"
            )
            genre_id_counter += 1

        # SAFE M2M link (NO DUPLICATES)
        pair = (book_id_counter, genres_index[g])
        if pair not in inserted_pairs:
            seed_sql.append(
                f"INSERT INTO book_genres (book_id, genre_id) "
                f"VALUES ({book_id_counter}, {genres_index[g]});"
            )
            inserted_pairs.add(pair)

    book_id_counter += 1



# --------- REVIEWS FOR FIRST N BOOKS ----------
N = 20  # change this number if you want more or fewer reviews!
VALID_REVIEWERS = [1, 2]  # matches the accounts you inserted

for book_id in range(1, N + 1):
    for acc in VALID_REVIEWERS:
        seed_sql.append(
            f"INSERT INTO reviews (account_id, book_id, review_content, created_at) "
            f"VALUES ({acc}, {book_id}, 'Great book!', NOW());"
        )


try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

    cursor = connection.cursor()

    print("Connected. Running seed SQL...")

    for line in seed_sql:
        if line.strip():
            cursor.execute(line)

    connection.commit()
    cursor.close()
    connection.close()
    print("Database seeded successfully!")

except Error as e:
    print("Error:", e)

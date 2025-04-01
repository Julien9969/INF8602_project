import sqlite3
import random

def get_db():
    conn = sqlite3.connect('database.db')
    return conn

def generate_fake_review(user):
    movie_titles = [
        "Space Explorers VI",
        "The Mystery of the Haunted Mansion 3D",
        "Adventures of Captain Awesome",
        "Love in Paris: A Sequel",
        "Robot Uprising: The Final Battle",
        "Whispers in the Woods",
        "The Great Cake Bake-Off",
        "Sunset Serenade",
        "Neon City Nights",
        "Galactic Guardians",
        "Cars"
    ]
    comments = [
        "A truly cinematic experience!",
        "I laughed, I cried, it was better than Cats.",
        "Not bad, could have been better.",
        "Absolutely terrible, do not waste your time.",
        "A masterpiece! Five stars!",
        "Entertaining and engaging from start to finish.",
        "The special effects were mind-blowing.",
        "The plot was a bit confusing.",
        "I really enjoyed the acting.",
        "A fun movie for the whole family."
    ]
    title = random.choice(movie_titles)
    comment = random.choice(comments)
    rating = round(random.uniform(1, 5), 1)
    return user, title, comment, rating

def populate_fake_reviews(conn, users):
    cursor = conn.cursor()
    for user in users:
        num_reviews = random.randint(5, 10)
        for _ in range(num_reviews):
            user_data = generate_fake_review(user)
            cursor.execute("INSERT INTO movies (user, title, comment, rating) VALUES (?, ?, ?, ?)", user_data)
    conn.commit()

def display_reviews(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    reviews = cursor.fetchall()
    if reviews:
        print("\n--- Fake Movie Reviews ---")
        for review in reviews:
            print(f"User: {review[1]}")
            print(f"Title: {review[2]}")
            print(f"Comment: {review[3]}")
            print(f"Rating: {review[4]}")
            print("-" * 20)
    else:
        print("No movie reviews found.")


def main():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS movies")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE movies (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, title TEXT, comment TEXT, rating REAL)")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('Timmy', 'qwerty11')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('Alice', '123456')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('Bob', 'password123')")
    conn.commit()

    users = ["Timmy", "Alice", "Bob"]
    populate_fake_reviews(conn, users)
    display_reviews(conn)

    conn.close()
    print("Database populated with fake reviews.")

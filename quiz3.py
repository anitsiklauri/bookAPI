import requests
import json
import sqlite3
from win10toast import ToastNotifier

response = requests.get("https://openlibrary.org/api/books?bibkeys=ISBN:9781451648546&format=json&jscmd=data")

print("Status Code:", response.status_code)
print("Headers:", response.headers)

with open("book_info.json", "w") as f:
    json.dump(response.json(), f, indent=4)

with open("book_info.json", "r") as f:
    data = json.load(f)

# Print the title and author of the book
book_info = data["ISBN:9781451648546"]
print("Title:", book_info["title"])
print("Author:", book_info["authors"][0]["name"])

conn = sqlite3.connect("books.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT
    )
""")

# Insert the book information into the books table
title = book_info["title"]
author = book_info["authors"][0]["name"]
cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))

conn.commit()
conn.close()

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# Retrieve the latest book from the books table
cursor.execute("SELECT title, author FROM books ORDER BY id DESC LIMIT 1")
result = cursor.fetchone()

conn.close()

# Create a Windows notification with the book information
toaster = ToastNotifier()
toaster.show_toast(
    result[0],
    result[1],
    duration=10
)

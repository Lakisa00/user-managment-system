import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

conn = mysql.connector.connect(
    host = DB_HOST,
    user = DB_USER,
    password = DB_PASSWORD,
    database = DB_NAME
)
cursor = conn.cursor()
cursor.execute("""
create table if not exists books(
    id int auto_increment primary key, 
    title varchar(100) not null,
    author varchar(100) not null,
    year int,
    available boolean default true
) 
""")
conn.commit()

def add_book(title, author, year):
    pass

def list_books():
    pass

def search_books(keyword):
    pass

def borrow_book(book_id):
    pass

def return_book(book_id):
    pass

def delete_book(book_id):
    pass

while True:
    print("1: Add Book")
    print("2: List Books")
    print("3: Search Books")
    print("4: Borrow Book")
    print("5: Return Book")
    print("6: Delete Book")
    print("7: EXIT")
    choice = input('Choose an Option 1-5: ').strip()
    if choice == '1':
        title = input("Enter Title: ").strip()
        author = input("Enter Author: ").strip()
        year = input("Enter Year: ").strip()
        year = int(year) if year.isdigit() else None
        add_book(title, author, year)
    elif choice == '2':
        list_books()
    elif choice == '3':
        keyword = input("Find Book: ").strip()
        search_books(keyword)
    elif choice == '4':
        book_id = input("Enter Book ID to Borrow: ")
        if book_id.isdigit():
            borrow_book(int(book_id))
        else:
            print("Invalid")
    elif choice == '5':
        book_id = input("Enter Book ID to Return: ")
        if book_id.isdigit():
            return_book(int(book_id))
        else:
            print("Invalid ID")
    elif choice == '6':
        book_id = input("Enter Book ID to Delete Book: ")
        if book_id.isdigit():
            delete_book(int(book_id))
        else:
            print("Invalid Book ID")
    elif choice == '7':
        print('Bye')
        break
    else:
        print("Invalid CHoice Pick the Following Options")
cursor.close()
conn.close()
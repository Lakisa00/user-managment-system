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
    try:
        cursor.execute("insert into books (title, author, year) values (%s,%s,%s)",(title,author,year))
        conn.commit()
        print(f"Book {title} Added Succesfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
def list_books():
    cursor.execute('select * from books')
    rows = cursor.fetchall()
    if not rows:
        print("No books found")
        return
    print("\n--- Book ---")
    for row in rows:
        status = "Available" if row[4] else "Borrowed"
        print(f"ID: {row[0]} | {row[1]} by {row[2]} ({row[3]}) - {status}")
        
def search_books(keyword):
    cursor.execute("select * from books where title like %s", (f"%{keyword}%"))
    rows = cursor.fetchall()
    if not rows:
        print(f"No books found with title containing '{keyword}'.")
        return
    print("\n--- Search Results ---")
    for row in rows:
        status = "Available" if row[4] else "Borrowed"
        print(f"ID: {row[0]} | {row[1]} by {row[2]} ({row[3]}) - {status}")
def borrow_book(book_id):
    cursor.execute("select available from books where id = %s",(book_id,))
    row = cursor.fetchone()
    if not row:
        print("Book is not found")
        return
    if not row[0]:
        print("Book is already borrowed")
        return
    cursor.execute("update books set available = false where id = %s",(book_id,))
    conn.commit()
    print(f"Book ID {book_id} borrowed")
def return_book(book_id):
    cursor.execute("select available from books where id = %s",(book_id))
    row = cursor.fetchone()
    if not row:
        print("Book not found")
        return
    if row[0]:
        print("Book is already available")
        return
    cursor.execute("update books set available = true where id = %s",(book_id,))
    conn.commit()
    print(f'Book ID {book_id} returned')
def delete_book(book_id):
    cursor.execute('delete from users where book_id = %s', (book_id))
    conn.commit()
    if cursor.rowcount == 0:
        print(f'No bookd Found with ID {book_id}')
    else:
        print(f'Book with ID {book_id} has been Deleted')

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
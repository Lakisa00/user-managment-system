import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="laki1234",
    database="test"
)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
)
""")

conn.commit()

def add_user(name, email):
    try:
        cursor.execute("insert into users (name, email) values (%s,%s)",(name, email))
        conn.commit()
        print(f'User {name} Added Succesfully')
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
def list_users():
    cursor.execute('select * from users')
    rows = cursor.fetchall()
    if not rows:
        print("No users found.")
        return
    print("\n--- Users ---")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]}")
        
def search_user(name):
    cursor.execute("SELECT * FROM users WHERE name LIKE %s", (f"%{name}%",))
    rows = cursor.fetchall()
    if not rows:
        print(f"No users found with name containing '{name}'.")
        return
    print("\n--- Search Results ---")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]}")
        
def delete_user(user_id):
    cursor.execute('delete from users where id = %s', (user_id,))
    conn.commit()
    if cursor.rowcount == 0:
        print(f'No User Found with ID {user_id}')
    else:
        print(f'User with ID {user_id} has been Deleted')

while True:
    print('1: Add User')
    print('2: List Users')
    print('3: Search User by Name')
    print('4: Delete User by ID')
    print('5: EXIT')
    choice = input('Choose an Option 1-5: ').strip()
    if choice == '1':
        name = input("Enter Name: ").strip()
        email = input("Enter EMAIL: ").strip()
        add_user(name, email)
    elif choice == '2':
        list_users()
    elif choice == '3':
        name = input("Find User: ").strip()
        search_user(name)
    elif choice == '4':
        user_id = input("Delete User: ").strip()
        if user_id.isdigit():
            delete_user(int(user_id))
        else:
            print('Invalid User ID')
    elif choice == '5':
        print('Goodbye')
        break
    else:
        print('Invalid Choice Pick the Following Options')
cursor.close()
conn.close()
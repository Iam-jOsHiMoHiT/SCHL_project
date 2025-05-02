import mysql.connector
from mysql.connector import errorcode

# Function to create a connection to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="bookstore",
            auth_plugin='mysql_native_password'  # Use native password authentication
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your MySQL credentials.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Error: {err.msg}")
        return None

# Function to create the 'books' table if it doesn't exist
def create_books_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL
            )
        """)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to add a book to the database
def add_book(title, author, price):
    connection = create_connection()
    if connection:
        try:
            create_books_table(connection)
            cursor = connection.cursor()
            query = "INSERT INTO books (title, author, price) VALUES (%s, %s, %s)"
            data = (title, author, price)
            cursor.execute(query, data)
            connection.commit()
            print("Book added successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

# Function to remove a book from the database
def rem_book(book_id):
    connection = create_connection()
    if connection:
        try:
            create_books_table(connection)
            cursor = connection.cursor()
            query = "DELETE FROM books WHERE id = %s"
            data = (book_id,)
            cursor.execute(query, data)
            connection.commit()
            if cursor.rowcount > 0:
                print("Book removed successfully.")
            else:
                print("Book not found.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

# Function to display all books in the database
def display_books():
    connection = create_connection()
    if connection:
        try:
            create_books_table(connection)
            cursor = connection.cursor()
            query = "SELECT * FROM books"
            cursor.execute(query)
            books = cursor.fetchall()
            if not books:
                print("No books in the database.")
            else:
                print("ID  | Title                | Author              | Price")
                print("-" * 50)
                for book in books:
                    print(f"{book[0]:<4}| {book[1]:<20}| {book[2]:<20}| ₹{book[3]:.2f}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

# Example usage
if __name__ == "__main__":
    print("                         ''WELCOME TO THE BOOKSTORE''                         ")
    print("1.ADD BOOK")
    print("2.REMOVE BOOK")
    print("3.DISPLAY BOOKS")
    while True:
        try:
            choice = int(input("ENTER THE FUNCTION YOU WANT TO PERFORM! (1/2/3) :: "))
            if choice == 1:
                title = input("ENTER THE TITLE OF BOOK :: ")
                author = input("ENTER THE NAME OF AUTHOR :: ")
                price = float(input("ENTER THE PRICE OF BOOK :: "))
                print("")
                add_book(title, author, price)
            elif choice == 2:
                book_id = int(input("ENTER THE BOOK ID :: "))
                print("")
                rem_book(book_id)
            elif choice == 3:
                print("")
                display_books()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Error: Please enter a valid number.")


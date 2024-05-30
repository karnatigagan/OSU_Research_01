import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create Authors table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Create Books table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES Authors (id)
)
''')

# Create BorrowRecords table
cursor.execute('''
CREATE TABLE IF NOT EXISTS BorrowRecords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    borrower_name TEXT NOT NULL,
    borrow_date TEXT NOT NULL,
    return_date TEXT,
    FOREIGN KEY (book_id) REFERENCES Books (id)
)
''')

# Commit the changes
conn.commit()

# Function to add a new author
def add_author(name):
    cursor.execute('INSERT INTO Authors (name) VALUES (?)', (name,))
    conn.commit()

# Function to add a new book
def add_book(title, author_id):
    cursor.execute('INSERT INTO Books (title, author_id) VALUES (?, ?)', (title, author_id))
    conn.commit()

# Function to borrow a book
def borrow_book(book_id, borrower_name, borrow_date):
    cursor.execute('INSERT INTO BorrowRecords (book_id, borrower_name, borrow_date) VALUES (?, ?, ?)', (book_id, borrower_name, borrow_date))
    conn.commit()

# Function to return a book
def return_book(record_id, return_date):
    cursor.execute('UPDATE BorrowRecords SET return_date = ? WHERE id = ?', (return_date, record_id))
    conn.commit()

# Function to get all books
def get_books():
    cursor.execute('SELECT Books.id, Books.title, Authors.name FROM Books JOIN Authors ON Books.author_id = Authors.id')
    return cursor.fetchall()

# Function to get all borrow records
def get_borrow_records():
    cursor.execute('SELECT BorrowRecords.id, Books.title, BorrowRecords.borrower_name, BorrowRecords.borrow_date, BorrowRecords.return_date FROM BorrowRecords JOIN Books ON BorrowRecords.book_id = Books.id')
    return cursor.fetchall()





# Example usage
if __name__ == "__main__":
    # Add authors
    add_author('J.K. Rowling')
    add_author('J.R.R. Tolkien')

    # Add books
    add_book('Harry Potter and the Philosopher\'s Stone', 1)
    add_book('The Hobbit', 2)

    # Borrow books
    borrow_book(1, 'John Doe', '2024-05-28')
    borrow_book(2, 'Jane Doe', '2024-05-29')

    # Return a book
    return_book(1, '2024-06-05')

    # Get and print all books
    books = get_books()
    print("Books in library:")
    for book in books:
        print(book)

    # Get and print all borrow records
    borrow_records = get_borrow_records()
    print("\nBorrow records:")
    for record in borrow_records:
        print(record)

# Close the connection
conn.close()


import sqlite3
from book import Book
import db_templates


class Database():

    def __init__(self):

        DATABASE_NAME = 'database.db'
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.connection.cursor()
        self.cursor.execute(db_templates.books_table)
        self.cursor.execute(db_templates.genres_table)
        self.add_new_genres(db_templates.initial_genres, True)


    def add_new_genres(self, genres: list[str], silent: bool = False) -> None:
        """
        The add_new_genres method adds new genres to the genres table in
        the database.

        Args:
        genres (list[str]): A list of strings representing the new genres
        to be added to the database.
        silent (bool): A boolean flag indicating whether to print a message
        if a genre already exists in the database (default is False).

        Behavior:
        If the genre already exists in the database, it either prints a
        message or does so silently based on the silent parameter.
        After attempting to add all the genres, the method commits
        any pending changes to the database.
        """

        for genre in genres:
            query = "INSERT INTO genres (genre_name) VALUES (?)"
            params = (genre,)
            try:
                self.cursor.execute(query, params)
            except Exception:
                if not silent:
                    print(f'{genre} already exists in DB')

        return self.commit_changes()


    def search(self, keyword: str) -> list[tuple]:
        """
        The search method searches for books in the database based on a given
        keyword.

        Args:
        keyword (str): A string representing the keyword to be used for
        searching.

        Returns:
        list[tuple]: A list of tuples, where each tuple represents a book
        record from the database.
        [(UID: int, title: str, author: str, description: str,genre: str,
        amount_of_pages: int), ...]

        Behavior:
        The method converts the provided keyword to lowercase and constructs
        an SQL query to search for books whose title or author contains the
        keyword (case-insensitive). It then executes the query with the
        provided parameters and returns all the matching results fetched from
        the database.
        """

        keyword = keyword.lower()
        query = """
        SELECT * FROM books WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ?
                """
        params = ('%' + keyword + '%', '%' + keyword + '%',)

        self.cursor.execute(query, params)

        return self.cursor.fetchall()

    def get_all_genres(self) -> list[tuple]:
        """
        Retrieves all genres from the database.

        Returns:
        list[tuple]: A list of tuples containing genre names.
        [(genre_name: str), ...]
        """

        query = "SELECT * FROM genres"

        self.cursor.execute(query)

        return self.cursor.fetchall()
    
    def delete_book(self, uid: int) -> None:
        """
        Delete a book from the database by its unique identifier.

        Args:
        uid (int): The unique identifier of the book to delete.
        """

        query, params = 'DELETE FROM books WHERE id = ?', (uid, )

        self.cursor.execute(query, params)

    def add_new_book(self, book: Book) -> None:
        """
        Add a new book to the database.

        Args:
        book (Book): An instance of the Book class representing the book to
        add.
        """

        query = """
        INSERT INTO books (title, author, description, genre, 
        amount_of_pages) VALUES (?, ?, ?, ?, ?)
                """
        params = (book.title, book.author, book.description, book.genre,
                  book.amount_of_pages,)
        
        self.cursor.execute(query, params)

    def get_book_by_uid(self, uid: int) -> tuple:
        """
        Retrieve a book from the database by its unique identifier.

        Args:
        uid (int): The unique identifier of the book to retrieve.

        Returns:
        tuple: A tuple containing book information
        (UID: int, title: str, author: str, description: str, genre: str,
        amount_of_pages: int)
        """

        query, params = "SELECT * FROM books WHERE id = ?", (uid,)

        self.cursor.execute(query, params)

        return self.cursor.fetchone()


    def get_all_books(self) -> list[tuple]:
        """
        Retrieves all books from the database

        Returns:
        list[tuple]: A list of tuples, where each tuple represents a book
        record from the database.
        [(UID: int, title: str, author: str, description: str, genre: str,
        amount_of_pages: int), ...]
        """

        query = "SELECT * FROM books"

        self.cursor.execute(query)

        return self.cursor.fetchall()


    def get_all_books_by_genre(self, genre: str) -> list[tuple]:
        """
        Retrieves all books of a specific genre from the database

        Args:
        genre (str): The genre of the books to retrieve.

        Returns:
        list[tuple]: A list of tuples, where each tuple represents a book
        record from the database.
        [(UID: int, title: str, author: str, description: str, genre: str,
        amount_of_pages: int), ...]
        """

        query, params = "SELECT * FROM books WHERE genre = ?", (genre,)

        self.cursor.execute(query, params)

        return self.cursor.fetchall()


    def get_last_book_added(self) -> tuple:
        """
        Gets the last book added to database.

        Returns:
        tuple: A tuple containing book information
        (UID: int, title: str, author: str, description: str, genre: str,
        amount_of_pages: int)
        """

        query = "SELECT * FROM books WHERE id=(SELECT MAX(id) FROM books)"

        self.cursor.execute(query)
        return self.cursor.fetchone()


    def get_amount_of_books(self) -> int:
        """
        Gets an amount of all records in database.

        Returns:
        int: Amount of all books in database
        """

        return len(self.get_all_books())


    def commit_changes(self) -> None:
        self.connection.commit()


    def close_connection(self) -> None:
        self.commit_changes()
        self.cursor.close()
        self.connection.close()

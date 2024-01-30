"""This file represents a library administration module"""
from db import Database
from prettytable import PrettyTable as pt
from book import Book
from menu import Menu


class Library:
    """Class to manage a library of books."""

    def __init__(self):
        self.db = Database()
        self.menu_tools = Menu()
        self.BOOK_ATTRS = ['UID', 'Title', 'Author',
                           'Description', 'Genre', 'Pages']


    def add_new_genre(self, genre: str):
        """
        Method to add a new genre to the database.

        Args:
        genre (str): New genre to be added.

        Returns:
        str: Added genre.
        """

        if 1 < len(genre) < 64:
            if self._dialog('Add this genre to DB?'):
                self.db.add_new_genres([genre])
                return genre
        else:
            print('Genre max. length is 64 symbols')


    def add_new_book(self) -> None:
        """Method to add a new book to the library."""

        new_book = self.create_book_obj()

        try:
            self.db.add_new_book(new_book)
            self.db.commit_changes()
            last_book_added = self.db.get_last_book_added()
            if last_book_added[1] == new_book.title and last_book_added[5] == new_book.amount_of_pages:
                print('Book added succesfuly, UID:', last_book_added[0])
                return
            else:
                raise Exception(
                    'Could not add a new book to DB. [FAILED ON RESULT CHECK]'
                    )
        except Exception:
            print('An error occured while performing this action.')


    def _get_book_uid_input(self) -> int:
        """
        Get input for book's UID from the user.

        Returns:
        int: Book's UID entered by the user.
        """

        while True:
            book_uid = input("Book's UID: ")
            if not book_uid.isdigit():
                print('Only digit input allowed! Try something else.')
                continue
            elif not self.db.get_book_by_uid(int(book_uid)):
                print('This book does not exist! Try something else')
                continue

            return int(book_uid)


    def _get_book_by_uid(self, book_uid: int) -> tuple:
        """
        Retrieve a book from the database by its unique identifier.

        Args:
        - book_uid (int): The unique identifier of the book to retrieve.

        Returns:
        - tuple: A tuple containing the details of the selected book if found.
        """

        selected_book = self.db.get_book_by_uid(book_uid)
        if not selected_book:
            print('This book doesnt exist! Try something else.')
        else:
            return selected_book


    def _create_table_pages(self, all_books_list) -> list:
        """
        Create a list of table pages for displaying books.

        Args:
        all_books_list: List of all books to be displayed.

        Returns:
        list: List of table pages for displaying books.
        """

        pages = []
        books_per_page = 10

        for i in range(0, len(all_books_list), books_per_page):
            books_for_page = all_books_list[i:i + books_per_page]
            table = pt(self.BOOK_ATTRS)
            for book_tuple in books_for_page:
                book = list(book_tuple)
                if len(book[3]) > 30:
                    book[3] = f'{book[3][:30]}...'
                if len(book[1]) > 15:
                    book[1] = f'{book[1][:15]}...'
                table.add_row(book)
            pages.append(table)

        return pages


    def create_book_obj(self) -> Book:
        """
        Method to create a new book object.

        Returns:
        Book: New book object.
        """

        title = input('Title: ')
        author = input('Author: ')
        description = input('Description: ')
        genre = self._choose_genre_menu()

        while True:
            try:
                pages = int(input('Amount of pages: '))
                break
            except ValueError:
                print('Provide a numeric value!')
        new_book = Book(title, author, description, genre, pages)

        return new_book


    def delete_book(self, book_uid: int) -> bool:
        """
        Delete a book from the database based on its UID.

        Args:
        book_uid (int): UID of the book to be deleted.

        Returns:
        bool: True if the book is successfully deleted, False otherwise.

        Raises:
        Exception: If failed to delete book from DB.
        """

        if self._dialog('Delete book %d?', book_uid):
            self.db.delete_book(book_uid)
            self.db.commit_changes()
            if not self.db.get_book_by_uid(book_uid):
                print('Book is deleted')
                return True
            else:
                raise Exception('''Failed to delete book from DB.
                                [FAILED ON RESULT CHECK]''')
        else:
            return False


    def _dialog(self, question: str, *args) -> bool:
        """
        Display a dialog with the given question and return user's response.

        Args:
        question (str): Question to be displayed.
        args: Additional arguments for formatting the question.

        Returns:
        bool: True if user agrees (Y), False if user disagrees (N).
        """

        while True:
            agreement = input(
                f'{question % args if args else question} Y/N\n>> '
                ).lower()
            if agreement == 'y':
                return True
            elif agreement == 'n':
                return False


    def main_menu(self):
        """Method to add a new book to the library."""

        static_menu_options = ['Add new book', 'Exit']
        dynamic_menu_options = []

        if len(self.db.get_all_books()) != 0:
            for option in ['See all books', 'Delete certain book']:
                dynamic_menu_options.append(option)

        menu = self.menu_tools.create_menu(dynamic_menu_options, 
                                           static_menu_options)
        while True:
            print(menu)
            user_input_menu_option = input('\n>> ')
            choosed_option = self.menu_tools.get_choosed_menu_option(menu,
                                                    user_input_menu_option)
            if choosed_option:
                if 'Add new book' in choosed_option:
                    self.add_new_book()
                    return self.certain_book_menu(
                        self.db.get_last_book_added()[0])
                elif 'Exit' in choosed_option:
                    return exit()

                if dynamic_menu_options:
                    if 'Delete certain book' in choosed_option:
                        book_uid = self._get_book_uid_input()
                        self.delete_book(book_uid)
                    elif 'See all books' in choosed_option:
                        return self.all_books_menu()
                        
            else:
                print('Wrong option! Try something else.')


    def _choose_genre_menu(self, allow_add_new_genre = True) -> str:
        """
        Method to choose a genre from the menu or add a new one.

        Args:
        allow_add_new_genre (bool): Flag to allow adding a new genre.

        Returns:
        str: Chosen (or added) genre.
        """

        menu = self.menu_tools.create_menu(
            [i[1] for i in self.db.get_all_genres()])
        
        while True:
            print(f'Existing genres:\n{menu}')
            user_input_menu_option = input(f'''
                Choose one by typing in a digit
                {", or provide a new one:" if allow_add_new_genre else ":"}
                \n>> 
                                            ''')
            if user_input_menu_option.isdigit():
                genre = self.menu_tools.get_choosed_menu_option(
                    menu, user_input_menu_option)
                if genre:
                    return genre
                else:
                    print('-'*50, 'Non-existing option!')
            elif allow_add_new_genre:
                return self.add_new_genre()
            else:
                print('Only digits allowed')


    def certain_book_menu(self, book_uid: int):
        """
        Display detailed information about a specific book and provide options
        to delete the book or return to the main book menu.

        Args:
        - book_uid (int): The unique identifier of the book to display.
        """

        selected_book = self.db.get_book_by_uid(book_uid)
        static_menu_options = ['Delete', 'Back to all books']
        menu = self.menu_tools.create_menu(static_menu_options)

        while True:
            print('\n\n', '-'*15)
            for attr_name, selected_book_attr_value in  zip(self.BOOK_ATTRS,
                                                            selected_book):
                print(f'-- {attr_name}: {selected_book_attr_value}')
            print('-'*15)
            print(menu)
            user_input_menu_option = input('\n>> ')
            choosed_option = self.menu_tools.get_choosed_menu_option(menu, 
                                                    user_input_menu_option)
            if choosed_option:
                if "Delete" in choosed_option:
                    if self.delete_book(book_uid):
                        return self.all_books_menu()
                elif "Back to all books" in choosed_option:
                    return self.all_books_menu()
            else:
                print('Wrong option! Try something else.')


    def search_menu(self):
        """
        Display a search menu to allow users to search for books by author or
        title.

        The search is performed using the provided keyword, and the results
        are displayed in paginated format. Users can select a certain book,
        delete a certain book, go back to the main menu, change the search
        keyword, or exit the program.

        The method handles user input validation and provides appropriate
        feedback for incorrect input.

        Note: The method relies on other internal methods and properties of
        the class to perform database operations and handle user interactions.
        """

        print('''
              NOTICE: search will be performed between author and title of
              the book.
              \nMay not work properly if you use non-English letters.\n\n
              ''')
        
        current_page = 0

        while True:
            search_keyword = input('Search keyword\n>> ')
            search_result = self.db.search(search_keyword)
            if not search_result:
                print('No books matching this keyword were found, try again')
            else:
                break

        table_pages = self._create_table_pages(search_result)
        static_menu_options = ['Select certain book', 'Delete certain book',
            'Go back to main menu', 'Change keyword', 'Exit']
        
        while True:
            dynamic_menu_options = []
            if current_page+1 < len(table_pages):
                dynamic_menu_options.append('Next page')
            if len(table_pages) > 1 and current_page+1 > 1:
                dynamic_menu_options.append('Previous page')
            menu = self.menu_tools.create_menu(dynamic_menu_options,
                                               static_menu_options)
            print(table_pages[current_page])
            print(f'Page {current_page+1}/{len(table_pages)}\n')
            print(menu)
            user_input_menu_option = input('\n>> ')
            choosed_option = self.menu_tools.get_choosed_menu_option(menu,
                                                    user_input_menu_option)

            if choosed_option:
                if "Select certain book" in choosed_option:
                    selected_book = self._get_book_uid_input()
                    return self.certain_book_menu(selected_book)
                elif 'Delete certain book' in choosed_option:
                    book_uid = self._get_book_uid_input()
                    self.delete_book(book_uid)
                    pass
                elif 'Go back to main menu' in choosed_option:
                    return self.main_menu()
                elif 'Change keyword' in choosed_option:
                    return self.search_menu()
                elif 'Exit' in choosed_option:
                    return exit()

                if dynamic_menu_options:
                    if "Next page" in choosed_option:
                        current_page += 1
                    elif "Previous page" in choosed_option:
                        current_page -= 1
            else:
                print('Wrong option! Try something else.')     


    def filter_by_genre_menu(self):
        """
        Display a filter menu to allow users to filter books by genre.

        The filter is performed using the provided genre, and the results
        are displayed in paginated format. Users can select a certain book,
        delete a certain book, go back to the main menu, change the filter
        genre, or exit the program.

        The method handles user input validation and provides appropriate
        feedback for incorrect input.

        Note: The method relies on other internal methods and properties of
        the class to perform database operations and handle user interactions.
        """


        while True:
            genre = self._choose_genre_menu(allow_add_new_genre=False)
            all_books_list = self.db.get_all_books_by_genre(genre)
            if not all_books_list:
                print('No books with choosen genre found, try another one')
            else:
                break

        current_page = 0
        pages = self._create_table_pages(all_books_list)   
        static_menu_options = ['Select certain book', 'Delete certain book',
                               'Go back to main menu', 'Change filter',
                               'Exit']
        while True:
            dynamic_menu_options = []
            if current_page+1 < len(pages):
                dynamic_menu_options.append('Next page')
            if len(pages) > 1 and current_page+1 > 1:
                dynamic_menu_options.append('Previous page')
            menu = self.menu_tools.create_menu(dynamic_menu_options,
                                               static_menu_options)
            print(pages[current_page])
            print(f'Page {current_page+1}/{len(pages)}\n')
            print(menu)
            user_input_menu_option = input('\n>> ')
            choosed_option = self.menu_tools.get_choosed_menu_option(
                menu, user_input_menu_option)

            if choosed_option:
                if "Select certain book" in choosed_option:
                    selected_book = self._get_book_uid_input()
                    return self.certain_book_menu(selected_book)
                elif 'Delete certain book' in choosed_option:
                    book_uid = self._get_book_uid_input()
                    self.delete_book(book_uid)
                elif 'Go back to main menu' in choosed_option:
                    return self.main_menu()
                elif 'Change filter' in choosed_option:
                    return self.filter_by_genre_menu()
                elif 'Exit' in choosed_option:
                    return exit()

                if dynamic_menu_options:
                    if "Next page" in choosed_option:
                        current_page += 1
                    elif "Previous page" in choosed_option:
                        current_page -= 1
            else:
                print('Wrong option! Try something else.')


    def all_books_menu(self) -> None:
        """
        The method retrieves all books from the database and paginates the
        data to display it in a user-friendly format.

        It then presents a menu with options for the user to interact with
        the list of books.

        The method handles user input validation and provides appropriate
        feedback for incorrect input.

        Note: The method relies on other internal methods and properties of
        the class to perform database operations and handle user interactions.
        """

        current_page = 0
        all_books_list = self.db.get_all_books()
        pages = self._create_table_pages(all_books_list)
        static_menu_options = ['Select certain book', 'Delete certain book',
                               'Search by keyword', 'Filter by genre',
                               'Go back to main menu', 'Exit']
        while True:
            dynamic_menu_options = []
            if current_page+1 < len(pages):
                dynamic_menu_options.append('Next page')
            if len(pages) > 1 and current_page+1 > 1:
                dynamic_menu_options.append('Previous page')
            menu = self.menu_tools.create_menu(dynamic_menu_options,
                                               static_menu_options)
            print(pages[current_page])
            print(f'Page {current_page+1}/{len(pages)}\n')
            print(menu)
            user_input_menu_option = input('\n>> ')
            choosed_option = self.menu_tools.get_choosed_menu_option(
                menu, user_input_menu_option)

            if choosed_option:
                if "Select certain book" in choosed_option:
                    selected_book = self._get_book_uid_input()
                    return self.certain_book_menu(selected_book)
                elif 'Delete certain book' in choosed_option:
                    book_uid = self._get_book_uid_input()
                    self.delete_book(book_uid)
                elif 'Search by keyword' in choosed_option:
                    return self.search_menu()
                elif 'Filter by genre' in choosed_option:
                    return self.filter_by_genre_menu()
                elif 'Go back to main menu' in choosed_option:
                    return self.main_menu()
                elif 'Exit' in choosed_option:
                    return exit()

                if dynamic_menu_options:
                    if "Next page" in choosed_option:
                        current_page += 1
                    elif "Previous page" in choosed_option:
                        current_page -= 1
            else:
                print('Wrong option! Try something else.')


if __name__ == '__main__':
    lib = Library()
    lib.main_menu()

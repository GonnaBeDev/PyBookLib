"""A book class for Library"""

class Book:
    
    def __init__(self, title: str, author: str, description: str,
                 genre: str, amount_of_pages: int) -> None:
        
        self.title = title
        self.author = author
        self.description = description
        self.genre = genre
        self.amount_of_pages = amount_of_pages

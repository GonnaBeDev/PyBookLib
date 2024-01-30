"""Templates for db.py"""

books_table = """
CREATE TABLE IF NOT EXISTS books (
                id              INTEGER       PRIMARY KEY
                                            UNIQUE
                                            NOT NULL,
                title           TEXT (1, 256) NOT NULL,
                author           TEXT (1, 128) NOT NULL,
                description     TEXT (0, 512),
                genre           TEXT (1, 64) NOT NULL,
                amount_of_pages INTEGER (1)   NOT NULL
            );
"""

genres_table = """
CREATE TABLE IF NOT EXISTS genres (
        id              INTEGER       PRIMARY KEY
                                    UNIQUE
                                    NOT NULL,
        genre_name           TEXT (1, 64) NOT NULL
                            UNIQUE
            );
"""

initial_genres = ['Fantasy', 'Romance', 'Detective', 'Sci-Fi',
                  'Thriller', 'Comedy', 'Classics']
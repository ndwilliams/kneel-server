import sqlite3

DB_PATH = "./kneeldiamonds.sqlite3"


class Size:

    def __init__(self):
        self.id = 0
        self.carets = ""
        self.price = 0

    def create(self, id, carets, price):
        size = Size()
        size.id = id
        size.carets = carets
        size.price = price
        return size

    def get_single(self, pk):
        sql = """
        SELECT
            s.id,
            s.carets,
            s.price
        FROM
            Sizes s
        WHERE s.id = ?
        """
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(sql, (pk,))
            row = db_cursor.fetchone()

            new_size = self.create(
                row["id"],
                row["carets"],
                row["price"],
            )

            return new_size.__dict__

    def get_all(self):
        sql = """SELECT * FROM Sizes"""

        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(sql)
            rows = db_cursor.fetchall()

            sizes = []

            for row in rows:
                new_size = self.create(
                    row["id"],
                    row["carets"],
                    row["price"]
                )

                sizes.append(new_size.__dict__)

            return sizes

    def db_create(self, data_tuple) -> int:
        sql = """
        INSERT INTO Sizes Values(null, ?, ?)"""
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(sql, (data_tuple["carets"], data_tuple["price"]))
            return db_cursor.lastrowid

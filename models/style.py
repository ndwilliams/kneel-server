import sqlite3

DB_PATH = "./kneeldiamonds.sqlite3"


class Style:

    def __init__(self):
        self.id = 0
        self.name = ""
        self.price = 0

    def create(self, id, name, price):
        style = Style()
        style.id = id
        style.name = name
        style.price = price
        return style

    def get_single(self, pk):
        sql = """
        SELECT
            s.id,
            s.name,
            s.price
        FROM
            Styles s
        WHERE s.id = ?
        """
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(sql, (pk,))
            row = db_cursor.fetchone()

            new_style = self.create(
                row["id"],
                row["name"],
                row["price"],
            )

            return new_style.__dict__

    def get_all(self):
        sql = """SELECT * FROM Styles"""

        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(sql)
            rows = db_cursor.fetchall()

            styles = []

            for row in rows:
                new_style = self.create(
                    row["id"],
                    row["name"],
                    row["price"]
                )

                styles.append(new_style.__dict__)

            return styles

    def db_create(self, data_tuple) -> int:
        sql = """
        INSERT INTO Styles Values(null, ?, ?)"""
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(sql, (data_tuple["name"], data_tuple["price"]))
            return db_cursor.lastrowid

    def db_update(self, data_tuple, url) -> int:
        sql = """
        UPDATE Styles 
        SET 
            name = ?, 
            price = ?
        WHERE id = ? 
        """
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(
                sql, (data_tuple["name"], data_tuple["price"], url["pk"]))
            return db_cursor.rowcount

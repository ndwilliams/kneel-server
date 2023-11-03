import sqlite3

DB_PATH = "./kneeldiamonds.sqlite3"


class Metal:

    def __init__(self):
        self.id = 0
        self.type = ""
        self.price = 0

    def create(self, id, type, price):
        metal = Metal()
        metal.id = id
        metal.type = type
        metal.price = price
        return metal

    def get_single(self, pk):
        sql = """
        SELECT
            m.id,
            m.type,
            m.price
        FROM
            Metals m
        WHERE m.id = ?
        """
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(sql, (pk,))
            row = db_cursor.fetchone()

            new_metal = self.create(
                row["id"],
                row["type"],
                row["price"],
            )

            return new_metal.__dict__

    def get_all(self):
        sql = """SELECT * FROM Metals"""

        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(sql)
            rows = db_cursor.fetchall()

            metals = []

            for row in rows:
                new_metal = self.create(
                    row["id"],
                    row["type"],
                    row["price"]
                )

                metals.append(new_metal.__dict__)

            return metals

    def db_create(self, data_tuple) -> int:
        sql = """
        INSERT INTO Metals Values(null, ?, ?)"""
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(sql, (data_tuple["type"], data_tuple["price"]))
            return db_cursor.lastrowid

    def db_update(self, data_tuple, url) -> int:
        sql = """
        UPDATE Metals 
        SET 
            type = ?, 
            price = ?
        WHERE id = ? 
        """
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(
                sql, (data_tuple["type"], data_tuple["price"], url["pk"]))
            return db_cursor.rowcount

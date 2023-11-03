import sqlite3
from datetime import date

DB_PATH = "./kneeldiamonds.sqlite3"


class Order:

    def __init__(self):
        self.id = 0
        self.metal_id = 0
        self.size_id = 0
        self.style_id = 0

    def create(self, id, metal_id, size_id, style_id, timestamp):
        order = Order()
        order.id = id
        order.metal_id = metal_id
        order.size_id = size_id
        order.style_id = style_id
        order.timestamp = timestamp
        return order

    def get_single(self, pk):
        sql = """
        SELECT * FROM Orders WHERE id = ?
        """
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(sql, (pk,))
            row = db_cursor.fetchone()

            new_order = self.create(
                row["id"],
                row["metal_id"],
                row["size_id"],
                row["style_id"],
                row["timestamp"]
            )

            return new_order.__dict__

    def get_all(self):
        sql = """SELECT * FROM Orders"""

        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(sql)
            rows = db_cursor.fetchall()

            orders = []

            for row in rows:
                new_order = self.create(
                    row["id"],
                    row["metal_id"],
                    row["size_id"],
                    row["style_id"],
                    row["timestamp"]
                )

                orders.append(new_order.__dict__)

            return orders

    def db_create(self, data_tuple) -> int:
        sql = """
        INSERT INTO Orders (metal_id, size_id, style_id) VALUES (?, ?, ?)"""
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(
                sql, (data_tuple["metal_id"], data_tuple["size_id"], data_tuple["style_id"]))
            return db_cursor.lastrowid

    def db_update(self, data_tuple, url) -> int:
        sql = """
        UPDATE Orders 
        SET 
            metal_id = ?, 
            size_id = ?,
            style_id = ?, 
            timestamp = CURRENT_DATE
        WHERE id =?
        """
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute(
                sql, (data_tuple["metal_id"], data_tuple["size_id"], data_tuple["style_id"], url["pk"]))
            return db_cursor.rowcount

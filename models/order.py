import sqlite3
from datetime import date

DB_PATH = "./kneeldiamonds.sqlite3"


class Order:

    def __init__(self):
        self.id = 0
        self.metal_id = 0
        self.size_id = 0
        self.style_id = 0
        self.size = {}
        self.metal = {}
        self.style = {}

    def create(self, id, metal_id, size_id, style_id):
        order = Order()
        order.id = id
        order.metal_id = metal_id
        order.size_id = size_id
        order.style_id = style_id

        return order

    def get_single(self, url):
        if url["query_params"]:
            expansion = url["query_params"]["_expand"]
            if any(parameter in expansion for parameter in ("metal", "size", "style")):

                sql = """SELECT
                            o.id,
                            o.metal_id,
                            o.size_id,
                            o.style_id,
                            m.id metal_pk,
                            m.type,
                            m.price metal_price,
                            si.id size_pk,
                            si.carets,
                            si.price size_price,
                            st.id style_pk,
                            st.name,
                            st.price style_price
                        FROM 
                            Orders o
                        JOIN 
                            Sizes si ON o.size_id = si.id
                        JOIN
                            Styles st ON o.style_id = st.id
                        JOIN 
                            Metals m ON o.metal_id = m.id
                        WHERE o.id = ?                
                    """

                with sqlite3.connect(DB_PATH) as conn:
                    conn.row_factory = sqlite3.Row
                    db_cursor = conn.cursor()
                    db_cursor.execute(sql, (url["pk"],))
                    row = db_cursor.fetchone()

                metal = {
                    "id": row["metal_pk"],
                    "type": row["type"],
                    "price": row["metal_price"]
                }
                size = {
                    "id": row["size_pk"],
                    "carets": row["carets"],
                    "price": row["size_price"]
                }
                style = {
                    "id": row["style_pk"],
                    "name": row["name"],
                    "price": row["style_price"]
                }

                new_order = self.create(
                    row["id"],
                    row["metal_id"],
                    row["size_id"],
                    row["style_id"]
                )

                if "metal" in expansion:
                    new_order.metal = metal
                else:
                    delattr(new_order, "metal")
                if "style" in expansion:
                    new_order.style = style
                else:
                    delattr(new_order, "style")
                if "size" in expansion:
                    new_order.size = size
                else:
                    delattr(new_order, "size")

        else:
            sql = """SELECT * FROM Orders WHERE id = ?"""
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                db_cursor = conn.cursor()
                db_cursor.execute(sql, (url["pk"],))
                row = db_cursor.fetchone()

            new_order = self.create(
                row["id"],
                row["metal_id"],
                row["size_id"],
                row["style_id"]
            )

            delattr(new_order, "metal")
            delattr(new_order, "size")
            delattr(new_order, "style")

        return new_order.__dict__

    def get_all(self, url):
        if url["query_params"]:
            expansion = url["query_params"]["_expand"]
            if any(parameter in expansion for parameter in ("metal", "size", "style")):

                sql = """SELECT
                            o.id,
                            o.metal_id,
                            o.size_id,
                            o.style_id,
                            m.id metal_pk,
                            m.type,
                            m.price metal_price,
                            si.id size_pk,
                            si.carets,
                            si.price size_price,
                            st.id style_pk,
                            st.name,
                            st.price style_price
                        FROM 
                            Orders o
                        JOIN 
                            Sizes si ON o.size_id = si.id
                        JOIN
                            Styles st ON o.style_id = st.id
                        JOIN 
                            Metals m ON o.metal_id = m.id                
                    """

                with sqlite3.connect(DB_PATH) as conn:
                    conn.row_factory = sqlite3.Row
                    db_cursor = conn.cursor()
                    db_cursor.execute(sql)
                    rows = db_cursor.fetchall()

                    orders = []

                    for row in rows:
                        metal = {
                            "id": row["metal_pk"],
                            "type": row["type"],
                            "price": row["metal_price"]

                        }
                        size = {
                            "id": row["size_pk"],
                            "carets": row["carets"],
                            "price": row["size_price"]
                        }
                        style = {
                            "id": row["style_pk"],
                            "name": row["name"],
                            "price": row["style_price"]
                        }

                        new_order = self.create(
                            row["id"],
                            row["metal_id"],
                            row["size_id"],
                            row["style_id"]
                        )

                        if "metal" in expansion:
                            new_order.metal = metal
                        else:
                            delattr(new_order, "metal")
                        if "style" in expansion:
                            new_order.style = style
                        else:
                            delattr(new_order, "style")
                        if "size" in expansion:
                            new_order.size = size
                        else:
                            delattr(new_order, "size")

                        orders.append(new_order.__dict__)
        else:
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
                        row["style_id"]
                    )

                    delattr(new_order, "metal")
                    delattr(new_order, "size")
                    delattr(new_order, "style")

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

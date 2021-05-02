import sqlite3


class DBContent:
    def __init__(self):
        self.con = sqlite3.connect('../db.sqlite3')
        self.cursor = self.con.cursor()

    def categories(self):
        self.cursor.execute('SELECT * FROM bot_content_category')
        rows_categories = self.cursor.fetchall()
        return rows_categories

    def products(self):
        self.cursor.execute('SELECT * FROM bot_content_product')
        rows_products = self.cursor.fetchall()
        return rows_products


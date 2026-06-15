import sqlite3
import pathlib

#later on implement partial delivery of db rows

def dict_factory(cursor, row):
            fields = [column[0] for column in cursor.description]
            return {key: value for key, value in zip(fields, row)}
        
ROOT_PATH = pathlib.Path(__file__).resolve().parent.parent

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect(ROOT_PATH/"backend/posts.db")
        self.conn.row_factory = dict_factory
        self.cur = self.conn.cursor()
        self._create_db()
        
    def _create_db(self):
        self.cur.execute(
        """
        CREATE TABLE IF NOT EXISTS posts(
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "post_id" TEXT UNIQUE,
        "post_date" TEXT,
        "author" TEXT,
        "post_content" TEXT
        ) STRICT;""")
        
        self.conn.commit()

    def insert_parsed_data(self,parsed_data:list[dict]):
        for post_dict in parsed_data:
            post_id = post_dict["id"]
            post_author = post_dict["author"]
            post_content = post_dict["text"]
            post_date = post_dict["date"]

            self.cur.execute(
            """
            INSERT OR IGNORE INTO posts (post_id,post_date,author,post_content)
            VALUES (?,?,?,?)
            """,
            (post_id,post_date,post_author,post_content)      
            )
        self.conn.commit()

    def _get_table(self):
        self.cur.execute("SELECT * FROM posts")
        return self.cur.fetchall()

    def _insert_one(self,id,date,author,content):
        self.cur.execute(
            """
            INSERT OR IGNORE INTO posts (post_id,post_date,author,post_content)
            VALUES (?,?,?,?)
            """,
            (id,date,author,content)      
            )
        self.conn.commit()

    def _clear_table(self):
        self.cur.execute(
        """
        DELETE FROM posts
        """
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
    
    def export(self):

        self.cur.execute("SELECT * FROM posts")
        return self.cur.fetchall()

if __name__ == "__main__":
    test = DBManager()
    test._clear_table()

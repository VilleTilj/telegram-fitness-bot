import sqlite3
from contextlib import contextmanager


class DB_helper:
    def __init__(self, db_name='excercises.db') -> None:
        self.dbname = db_name
        

    @contextmanager
    def cursor(self):
        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()
            yield cur
            conn.commit()
        finally:
            conn.close()
    
    def setup(self):
        with self.cursor() as cur:
            stmt = "CREATE TABLE IF NOT EXISTS planking (user text not null, created date, result integer not null)"
            cur.execute(stmt)

    
    def add_planking_results(self, user, date, result):
        with self.cursor() as cur:
            stmt = "INSERT INTO planking values(?,?,?)"
            args = (user, date, result)
            cur.execute(stmt, args)


    def delete_planking_result(self, user):
        with self.cursor() as cur:
            stmt = "DELETE FROM planking WHERE user = (?) and rowid = (SELECT MAX(rowid) FROM planking);"
            args = (user, )
            cur.execute(stmt, args)
        

    def get_plank_results(self):
        with self.cursor() as cur:
            stmt = "SELECT user, created, result FROM planking"
            cur.execute(stmt)
            rows = cur.fetchall()
            data = {}
            for row in rows:
                user, created, result = row
                if user not in data:
                    data[user] = []
                data[user].append((created, result))

        return data 
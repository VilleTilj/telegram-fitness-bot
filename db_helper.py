import sqlite3

class DB_helper:
    def __init__(self, db_name='excercises.db') -> None:
        self.dbname = db_name
        self.conn = sqlite3.connect(db_name)
    
    def setup(self):
        self.conn = sqlite3.connect(self.dbname)
        stmt = "CREATE TABLE IF NOT EXISTS planking (user text not null, created date, result integer not null)"
        self.conn.execute(stmt)
        self.conn.commit()
        self.conn.close()
    
    def add_planking_results(self, user, date, result):
        self.conn = sqlite3.connect(self.dbname)
        stmt = "INSERT INTO planking values(?,?,?)"
        args = (user, date, result)
        self.conn.execute(stmt, args)
        self.conn.commit()
        self.conn.close()

    def delete_planking_result(self, user):
        self.conn = sqlite3.connect(self.dbname)
        stmt = "DELETE FROM planking WHERE user = (?) and id = (SELECT MAX(id) FROM planking);"
        args = (user, )
        self.conn.execute(stmt, args)
        self.conn.commit()
        self.conn.close()

    def get_plank_results(self):
        self.conn = sqlite3.connect(self.dbname)
        stmt = "SELECT result FROM planking"
        results = [x[0] for x in self.conn.execute(stmt)]
        self.conn.close()

        return results 
import sqlite3

class DB_helper:
    def __init__(self, db_name='excercises.db') -> None:
        self.dbname = db_name
        self.conn = sqlite3.connect(db_name)
    
    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS planking (user text not null, created date, result integer not null)"
        self.conn.execute(stmt)
        self.conn.commit()
    
    def add_planking_results(self, user, date, result):
        stmt = "INSERT INTO planking values(?,?,?)"
        args = (user, date, result)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_planking_result(self, user):
        stmt = "DELETE FROM planking WHERE user = (?) and id = (SELECT MAX(id) FROM planking);"
        args = (user, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_plank_results(self):
        stmt = "SELECT result FROM planking"
        return [x[0] for x in self.conn.execute(stmt)]
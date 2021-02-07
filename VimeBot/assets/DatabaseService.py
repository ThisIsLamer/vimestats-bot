from loguru import logger

from assets.Database.userbind import start, add, remove, getNick


class DatabaseService():

    def __init__(self):
        self.base = start()
        self.sql = self.base[1]
        self.db = self.base[0]

    def add(self, id, nick):
        add(sql=self.sql, db=self.db, id=id, nick=nick)

    def remove(self, id):
        remove(sql=self.sql, db=self.db, id=id)

    def getNick(self, id):
        return getNick(sql=self.sql, db=self.db, id=id)

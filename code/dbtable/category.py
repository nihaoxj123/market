from code.tools import dbutil

class Category:

    def __init__(self,id,name):
        self.id = id
        self.name = name

    def toDict(self) -> dict:
        json = {}
        json['id'] = self.id
        json['name'] = self.name
        return json

    def __str__(self):
        return str(self.toDict())



def create(name):
    db = dbutil.openDb()

    sql = f'''INSERT INTO TCategory (NAME) VALUES('{name}')'''
    id = dbutil.insert(db,sql)
    db.close()
    return id

def selectAll():
    db = dbutil.openDb()

    sql = 'SELECT id,name FROM TCategory'
    cList = dbutil.select(db,sql)
    db.close()

    list = []
    if cList:
        for c in cList:
            list.append(Category(c[0],c[1]).toDict())
    return list

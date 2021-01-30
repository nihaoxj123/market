import MySQLdb

# 打开数据库并返回游标
def openDb():
    db = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        password='aa123456',
        database='test',charset='gbk')
    return db

# 查询 返回查询到的数据
def select(db,sql):
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

# 插入数据
def insert(db,sql):
    id = 0
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        id = db.insert_id()
        db.commit()
    except BaseException as e:
        print('insert:',e)
        db.rollback()
    finally:
        return id

# 更新
def update(db,sql):
    cursor = db.cursor()
    count = 0
    try:
        cursor.execute(sql)
        count = cursor.rowcount
        db.commit()
    except BaseException as e:
        db.rollback()
        print('update',e)
    finally:
        return count

# 删除
def delete(db,sql):
    return update(db,sql)

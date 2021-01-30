from code.tools import dbutil


class User:

    def __init__(self,id:int,usercode:str,nickname:str,password:str,createtime:str):
        self.id = id
        self.userCode = usercode
        self.nickName = nickname
        self.password = password
        self.createTime = str(createtime)

    @classmethod
    def newUser(self,nickname:str,password:str):
        return User(0,'',nickname,password,'')

    def __str__(self):
        json ={}
        json['id'] = self.id
        json['userCode'] = self.userCode
        json['nickName'] = self.nickName
        json['password'] = self.password
        json['createTime'] = self.createTime
        return str(json)

'''
    创建一个用户
    user对象nickname和password必须要有值
'''
def create(user:User):
    db = dbutil.openDb()
    sql = """INSERT INTO tuser (usercode,nickname,password,createtime) VALUES((SELECT val+1 FROM TConfig WHERE id = 1),'%s','%s',NOW())"""%(user.nickName,user.password)
    id = dbutil.insert(db, sql)
    if id :
        user.id = id
        dbutil.update(db, 'UPDATE tconfig SET val=val+1 WHERE id = 1')
    db.close()
    return id

'''
    通过nickName查找用户
'''
def selectUserByCode(userCode:str):
    db = dbutil.openDb()
    sql = f"SELECT id,userCode,nickName,password,createTime FROM tuser WHERE userCode = '{userCode}'"
    result = dbutil.select(db, sql)
    db.close()
    if result:
        re = result[0]
        return User(re[0],re[1],re[2],re[3],re[4])

'''
    通过id查找用户
'''
def selectUserById(id):
    db = dbutil.openDb()
    sql = f"SELECT id,userCode,nickName,password,createTime,adminType FROM tuser WHERE id = '{id}'"
    result = dbutil.select(db, sql)
    db.close()
    if result:
        re = result[0]
        u = User(re[0], re[1], re[2], re[3], re[4])
        u.adminType = re[5]
        return u

def selectAdminByCode(usercode:str):
    db = dbutil.openDb()
    sql = f"SELECT id,userCode,nickName,password,createTime FROM tuser WHERE userCode = '{usercode}' AND adminType = '1'"
    result = dbutil.select(db, sql)
    db.close()
    if result:
        re = result[0]
        return User(re[0], re[1], re[2], re[3], re[4])

# 成为卖家
def updateAdminType(userId):
    db = dbutil.openDb()
    sql = "UPDATE tuser SET adminType = '1' WHERE id = %s"%userId
    count = dbutil.update(db,sql)
    db.close()
    return count

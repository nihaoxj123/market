from code.tools import dbutil

class Shop:
    def __init__(self,id:int,title:str,price:float,number:int,payNum=0,status='',createTime='',categoryName='',img=''):
        self.id = id
        self.title = title
        self.price = price
        self.number = number
        self.payNum = payNum
        self.status = status
        self.createTime = str(createTime)
        self.categoryName = categoryName
        self.img = img

    def __str__(self):
        json = self.toDict()
        return str(json)

    @classmethod
    def newShop(self,title:str,price:float,number:int,img):
        return Shop(0,title,price,number,img=img)

    def toDict(self) -> dict:
        json = {}
        json['id'] = self.id
        json['title'] = self.title
        json['price'] = str(self.price)
        json['number'] = self.number
        json['payNum'] = self.payNum
        json['status'] = self.status
        json['createTime'] = self.createTime
        json['categoryName'] = self.categoryName
        json['img'] = self.img
        json['shopSign'] = '阳江小店'
        return json




'''
查询所有商品
'''
def selectAll():
    db = dbutil.openDb()
    sql = '''SELECT id,title,price,number,payNum,status,createTime,img FROM tshop WHERE status = '1' AND adminId IN(SELECT id FROM tuser WHERE admintype = '1')'''
    result = dbutil.select(db, sql)

    shops = []
    if result:
        for re in result:
            shop = Shop(re[0],re[1],re[2],re[3],re[4],re[5],re[6],img=re[7])
            shops.append(shop.toDict())
    return shops

'''
查询指定用户添加的商品
'''
def selectByAdminId(adminId):
    db = dbutil.openDb()
    sql = f'''SELECT s.id,s.title,s.price,s.number,s.payNum,s.status,s.createTime,c.name AS 'categoryName',s.img FROM tshop s,tcategory c WHERE s.adminId = {adminId} AND cId = c.id'''
    result = dbutil.select(db, sql)
    db.close()

    shops = []
    if result:
        for re in result:
            shop = Shop(re[0], re[1], re[2], re[3], re[4], re[5], re[6],re[7],img=re[8])
            shops.append(shop.toDict())
    return shops

'''
创建商品
'''
def create(shop:Shop,adminId:int,cId):
    db = dbutil.openDb()
    sql = f'''INSERT INTO tshop (title,price,number,status,createTime,adminId,cId,img) VALUES('{shop.title}',{shop.price},{shop.number},'1',NOW(),{adminId},{cId},'{shop.img}')'''
    id = dbutil.insert(db, sql)
    db.close()
    return id

'''
删除一件商品
'''
def delete(adminId,id):
    try:
        db = dbutil.openDb()
        sql = f'''DELETE FROM tshop WHERE id = {id} AND adminid = {adminId}'''
        dbutil.delete(db, sql)
        db.close()
    except BaseException as e:
        print(e)
        return 0
    else:
        return 1

'''
修改商品指定字段
'''
def update(adminId,id,field,value):
    try:
        db = dbutil.openDb()
        sql = f'''UPDATE tshop SET {field} = '{value}' WHERE id = {id} AND adminid = {adminId}'''
        dbutil.delete(db, sql)
        db.close()
    except BaseException as e:
        print(e)
        return 0
    else:
        return 1

'''
修改商品指定字段
'''
def updateShop(adminId,id,shopTitle,shopPrice,number,img):
    db = dbutil.openDb()
    sql = f'''UPDATE tshop SET title = '{shopTitle}',price = {shopPrice},number = {number},img = '{img}' WHERE id = {id} AND adminid = {adminId}'''
    count = dbutil.update(db, sql)
    db.close()
    return count

# 模糊查询商品
def findShopByLikeTitle(adminId,title):
    db = dbutil.openDb()
    sql = f'''SELECT s.id,s.title,s.price,s.number,s.payNum,s.status,s.createTime,c.name AS 'categoryName',s.img FROM tshop s,tcategory c WHERE adminid = {adminId} AND title LIKE '%{title}%' AND cId = c.id'''
    result = dbutil.select(db,sql)
    db.close()

    shops = []
    if result:
        for re in result:
            shop = Shop(re[0], re[1], re[2], re[3], re[4], re[5], re[6], re[7], img=re[8])
            shops.append(shop.toDict())
    return shops

# 通过日期查询商品
def findShopByDate(adminId,startDate,endDate):
    db = dbutil.openDb()
    sql = f'''SELECT s.id,s.title,s.price,s.number,s.payNum,s.status,s.createTime,c.name AS 'categoryName',s.img FROM tshop s,tcategory c WHERE adminid = {adminId} AND createTime BETWEEN '{startDate}' AND DATE('{endDate}')+1 AND cId = c.id'''
    result = dbutil.select(db,sql)
    db.close()

    shops = []
    if result:
        for re in result:
            shop = Shop(re[0], re[1], re[2], re[3], re[4], re[5], re[6], re[7], img=re[8])
            shops.append(shop.toDict())
    return shops

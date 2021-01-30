from code.tools import dbutil


class Order:

    def __init__(self,orderNumber,createTime,shopTitle,price,shopId,userId,id,endPrice,orderId):
        self.orderNumber = orderNumber
        self.createTime = createTime
        self.shopTitle = shopTitle
        self.price = price
        self.shopId = shopId
        self.userId = userId
        self.id = id
        self.endPrice = endPrice
        self.orderId = orderId

    @classmethod
    # 元组转order对象
    def otup(self,tup):
        return Order(tup[0], str(tup[1]), tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])

    @staticmethod
    # 返回查询语句 由于大部分查询语句一样，所以使用公共sql语句，次语句以上面otup语句有关联，改此语句需要和otup函数一起改
    def getSelectSql(uos:str):
        sql = f'''SELECT o.number,o.createtime,s.title,s.price,t.sid AS 'SId',t.uid AS 'UId',o.id AS 'OId',o.price AS endPrice,o.orderId FROM 
                {uos} t,
                torder o,
                tshop s
                WHERE o.id = t.oid AND s.id = t.sid'''
        return sql

    @staticmethod
    # 多个元组转order列表
    def otup_list(tuplist):
        arr = []
        for d in tuplist:
            arr.append(Order.otup(d).toDict())
        return arr

    def __str__(self) -> str:
        json = self.toDict()
        return str(json)

    def toDict(self) -> dict:
        json = {}
        json['orderNumber'] = self.orderNumber
        json['createTime'] = self.createTime
        json['shopTitle'] = self.shopTitle
        json['price'] = str(self.price)
        json['shopId'] = self.shopId
        json['userId'] = self.userId
        json['id'] = self.id
        json['endPrice'] = str(self.endPrice)
        json['orderId'] = str(self.orderId)
        return json









'''
    查询所有订单
'''
def selectAll():
    db = dbutil.openDb()

    sql = Order.getSelectSql('uos')
    orders = dbutil.select(db, sql)
    db.close()

    return Order.otup_list(orders)

'''
    通过订单id查询 返回order信息 None表示没有找到
'''
def selectById(id):
    db = dbutil.openDb()

    sql = Order.getSelectSql(f'(SELECT uid,oid,sid FROM uos WHERE oid = {id})')
    order = dbutil.select(db, sql)
    db.close()
    if order:
        return Order.otup(order[0])

'''
    通过userid查询订单列表
'''
def selectListByUserId(userid):
    db = dbutil.openDb()

    sql = Order.getSelectSql(f'(SELECT uid,oid,sid FROM uos WHERE uid = {userid})')
    orders = dbutil.select(db, sql)
    db.close()
    return Order.otup_list(orders)

'''
创建（购买）订单
    :param num 购买数据
    :param shopId 购买的商品
    :param userId 购买的用户
'''
def createOrder(num,shopId,userId):
    db = dbutil.openDb()
    oId = 0
    try:
        price = dbutil.select(db, f'SELECT price FROM tshop WHERE id = {shopId}')
        if price: # 找到商品
            sql1 = f'''INSERT INTO torder (orderId,number,price,createtime) VALUES(
                        CONCAT(DATE_FORMAT(NOW(),'%Y%m%d%H%i%S'),FLOOR(RAND() * 10000)),
                        {num},{price[0][0]*num}, NOW())'''
            oId = dbutil.insert(db, sql1)
            if oId:
                sql2 = '''UPDATE tshop SET paynum = paynum + %s WHERE id = %s''' % (num, shopId)
                sql3 = '''INSERT INTO uos(uid,oid,sid) VALUES(%s,%s,%s)'''
                dbutil.insert(db, sql2)
                dbutil.insert(db, sql3 % (userId, oId, shopId))

    except:
        oId = 0
    finally:
        db.close()
    return oId

'''
通过卖家id查找订单
'''
def selectByAdminId(userId):
    db = dbutil.openDb()
    orders = []
    try:
        sql = Order.getSelectSql(f'(SELECT * FROM uos WHERE sid IN(SELECT id FROM tshop WHERE adminId = {userId}))')
        orders = dbutil.select(db, sql)
    except BaseException as e:
        print('selectByAdminId',e)
    db.close()
    return Order.otup_list(orders)

'''
通过卖家id查找已售商品(模糊查询orderId)
'''
def findByLikeOrderId(userId,orderId):
    db = dbutil.openDb()
    orders = []
    try:
        sql = Order.getSelectSql(f'''(SELECT * FROM uos WHERE oid IN(SELECT id FROM torder WHERE orderId LIKE '%{orderId}%'))''') +f' AND s.adminId = {userId}'
        orders = dbutil.select(db, sql)
    except BaseException as e:
        print('findByLikeOrderId',e)
    db.close()
    return Order.otup_list(orders)

'''
通过卖家id查找已售商品(模糊查询shopTitle)
'''
def findByLikeTittle(userId,shopTitle):
    db = dbutil.openDb()
    orders = []
    try:
        sql = Order.getSelectSql(f'''(SELECT * FROM uos WHERE sid IN(SELECT id FROM tshop WHERE adminId = {userId} AND title LIKE '%{shopTitle}%'))''')
        orders = dbutil.select(db, sql)
    except BaseException as e:
        print('findByLikeOrderId',e)
    db.close()
    return Order.otup_list(orders)


'''
通过卖家id查找指定日期范围已售商品
'''
def findByDate(userId,startDate,endDate):
    db = dbutil.openDb()
    orders = []
    try:
        sql = Order.getSelectSql(f'''(SELECT uid,oid,sid FROM uos WHERE sid IN(SELECT id FROM tshop WHERE adminid = {userId}))''') + \
              f''' AND o.createTime BETWEEN DATE_FORMAT({startDate},'%y-%m-%d') AND DATE_FORMAT({endDate},'%y-%m-%d')'''
        orders = dbutil.select(db, sql)
    except BaseException as e:
        print('findByLikeOrderId',e)
    db.close()
    return Order.otup_list(orders)


'''
通过卖家id查找近排的一天已售商品
    :param int day 0 今天 1 昨天 。。。以此类推
'''
def findByDay(userId,day:int):
    db = dbutil.openDb()
    orders = []
    try:
        sql = Order.getSelectSql(f'''(SELECT uid,oid,sid FROM uos WHERE sid IN(SELECT id FROM tshop WHERE adminid = {userId}))''') + \
              f''' AND DATE_FORMAT(o.createTime,'%y-%m-%d') = DATE_FORMAT(DATE(NOW())-{day},'%y-%m-%d')'''
        orders = dbutil.select(db, sql)
    except BaseException as e:
        print('findByLikeOrderId',e)
    db.close()
    return Order.otup_list(orders)

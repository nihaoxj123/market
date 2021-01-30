from flask import Blueprint,render_template,session,request
from code.dbtable import shop as sDb
import json

shop = Blueprint('shop',__name__,template_folder='../templates/shop')

@shop.route('/')
def shopPage():
    return render_template('/shop/shopList.html')

@shop.route('/getShopList',methods=['post'])
def getShopList():
    shops = sDb.selectAll()
    return json.dumps({'code':1,'message':'成功','data':shops})

# 添加商品
@shop.route('/addShop',methods=['post'])
def addShop():
    if 'userId' in session:
        userId = session['userId']
        if userId:
            title = request.form.get('shopTitle')
            price = request.form.get('shopPrice')
            number = request.form.get('number')
            img = request.form.get('shopImg')
            cId = request.form.get('cId')
            try:
                if img and int(number) > 0 and float(price) > 0:
                    s = sDb.Shop.newShop(title, price, number,img)
                    id = sDb.create(s, userId,cId)
                    if id:
                        return json.dumps({'code': 1, 'message': '添加成功', 'data': None})
            except BaseException:
                pass
            return json.dumps({'code': 0, 'message': '价钱和数量必须大于0并且图片不能为空', 'data': None})
    return json.dumps({'code': -1, 'message': '请先登录', 'data': None})

# 修改商品数据
@shop.route('/updateShopStatus',methods=['post'])
def updateShopStatus():
    if 'userId' in session:
        userId = session['userId']
        id = request.form.get('shopId')
        type = request.form.get('type')
        if userId and id:
            count = 0
            if type == '1':
                count = sDb.delete(userId,id)
            elif type == '2':
                count = sDb.update(userId,id,'status','1')
            elif type == '3':
                count = sDb.update(userId,id,'status','2')
            elif type == '4':
                shopTitle = request.form.get('shopTitle')
                shopPrice = request.form.get('shopPrice')
                number = request.form.get('number')
                img = request.form.get('img')
                count = sDb.updateShop(userId,id,shopTitle,shopPrice,number,img)
            if count:
                return json.dumps({'code':1,'message':'成功','data':None})
        return json.dumps({'code':0,'message':'失败','data':None})
    return json.dumps({'code':-1,'message':'请登录','data':None})
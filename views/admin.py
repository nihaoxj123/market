from flask import Blueprint,render_template,session,redirect,request
from code.dbtable import user
from code.dbtable import order
from code.dbtable import shop
from code.dbtable import category

import json

# template_folder 映射html页面
admin = Blueprint('admin',__name__,template_folder='../templates/admin')

# 商城管理首页
@admin.route('/')
def adminPage():
    if 'userId' in session:
        userId = session['userId']
        u = user.selectUserById(userId)
        if u :
            if u.adminType == '1':
                return render_template('admin.html',nickName=u.nickName)
            else:
                return render_template('requestMerchant.html',msg='您当前不是卖家，请申请')
    return redirect('/user/loginPage')

@admin.route('/requestMerchant',methods=['post'])
def requestMerchant():
    if 'userId' in session:
        userId = session['userId']
        if userId:
            count = user.updateAdminType(userId)
            if count:
                return json.dumps({'code':1,'message':'成功'})
            return json.dumps({'code': 0, 'message': '失败'})
    return redirect('/user/loginPage')

# 已售订单页面
@admin.route('/salesOrderPage')
def salesOrderPage():
    return render_template('salesOrder.html')

# 获取已售订单数据
@admin.route('/getPayOrderList',methods=['post'])
def getPayOrderList():
    if 'userId' in session:
        userId = session['userId']
        if userId:
            '''
            # type:1,orderId
            # type:2,likeTitle
            # type:3,startDate,endDate
            # type:4 今天
            # type:5 昨天
            # type:6 近7天
            # type:7 近30天
            '''
            type = request.form.get('type')
            if type == '1':
                orderId = request.form.get('orderId')
                orders = order.findByLikeOrderId(userId,orderId)
            elif type == '2':
                likeTitle = request.form.get('likeTitle')
                orders = order.findByLikeTittle(userId, likeTitle)
            elif type == '3':
                startDate,endDate = request.form.get('startDate'),request.form.get('endDate')
                orders = order.findByDate(userId,"'%s'"%startDate,"DATE('%s') + 1"%endDate)
            elif type == '4':
                orders = order.findByDay(userId,0)
            elif type == '5':
                orders = order.findByDay(userId,1)
            elif type == '6':
                orders = order.findByDate(userId,"DATE(NOW()) - 7","DATE(NOW())+1")
            elif type == '7':
                orders = order.findByDate(userId,"DATE(NOW()) - 30","DATE(NOW())+1")
            else:
                orders = order.selectByAdminId(userId)
            return json.dumps({'code': 1, 'message': '成功', 'data': orders})
    return json.dumps({'code': 0, 'message': '请先登录', 'data': None})

# 在售商品页面
@admin.route('/salesShopPage')
def salesShopPage():
    return render_template('salesShop.html')

# 获取在售商品数据
@admin.route('/getMyShops',methods=['post'])
def getMyShops():
    if 'userId' in session:
        userId = session['userId']
        if userId:
            type = request.form.get('type')
            if type == '1':
                likeTitle = request.form.get('likeTitle')
                shops = shop.findShopByLikeTitle(userId,likeTitle)
            elif type == '2':
                startDate = request.form.get('startDate')
                endDate = request.form.get('endDate')
                shops = shop.findShopByDate(userId,startDate,endDate)
            else:
                shops = shop.selectByAdminId(userId)
            return json.dumps({'code': 1, 'message': '成功', 'data': shops})
    return json.dumps({'code': 0, 'message': '请先登录', 'data': None})


@admin.route('/getCategoryList',methods=['post'])
def getCategoryList():
    try:
        data = category.selectAll()
        return json.dumps({'code': 1, 'message': '成功', 'data': data})
    except BaseException:
        pass
    return json.dumps({'code': 0, 'message': '成功', 'data': None})


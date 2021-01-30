from code.dbtable import shop
from code.dbtable import order


from flask import Flask,render_template,request,redirect,session
import json

app = Flask(__name__)
# 使用session需要设置秘密
app.secret_key = '!@#$%^&*()11'

# 导入蓝图
from views.admin import admin
from views.user import user
from views.shop import shop
# 配置蓝图 映射路径 /admin
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user,url_prefix='/user')
app.register_blueprint(shop,url_prefix='/shop')


@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/payShop',methods=['post'])
def payShop():
    try:
        num = int(request.form.get('payNum'))
        shopId = request.form.get('shopId')
        userId = session.get('userId')
        if userId:
            if num > 0:
                oid = order.createOrder(num, shopId, userId)
                if oid:
                    return json.dumps({'code': 1, 'message': '购买成功', 'data': None})
                else:
                    return json.dumps({'code': 0, 'message': '购买失败', 'data': None})
            else:
                return json.dumps({'code': 0, 'message': '购买商品不能小于1', 'data': None})
        else:
            return json.dumps({'code': 2, 'message': '请先登录', 'data': None})
    except BaseException as e:
        return json.dumps({'code': -1, 'message': '非法操作', 'data': None})

@app.route('/orderList')
def userOrderList():
    if 'userId' in session:
        userId = session['userId']
        if userId:
            orders = order.selectListByUserId(userId)
            return render_template('/orderList.html', orders=enumerate(orders), length=len(orders))
    return redirect('/')



@app.route('/deleteShop',methods=['post'])
def deleteShop():
    id = request.form.get('shopId')
    if shop.delete(id):
        return json.dumps({'code': 1, 'message': '删除成功', 'data': None})
    return json.dumps({'code': 0, 'message': '删除失败', 'data': None})



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=False)





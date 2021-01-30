from flask import Blueprint,render_template,request,session,redirect
from code.dbtable import user as uDb
import json

user = Blueprint('user',__name__,template_folder='../templates/user')

# 登录页面
@user.route('/loginPage')
def loginPage():
    return render_template('/login.html')

# 注册页面
@user.route('/registerPage')
def registerPage():
    return render_template('/register.html')

# 注册请求
@user.route('/register',methods=['post'])
def register():
    nickName = request.form.get('nickName')
    password = request.form.get('password')
    print(nickName,password)
    if nickName and password:
        id = uDb.create(uDb.User.newUser(nickName,password))
        if id:
            u = uDb.selectUserById(id)
            if u:
                return json.dumps({'code':1,'message':'这是您的会员账号（%s），请牢记。'%u.userCode})
    return json.dumps({'code':1,'message':'注册失败，请重新注册'})

# 请求登录
@user.route('/login',methods=['post'])
def login():
    usercdoe = request.form.get('usercode')
    password = request.form.get('password')

    u = uDb.selectUserByCode(usercdoe)
    if u and u.password == password:
        session['userId'] = u.id
        return redirect('/shop')
    else:
        return render_template('/login.html', title='会员登录', msg='账号或密码错误')

# 退出登录
@user.route('/loginout')
def loginout():
    if 'userId' in session:
        del session['userId']
    return redirect('/user/loginPage')
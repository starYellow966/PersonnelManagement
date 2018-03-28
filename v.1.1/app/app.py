# -*- coding: utf-8 -*-
#上面注释是为了告诉Python解释器，按照UTF-8编码读取源代码
import sys 
reload(sys);
sys.setdefaultencoding("utf-8");

from flask import Flask,render_template,Blueprint,request,flash,redirect,url_for
# from flask_httpauth import HTTPBasicAuth
import flask_excel as excel #excel操作工具包
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from flask_bootstrap import Bootstrap

from controller import organizationBlueprint,dictionaryBlueprint,logBlueprint
from models import organization,dictionary,users,redirectForm

app = Flask(__name__)
# auth = HTTPBasicAuth()
app.config['SECRET_KEY'] = 'i do not know how to use this one'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesignV1_1?charset=utf8';
# db = SQLAlchemy(app)

# LoginManager对象让程序和Flask_login一起工作
login_manager = LoginManager();


'''人事管理首页

:return : index.html
:date : 2018/3/13
'''
@app.route('/')
def index():
    return render_template('index.html');

@app.route('/login', methods = ['GET','POST'])
def login():
    form = users.Login_Form();
    if form.validate_on_submit():
        user = users.User.query.filter_by(name = form.name.data).first();
        if (user is not None and user.password == form.pwd.data):
            # remember 防止用户意外被退出由于浏览器的session意外被删掉
            # 与@fresh_login_required 连用
            # login_user(user, remember = form.remember_me.data);
            login_user(user)
            flash(u'登录成功');
            next = request.args.get('next');
            # is_safe_url should check if the url is safe for redirects.
            if not redirectForm.is_safe_url(next):
                return flask.abort(400);
            return redirectForm.redirect(url_for('index'));
            # return redirect(url_for('index'));
        else:
            flash(u'用户或密码错误');
            return render_template('login.html', form = form);
    return render_template('login.html', form = form);


@app.route('/logout')
@login_required
def logout():
    logout_user() #They will be logged out, and any cookies for their session will be cleaned up.
    flash(u'你已退出登录')
    return redirect(url_for('index'))


'''This sets the callback for reloading a user from the session
即当登陆成功后，该函数会自动从会话中存储的用户 ID 重新加载User对象
除了发送ajax这种异步请求外，发送http请求均会调用该函数

:param['user_id'] :　{unicode} 存储在会话中的用户ID
:return : User对象或者None(当user_id无效时)
'''
@login_manager.user_loader
def load_user(user_id):
    return users.User.query.get(int(user_id));

def initLoginManager():
    login_manager.session_protection = "strong"
    '''
    指当访问需要登录的页面时（即@login_requested修饰的页面时），如果没有登录则跳转到login_view指定的页面
    若login_view没有指定则抛出401错误

    也可以用@login_manager.unauthorized_handler 来实现相同功能，但url没有next参数
    '''
    login_manager.login_view = "login"
    # #伴随跳转到login页面时发送的消息，原理是flask.flash()
    login_manager.login_message = u"Please log in to access this page" 
    login_manager.login_message_category = "info"
    login_manager.refresh_view = "login"
    login_manager.needs_refresh_message = u"To protect your account, please reauthenticate to access this page."
    login_manager.needs_refresh_message_category = "info"

def initBlueprint():
    # 注册蓝图
    app.register_blueprint(organizationBlueprint)
    app.register_blueprint(dictionaryBlueprint)
    app.register_blueprint(logBlueprint)

if __name__ == '__main__':
    initLoginManager()
    initBlueprint()
    login_manager.init_app(app);
    excel.init_excel(app); # required since version 0.0.7
    # Bootstrap(app)
    # app.config.setdefault('BOOTSTRAP_SERVE_LOCAL', True)
    # app.config.setdefault('BOOTSTRAP_QUERYSTRING_REVVING', False)
    app.run(debug = True);
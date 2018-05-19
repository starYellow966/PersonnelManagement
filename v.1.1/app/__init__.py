# -*- coding: utf-8 -*-
import os
from flask import Flask,render_template,Blueprint,request,flash,redirect,url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
import flask_excel as excel
from extensions import db, login_manager, bootstrap, photos

from modelss import User,General_Log
from forms import Login_Form
from config import config
from controller import organizationBlueprint,dictionaryBlueprint,logBlueprint,employeeBlueprint,statisticsBlueprint
from models import redirectForm



# bootstrap = Bootstrap()
# db = SQLAlchemy()
# photos = UploadSet('photos', IMAGES)
# login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'i do not know how to use this one'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hx:huangxin123456@120.79.147.151/gdesignV1_1?charset=utf8';
    app.config['UPLOADED_PHOTOS_DEST'] = 'E://photos'
    # app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()
    # bootstrap.init_app(app)
    db.init_app(app)
    configure_uploads(app, photos)
    login_manager.init_app(app)
    excel.init_excel(app)

    init_blueprint(app)
    init_loginManager()
    init_route(app)
    # init_errorhandler(app)

    return app

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # bootstrap.init_app(app)
    db.init_app(app)
    configure_uploads(app, photos)
    login_manager.init_app(app)
    excel.init_excel(app)

    init_blueprint(app)
    init_loginManager()
    init_route(app)
    # init_errorhandler(app)

    return app

def init_loginManager():
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

    @login_manager.user_loader
    def load_user(user_id):
        '''This sets the callback for reloading a user from the session
        即当登陆成功后，该函数会自动从会话中存储的用户 ID 重新加载User对象
        除了发送ajax这种异步请求外，发送http请求均会调用该函数
        
        Decorators:
            login_manager.user_loader
        
        Arguments:
            user_id {unicode} -- 存储在会话中的用户ID
        
        Returns:
            [User] --  User对象或者None(当user_id无效时)
        '''
        cur_user = None
        try:
            cur_user = User.query.get(int(user_id))
            return cur_user
        except Exception as e:
            db.session.rollback()
            raise e

            

def init_blueprint(app):
    '''注册蓝图
    '''
    app.register_blueprint(organizationBlueprint, url_prefix = '/org')
    app.register_blueprint(dictionaryBlueprint, url_prefix = '/dict')
    app.register_blueprint(logBlueprint, url_prefix = '/log')
    app.register_blueprint(employeeBlueprint, url_prefix = '/employee')
    app.register_blueprint(statisticsBlueprint, url_prefix = '/statistics')

def init_route(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods = ['GET','POST'])
    def login():
        form = Login_Form()
        try:
            if form.validate_on_submit():
                user = User.query.filter_by(name = form.name.data).first()
                if (user is not None and user.check_password(form.pwd.data)):
                    login_user(user)
                    # 日志记录
                    log = General_Log('用户'+ current_user.name + "登录系统",current_user.name,request.remote_addr)
                    db.session.add(log)
                    db.session.commit()
                    next = request.args.get('next')
                    # is_safe_url should check if the url is safe for redirects.
                    if not redirectForm.is_safe_url(next):
                        return flask.abort(400)
                    return redirectForm.redirect(url_for('index'))
                else:
                    flash(u'密码错误')
            else:
                #因为validate_on_submit()在页面加载完成后就会返回一个false
                if (form.name.data != None and len(form.name.data) > 0):
                    flash(u'用户不存在')
        except Exception as e:
            flash(u'未知错误')
            db.session.rollback()
            raise e
        return render_template('login.html', form = form)


    @app.route('/logout')
    @login_required
    def logout():
        
        try:
            # 日志记录
            log = General_Log('用户'+ current_user.name + "退出系统",current_user.name,request.remote_addr)
            db.session.add(log)
            db.session.commit()
            logout_user() #They will be logged out, and any cookies for their session will be cleaned up.
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            raise e


def init_errorhandler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'),404

    @app.errorhandler(500)
    def interal_server_error(e):
        return render_template('500.html'),500
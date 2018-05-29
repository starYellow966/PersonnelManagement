# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import  Required, ValidationError
from flask_wtf import FlaskForm
from modelss import User

class Login_Form(FlaskForm):
    name = StringField(u'用户名',validators=[Required(message=u'用户名不能为空')])
    pwd = PasswordField(u'密码',validators=[Required(message=u'密码不能为空')])
    # remember_me = BooleanField('Remember_me', default = False)
    submit=SubmitField(u'登录')

    def validate_name(self, field):
        # print 'validate_name'
        name = field.data
        user = User.query.filter_by(name = name).count()
        if user == 0 :
            raise ValidationError(u"此用户不存在")



from urlparse import urlparse, urljoin
from flask import request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import TextField, HiddenField

'''
A common pattern with form processing is to automatically redirect back to the user. 
There are usually two ways this is done: by inspecting a next URL parameter or by looking at the HTTP referrer.
Unfortunately you also have to make sure that users are not redirected to malicious attacker's pages and just to the same host. 
If you are using Flask-WTF there is a nicer way
'''
class RedirectForm(FlaskForm):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

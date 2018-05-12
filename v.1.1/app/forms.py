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
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class commitForm(FlaskForm):
    car_number= StringField(validators=[DataRequired(message="车牌号不能为空"), Length(
        7, 7, message='格式错误')])
    supplier = StringField(validators=[DataRequired(message="供应商不能为空"), Length(
        6, 20, message='长度位于6~20之间')])
    submit = SubmitField('提交')
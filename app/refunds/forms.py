from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired

class CreateRefundForm(FlaskForm):
    reason = TextAreaField('Reason', validators=[InputRequired()])
    order_uuid = StringField('Order UUID', validators=[InputRequired()])
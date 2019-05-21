from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms import validators
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    confirm = SubmitField('Confirm')
    total = IntegerField('Total', validators=[DataRequired(),
                                              validators.number_range(min=1,
                                                                      max=30)
                                              ])
    start_time = DateField("StartTime", validators=[DataRequired()])
    description = StringField("Description")
    end_time = DateField("EndTime", validators=[DataRequired()])
    ticket_price = IntegerField("TicketPrice")
    address = StringField('Address')
    location = StringField('Location', validators=[DataRequired()])
    img_url = StringField('Image', validators=[DataRequired()])
    details = StringField('Details')

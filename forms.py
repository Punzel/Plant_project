from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.fields import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

     
class add_plant_form(FlaskForm):
    name = TextField('Plantname')
    german_name = TextField('German Name')
    latin_name = TextField('Latin Plantname', validators=[DataRequired()])
    plant_information = TextField('Plant Information')
    light = TextField('light')
    watering = TextField('watering')
    placement = TextField('placement')
    insect_friendly = TextField('insect friendly')
    other_information = TextField('other information')
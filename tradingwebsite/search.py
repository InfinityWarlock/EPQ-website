from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
import postcodes_io_api

api = postcodes_io_api.Api(debug_http=True)

def postcode_check(form, field):
    postcode = field.data.replace(" ", "").upper()
    valid = api.is_postcode_valid(postcode)
    if valid == False:
        raise ValidationError('Invalid Postcode')

class SearchForm(FlaskForm):
    query = StringField("Search")
    sort = SelectField("Sort Posts by: ", choices = [("t", "Date added (Newest First)"), ("p", "Price (Low to High)"), ("d", "Distance (Nearest First)")])
    postcode = StringField('Your Postcode', validators = [DataRequired(), postcode_check])
    max_distance = SelectField("Max Distance", choices = [(None, "Nationwide"), (100, "100 miles"), (50, "50 miles"), (30, "30 miles"), (15, "15 miles"), (10, "10 miles"), (5, "5 miles")])
    condition = SelectMultipleField('Condition of Item', validators = [DataRequired()], choices = [(i, i) for i in ["New", "Good", "Slightly Faulty", "Not working at all"]])
    submit = SubmitField("Search")

class CPUSearch(SearchForm):
    brand = SelectMultipleField('CPU Brand', choices = [(i, i) for i in ["Intel", "AMD"]])

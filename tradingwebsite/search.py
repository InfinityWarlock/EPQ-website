from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    query = StringField("Search", validators = [DataRequired, Length(min = 2 max = 50)])
    sort = SelectField("Sort Posts by: ", choices = [("t", "Date added (Newest First)"), ("p", "Price (Low to High)"), ("d", "Distance (Nearest First)")])
    #Add postcode field then max distance field and condition field then part specific fields
    submit = SubmitField("Search")



from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, ValidationError, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, NumberRange, URL, NumberRange
import postcodes_io_api
import re

api = postcodes_io_api.Api(debug_http=True)

def postcode_check(form, field):
    postcode = field.data.replace(" ", "").upper()
    valid = api.is_postcode_valid(postcode)
    if valid == False:
        raise ValidationError('Invalid Postcode')

def url_check(form, field):
    text = field.data
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if text:
        if re.match(regex, text) is None:
            raise ValidationError('Invalid URL')

class PostCreationForm(FlaskForm):
    title = StringField('Post Title', validators = [DataRequired(), Length(min = 3, max = 50)])
    price = FloatField('Price (£)', validators = [DataRequired(), NumberRange(min = 0)])
    # need to add price (and price reccomendation)
    email = StringField('Contact Email', validators = [DataRequired(), Email()])
    description = TextAreaField('Item Description', validators = [DataRequired(), Length(min = 3, max = 300)])
    condition = SelectField('Condition of Item', validators = [DataRequired()], choices = [(i, i) for i in ["New", "Good", "Slightly Faulty", "Not working at all"]])
    location = StringField('Your Postcode', validators = [DataRequired(), postcode_check])
    picture = StringField('Image Address of a picture of the item (upload to a service like google photos then copy the image address)', validators = [url_check]) #couldnt find an easy way to store files on mongodb so changed the image to image address
    submit = SubmitField('Post')

class ItemForm(FlaskForm):
    item = SelectField('Item', coerce = int)
    submit = SubmitField('Next')
from tradingwebsite import db
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

def get_choices(category, filter_type):
    components = db.components
    component_dict = components.find_one()
    posts = db.posts
    post_list = posts.find()
    options = []
    items = component_dict[category]
    post_ids = [post["item"] for post in post_list]
    for item in items:
        if (option := item[filter_type]) not in options and item["id"] in post_ids:
            options.append(option)
    return options

class SearchForm(FlaskForm):
    query = StringField("Search")
    sort = SelectField("Sort Posts by: ", choices = [("t", "Date added (Newest First)"), ("p", "Price (Low to High)"), ("d", "Distance (Nearest First)")])
    postcode = StringField('Your Postcode', validators = [DataRequired(), postcode_check])
    max_distance = SelectField("Max Distance", choices = [(200, "Nationwide"), (100, "100 miles"), (50, "50 miles"), (30, "30 miles"), (15, "15 miles"), (10, "10 miles"), (5, "5 miles")], coerce = int)
    condition = SelectMultipleField('Condition of Item', choices = [(i, i) for i in ["New", "Good", "Slightly Faulty", "Not working at all"]])
    

class CPUSearch(SearchForm):
    brand = SelectMultipleField('CPU Brand', choices = [(i, i) for i in get_choices("cpus", "brand")])
    submit = SubmitField("Search")

class GPUSearch(SearchForm):
    brand = SelectMultipleField('Graphics Card Brand', choices = [(i, i) for i in get_choices("gpus", "brand")])
    submit = SubmitField("Search")

class RAMSearch(SearchForm):
    module_type = SelectMultipleField('Module type', choices = [(i, i) for i in get_choices("ram", "type")])
    speed = SelectMultipleField('Clock Speed', choices = [(i, i) for i in get_choices("ram", "speed")])
    size = SelectMultipleField('Size', choices = [(i, i) for i in get_choices("ram", "size")])
    form_factor = SelectMultipleField('Form Factor', choices = [(i, i) for i in get_choices("ram", "form factor")])
    submit = SubmitField("Search")

class StorageSearch(SearchForm):
    storage_type = SelectMultipleField('Module type', choices = [(i, i) for i in get_choices("storage", "type")])
    rpm = SelectMultipleField('RPM', choices = [(i, i) for i in get_choices("storage", "rpm")])
    size = SelectMultipleField('Size', choices = [(i, i) for i in get_choices("storage", "size")])
    form_factor = SelectMultipleField('Form Factor', choices = [(i, i) for i in get_choices("storage", "form factor")])
    interface = SelectMultipleField('Interface', choices = [(i, i) for i in get_choices("storage", "interface")])
    submit = SubmitField("Search")

class PSUSearch(SearchForm):
    efficiency = SelectMultipleField('Efficiency', choices = [(i, i) for i in get_choices("psus", "efficiency")])
    wattage = SelectMultipleField('Wattage', choices = [(i, i) for i in get_choices("psus", "wattage")])
    modular = SelectMultipleField('Modular', choices = [(i, i) for i in get_choices("psus", "modular")])
    form_factor = SelectMultipleField('Form Factor', choices = [(i, i) for i in get_choices("psus", "form factor")])
    submit = SubmitField("Search")

class OtherSearch(SearchForm):
    submit = SubmitField("Search")
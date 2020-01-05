import pymongo
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SelectField, SubmitField

db_connection_string = "mongodb+srv://CatnipMasterRace:XuUrP6Ui5EErAcro@epq-trading-site-q3dcn.gcp.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(db_connection_string)
db = client.epq_trading_site
components = db.components
component_dict = components.find_one()

class CategoryForm(FlaskForm):
    category = SelectField('Component Type',
        choices = [(i, i) for i in ["Other", "CPU", "Motherboard", "Memory", "Storage", 
            "Graphics Card", "Power Supply", "Case"]])
    submit = SubmitField("Next")

class CPUForm(FlaskForm):
    brand = SelectField('CPU Brand', choices = [(i, i) for i in ["Intel", "AMD"]])
    query = StringField("Search")
    submit = SubmitField("Next")

class GPUForm(FlaskForm):
    brand = SelectField('GPU Brand', choices = [(i, i) for i in ["ATI/AMD", "Nvidia"]])
    query = StringField("Search")
    submit = SubmitField("Next")

def get_options(part_type, filter_type):
    options = []
    items = component_dict[part_type]
    for item in items:
        if item[filter_type] not in options:
            options.append(item[filter_type])
    return options

class PSUForm(FlaskForm):
    efficiency = SelectField('Efficiency', choices = [(i, i) for i in get_options("psus", "efficiency")])
    form_factor = SelectField('Form Factor', choices = [(i, i) for i in get_options("psus", "form factor")])
    wattage = SelectField('Wattage', choices = [(i, i) for i in get_options("psus", "wattage")])
    modular = SelectField('Modular', choices = [(i, i) for i in get_options("psus", "modular")])
    submit = SubmitField("Next")
    

class RAMForm(FlaskForm):
    module_type = SelectField('Module type', choices = [(i, i) for i in get_options("ram", "type")])
    speed = SelectField('Clock Speed', choices = [(i, i) for i in get_options("ram", "speed")])
    size = SelectField('Size', choices = [(i, i) for i in get_options("ram", "size")])
    form_factor = SelectField('Form Factor', choices = [(i, i) for i in ["Desktop", "Laptop"]])
    submit = SubmitField("Next")

def get_rpm_options():
    options = get_options("storage", "rpm")
    index = options.index("None")
    options[index] = "SSD"
    return options

class StorageForm(FlaskForm):
    size = SelectField("Size", choices = [(i, i) for i in get_options("storage", "size")])
    drive_type = SelectField("Drive Type", choices = [(i, i) for i in get_options("storage", "type")])
    form_factor = SelectField("Form Factor", choices = [(i, i) for i in get_options("storage", "form factor")])
    interface = SelectField("Interface", choices = [(i, i) for i in get_options("storage", "interface")])
    rpm = SelectField("RPM", choices = [(i, i) for i in get_rpm_options()])
    submit = SubmitField("Next")

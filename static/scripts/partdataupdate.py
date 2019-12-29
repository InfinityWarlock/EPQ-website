#This is a script to update the components collection of the database
import pymongo
from pcpartpicker import API as pcppAPI #package with code that scrapes the pcpartpicker website for data about components
from pprint import pprint

db_connection_string = "mongodb+srv://CatnipMasterRace:XuUrP6Ui5EErAcro@epq-trading-site-q3dcn.gcp.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(db_connection_string)
db = client.epq_trading_site

api = pcppAPI("uk")

part_id = 0 #every part will have a unique id so posts can be classified by what component they are selling by giving the post the same id

print(api.retrieve("cpu")["cpu"][500])
#different component classes are structured differently so i need a unique function for each component type
def get_cpus():
    global part_id #this global variable needs to be modified inside the local scope of a function
    cpu_data = api.retrieve("cpu")["cpu"]
    cpus = []
    for cpu in cpu_data:
        brand = cpu.brand
        model = cpu.model
        name = brand + " " + model
        cpu_dict = {"name": name, "brand": brand, "model": model, "id": part_id}
        part_id += 1 #increased for each part
        cpus.append(cpu_dict)
    return cpus

cpus = get_cpus()
pprint(cpus)
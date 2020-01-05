#This is a script to update the components collection of the database
import pymongo
from pcpartpicker import API as pcppAPI #package with code that scrapes the pcpartpicker website for data about components
from pprint import pprint

db_connection_string = "mongodb+srv://CatnipMasterRace:XuUrP6Ui5EErAcro@epq-trading-site-q3dcn.gcp.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(db_connection_string)
db = client.epq_trading_site
components = db.components

api = pcppAPI("uk")

part_id = 0 #every part will have a unique id so posts can be classified by what component they are selling by giving the post the same id

print(api.retrieve("internal-hard-drive")["internal-hard-drive"][1000])
#different component classes are structured differently so i need a unique function for each component type
def get_cpus():
    global part_id #this global variable needs to be modified inside the local scope of a function
    cpu_data = api.retrieve("cpu")["cpu"]
    cpus = []
    for cpu in cpu_data:
        brand = cpu.brand
        model = cpu.model
        name = brand + " " + model
        repeat = False
        for i in cpus:
            if i["name"] == name:
                repeat = True
                break
        if repeat == False:
            cpu_dict = {"name": name, "brand": brand, "model": model, "id": part_id}
            part_id += 1 #increased for each part
            cpus.append(cpu_dict)
    return cpus

def get_videocards():
    global part_id
    gpu_data = api.retrieve("video-card")["video-card"]
    videocards = []
    for gpu in gpu_data:
        chipset = gpu.chipset
        if "TITAN" in chipset or "Titan" in chipset or "Quadro" in chipset or "NVS" in chipset or "GeForce" in chipset:
            brand = "Nvidia"
        else:
            brand = "ATI/AMD"
        name = brand + " " + chipset
        repeat = False
        for i in videocards:
            if i["name"] == name:
                repeat = True
                break
        if repeat == False:
            gpu_dict = {"name": name, "brand": brand, "chipset": chipset, "id": part_id}
            part_id += 1
            videocards.append(gpu_dict)
    return videocards

def get_psus():
    global part_id
    psu_data = api.retrieve("power-supply")["power-supply"]
    psus = []
    for psu in psu_data:
        efficiency = psu.efficiency_rating
        form_factor = psu.form_factor
        wattage = str(psu.wattage) + "W"
        modular = psu.modular
        name = wattage + " " + form_factor + " " + modular + " " + str(efficiency)
        repeat = False
        for i in psus:
            if i["name"] == name:
                repeat = True
                break
        if repeat == False:
            psu_dict = {"name": name, "efficiency": efficiency, "form factor": form_factor, "wattage": wattage, "modular": modular, "id": part_id}
            part_id += 1
            psus.append(psu_dict)
    return psus

def get_ram():
    global part_id
    ram_data = api.retrieve("memory")["memory"]
    ram = []
    for item in ram_data:
        module_type = item.module_type
        speed = str((item.speed.cycles)/1000000) + "MHz"
        size = str(item.number_of_modules) + "x" + str((item.module_size.total)/1000000000) + "GB"
        if "SODIMM" in item.form_factor:
            form_factor = "Laptop"
        else:
            form_factor = "Desktop"
        name = form_factor+module_type+speed+size
        repeat = False
        for i in ram:
            if i["name"] == name:
                repeat = True
                break
        if repeat == False:
            ram_dict = {"name": name, "type": module_type, "speed": speed, "size": size, "form factor": form_factor, "id": part_id}
            part_id += 1
            ram.append(ram_dict)
    return ram

#will add case category but no filters (so no price reccomendation)
#same for motherboards as the API doesnt give me enough info (specifically what chipset the mobo is)

def get_storage():
    global part_id
    storage_data = api.retrieve("internal-hard-drive")["internal-hard-drive"]
    drives = []
    for drive in storage_data:
        size = str((drive.capacity.total)/1000000000)+"GB"
        drive_type = drive.storage_type
        form_factor = drive.form_factor
        interface = drive.interface
        if drive_type != "SSD":
            rpm = str(drive.platter_rpm)+"RPM"
        else:
            rpm = str(None)
        name = size+form_factor+interface+rpm+drive_type
        repeat = False
        for i in drives:
            if i["name"] == name:
                repeat = True
                break
        if repeat == False:
            drive_dict = {"name": name, "size": size, "type": drive_type, "form factor": form_factor, "interface": interface, "rpm": rpm, "id": part_id}
            part_id += 1
            drives.append(drive_dict)
    return drives

def upload_parts():
    global part_id
    cpus = get_cpus()
    motherboards = {"id": part_id}
    part_id += 1
    ram = get_ram()
    storage = get_storage()
    gpus = get_videocards()
    psus = get_psus()
    cases = {"id": part_id}
    part_id += 1
    other = {"id": part_id}
    parts_dict = {"cpus": cpus, "motherboards": motherboards, "ram": ram, "storage": storage, "gpus": gpus, "psus": psus, "cases": cases, "other": other}
    inserted = components.insert_one(parts_dict)
    print(inserted.inserted_id)


upload_parts()
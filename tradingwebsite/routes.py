import flask
import json
from tradingwebsite import app, db
from tradingwebsite.forms import PostCreationForm, ItemForm
from tradingwebsite.database import upload_post, get_posts, get_price_reccomendation, display_posts, get_time_created
from tradingwebsite import filters
from tradingwebsite import search

posts = db.posts
components = db.components
component_dict = components.find_one()

@app.route("/")
@app.route("/home")
def home():
    return flask.render_template("home.html", title = "Home")

@app.route("/about")
def about():
    return flask.render_template("about.html", title = "About")

@app.route("/browse-posts", methods = ['GET', 'POST'])
def browse_posts():
    all_search_form = search.OtherSearch()
    if all_search_form.validate_on_submit():
        query = all_search_form.query
        sort = all_search_form.sort
        postcode = all_search_form.postcode
        max_distance = all_search_form.max_distance
        condition = all_search_form.condition
        filters = json.dumps({"query": query.data, "sort": sort.data, "postcode": postcode.data.replace(" ", "").upper(), "max distance": max_distance.data, "condition": condition.data})
        return flask.redirect(flask.url_for("browse_posts", filters = filters))
    try:
        filters = json.loads(flask.request.args.get('filters', None))
        displayed_posts = display_posts(posts, component_dict, query_param = filters["query"], sort = filters["sort"], postcode = filters["postcode"], max_distance = filters["max distance"], conditions_param = filters["condition"])
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    except:
        displayed_posts = display_posts(posts, component_dict)
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    return flask.render_template("all_posts.html", title = "All Posts", displayed_posts = displayed_posts, all_search_form = all_search_form)

@app.route("/browse-posts/cpus", methods= ['GET', 'POST'])
def cpus():
    cpu_search_form = search.CPUSearch()
    cpu_search_form.brand.choices = [(i, i) for i in search.get_choices("cpus", "brand")]
    if cpu_search_form.validate_on_submit():
        query = cpu_search_form.query
        sort = cpu_search_form.sort
        postcode = cpu_search_form.postcode
        max_distance = cpu_search_form.max_distance
        condition = cpu_search_form.condition
        brand = cpu_search_form.brand
        filters = json.dumps({"query": query.data, "sort": sort.data, "postcode": postcode.data.replace(" ", "").upper(), "max distance": max_distance.data, "condition": condition.data, "specific": {"brand": brand.data}})
        return flask.redirect(flask.url_for("cpus", filters = filters))
    try:
        filters = json.loads(flask.request.args.get('filters', None))
        displayed_posts = display_posts(posts, component_dict, "cpus", filters["query"], filters["sort"], filters["postcode"], filters["max distance"], filters["condition"], filters["specific"])
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    except:
        displayed_posts = display_posts(posts, component_dict, "cpus")
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    return flask.render_template("cpu_posts.html", title = "CPU Posts", displayed_posts = displayed_posts, cpu_search_form = cpu_search_form)

@app.route("/browse-posts/video-cards", methods= ['GET', 'POST'])
def video_cards():
    gpu_search_form = search.GPUSearch()
    gpu_search_form.brand.choices = [(i, i) for i in search.get_choices("gpus", "brand")]
    if gpu_search_form.validate_on_submit():
        query = gpu_search_form.query
        sort = gpu_search_form.sort
        postcode = gpu_search_form.postcode
        max_distance = gpu_search_form.max_distance
        condition = gpu_search_form.condition
        brand = gpu_search_form.brand
        filters = json.dumps({"query": query.data, "sort": sort.data, "postcode": postcode.data.replace(" ", "").upper(), "max distance": max_distance.data, "condition": condition.data, "specific": {"brand": brand.data}})
        return flask.redirect(flask.url_for("video_cards", filters = filters))
    try:
        filters = json.loads(flask.request.args.get('filters', None))
        displayed_posts = display_posts(posts, component_dict, "gpus", filters["query"], filters["sort"], filters["postcode"], filters["max distance"], filters["condition"], filters["specific"])
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    except:
        displayed_posts = display_posts(posts, component_dict, "gpus")
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    return flask.render_template("gpu_posts.html", title = "Graphics Card Posts", displayed_posts = displayed_posts, gpu_search_form = gpu_search_form)

@app.route("/browse-posts/cases", methods= ['GET', 'POST'])
def cases():
    case_search_form = search.OtherSearch()
    if case_search_form.validate_on_submit():
        query = case_search_form.query
        sort = case_search_form.sort
        postcode = case_search_form.postcode
        max_distance = case_search_form.max_distance
        condition = case_search_form.condition
        filters = json.dumps({"query": query.data, "sort": sort.data, "postcode": postcode.data.replace(" ", "").upper(), "max distance": max_distance.data, "condition": condition.data})
        return flask.redirect(flask.url_for("cases", filters = filters))
    try:
        filters = json.loads(flask.request.args.get('filters', None))
        displayed_posts = display_posts(posts, component_dict, "cases", filters["query"], filters["sort"], filters["postcode"], filters["max distance"], filters["condition"])
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    except:
        displayed_posts = display_posts(posts, component_dict, "cases")
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    return flask.render_template("case_posts.html", title = "Case Posts", displayed_posts = displayed_posts, case_search_form = case_search_form)

@app.route("/browse-posts/motherboards", methods= ['GET', 'POST'])
def motherboards():
    motherboard_search_form = search.OtherSearch()
    if motherboard_search_form.validate_on_submit():
        query = motherboard_search_form.query
        sort = motherboard_search_form.sort
        postcode = motherboard_search_form.postcode
        max_distance = motherboard_search_form.max_distance
        condition = motherboard_search_form.condition
        filters = json.dumps({"query": query.data, "sort": sort.data, "postcode": postcode.data.replace(" ", "").upper(), "max distance": max_distance.data, "condition": condition.data})
        return flask.redirect(flask.url_for("motherboards", filters = filters))
    try:
        filters = json.loads(flask.request.args.get('filters', None))
        displayed_posts = display_posts(posts, component_dict, "motherboards", filters["query"], filters["sort"], filters["postcode"], filters["max distance"], filters["condition"])
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    except:
        displayed_posts = display_posts(posts, component_dict, "motherboards")
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    return flask.render_template("motherboard_posts.html", title = "Motherboard Posts", displayed_posts = displayed_posts, motherboard_search_form = motherboard_search_form)

@app.route("/browse-posts/memory", methods= ['GET', 'POST'])
def memory():
    ram_search_form = search.RAMSearch()
    ram_search_form.module_type.choices = [(i, i) for i in search.get_choices("ram", "type")]
    ram_search_form.speed.choices = [(i, i) for i in search.get_choices("ram", "speed")]
    ram_search_form.size.choices = [(i, i) for i in search.get_choices("ram", "size")]
    ram_search_form.form_factor.choices = [(i, i) for i in search.get_choices("ram", "form factor")]
    if ram_search_form.validate_on_submit():
        query = ram_search_form.query
        sort = ram_search_form.sort
        postcode = ram_search_form.postcode
        max_distance = ram_search_form.max_distance
        condition = ram_search_form.condition
        module_type = ram_search_form.module_type
        speed = ram_search_form.speed
        size = ram_search_form.size
        form_factor = ram_search_form.form_factor
        filters = json.dumps({"query": query.data, "sort": sort.data, "postcode": postcode.data.replace(" ", "").upper(), "max distance": max_distance.data, "condition": condition.data, "specific": {"type": module_type.data, "speed": speed.data, "size": size.data, "form factor": form_factor.data}})
        return flask.redirect(flask.url_for("memory", filters = filters))
    try:
        filters = json.loads(flask.request.args.get('filters', None))
        displayed_posts = display_posts(posts, component_dict, "ram", query_param = filters["query"], sort = filters["sort"], postcode = filters["postcode"], max_distance = filters["max distance"], conditions_param = filters["condition"], filters_param = filters["specific"])
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    except:
        displayed_posts = display_posts(posts, component_dict, "ram")
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    return flask.render_template("ram_posts.html", title = "Memory Posts", displayed_posts = displayed_posts, ram_search_form = ram_search_form)

@app.route("/browse-posts/storage", methods= ['GET', 'POST'])
def storage():
    storage_search_form = search.StorageSearch()
    storage_search_form.storage_type.choices = [(i, i) for i in search.get_choices("storage", "type")]
    storage_search_form.rpm.choices = [(i, i) for i in search.get_choices("storage", "rpm")]
    storage_search_form.size.choices = [(i, i) for i in search.get_choices("storage", "size")]
    storage_search_form.form_factor.choices = [(i, i) for i in search.get_choices("storage", "form factor")]
    storage_search_form.interface.choices = [(i, i) for i in search.get_choices("storage", "interface")]
    if storage_search_form.validate_on_submit():
        query = storage_search_form.query
        sort = storage_search_form.sort
        postcode = storage_search_form.postcode
        max_distance = storage_search_form.max_distance
        condition = storage_search_form.condition
        storage_type = storage_search_form.storage_type
        rpm = storage_search_form.rpm
        size = storage_search_form.size
        form_factor = storage_search_form.form_factor
        interface = storage_search_form.interface
        filters = json.dumps({"query": query.data, "sort": sort.data, "postcode": postcode.data.replace(" ", "").upper(), "max distance": max_distance.data, "condition": condition.data, "specific": {"type": storage_type.data, "rpm": rpm.data, "size": size.data, "form factor": form_factor.data, "interface": interface.data}})
        return flask.redirect(flask.url_for("storage", filters = filters))
    try:
        filters = json.loads(flask.request.args.get('filters', None))
        displayed_posts = display_posts(posts, component_dict, "storage", query_param = filters["query"], sort = filters["sort"], postcode = filters["postcode"], max_distance = filters["max distance"], conditions_param = filters["condition"], filters_param = filters["specific"])
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    except:
        displayed_posts = display_posts(posts, component_dict, "storage")
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    return flask.render_template("storage_posts.html", title = "Storage Posts", displayed_posts = displayed_posts, storage_search_form = storage_search_form)

@app.route("/browse-posts/power-supplies", methods= ['GET', 'POST'])
def power_supplies():
    psu_search_form = search.PSUSearch()
    psu_search_form.efficiency.choices = [(i, i) for i in search.get_choices("psus", "efficiency")]
    psu_search_form.form_factor.choices = [(i, i) for i in search.get_choices("psus", "form factor")]
    psu_search_form.wattage.choices = [(i, i) for i in search.get_choices("psus", "wattage")]
    psu_search_form.modular.choices = [(i, i) for i in search.get_choices("psus", "modular")]
    if psu_search_form.validate_on_submit():
        query = psu_search_form.query
        sort = psu_search_form.sort
        postcode = psu_search_form.postcode
        max_distance = psu_search_form.max_distance
        condition = psu_search_form.condition
        efficiency = psu_search_form.efficiency
        wattage = psu_search_form.wattage
        modular = psu_search_form.modular
        form_factor = psu_search_form.form_factor
        filters = json.dumps({"query": query.data, "sort": sort.data, "postcode": postcode.data.replace(" ", "").upper(), "max distance": max_distance.data, "condition": condition.data, "specific": {"efficiency": efficiency.data, "wattage": wattage.data, "modular": modular.data, "form factor": form_factor.data}})
        return flask.redirect(flask.url_for("power_supplies", filters = filters))
    try:
        filters = json.loads(flask.request.args.get('filters', None))
        displayed_posts = display_posts(posts, component_dict, "psus", query_param = filters["query"], sort = filters["sort"], postcode = filters["postcode"], max_distance = filters["max distance"], conditions_param = filters["condition"], filters_param = filters["specific"])
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    except:
        displayed_posts = display_posts(posts, component_dict, "psus")
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    return flask.render_template("psu_posts.html", title = "Power Supply Posts", displayed_posts = displayed_posts, psu_search_form = psu_search_form)

@app.route("/browse-posts/other", methods= ['GET', 'POST'])
def other():
    other_search_form = search.OtherSearch()
    if other_search_form.validate_on_submit():
        query = other_search_form.query
        sort = other_search_form.sort
        postcode = other_search_form.postcode
        max_distance = other_search_form.max_distance
        condition = other_search_form.condition
        filters = json.dumps({"query": query.data, "sort": sort.data, "postcode": postcode.data.replace(" ", "").upper(), "max distance": max_distance.data, "condition": condition.data})
        return flask.redirect(flask.url_for("other", filters = filters))
    try:
        filters = json.loads(flask.request.args.get('filters', None))
        displayed_posts = display_posts(posts, component_dict, "other", filters["query"], filters["sort"], filters["postcode"], filters["max distance"], filters["condition"])
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    except:
        displayed_posts = display_posts(posts, component_dict, "other")
        for post in displayed_posts:
            post["readable time"] = get_time_created(post["time created"])
    return flask.render_template("other_posts.html", title = "Other Posts", displayed_posts = displayed_posts, other_search_form = other_search_form)

@app.route("/set-category", methods= ['GET', 'POST'])
def set_category():
    category_form = filters.CategoryForm()
    if category_form.validate_on_submit():
        category = category_form.category.data
        flask.session.clear()
        if category == "Other":
            flask.session["item id"] = component_dict["other"]["id"]
            return flask.redirect(flask.url_for('create_post'))
        elif category == "Motherboard":
            flask.session["item id"] = component_dict["motherboards"]["id"]
            return flask.redirect(flask.url_for('create_post'))
        elif category == "Case":
            flask.session["item id"] = component_dict["cases"]["id"]
            return flask.redirect(flask.url_for('create_post'))
        elif category == "CPU":
            return flask.redirect(flask.url_for('set_cpus'))
        elif category == "Graphics Card":
            return flask.redirect(flask.url_for('set_gpus'))
        elif category == "Memory":
            return flask.redirect(flask.url_for('set_ram'))
        elif category == "Power Supply":
            return flask.redirect(flask.url_for('set_psus'))
        elif category == "Storage":
            return flask.redirect(flask.url_for('set_storage'))
    return flask.render_template("set-category.html", title = "Set Post Category", category_form = category_form)

@app.route("/set-cpus", methods = ["GET", "POST"])
def set_cpus():
    options = []
    flask.session["options"] = options
    cpu_form = filters.CPUForm()
    if cpu_form.validate_on_submit():
        brand = cpu_form.brand.data
        query = cpu_form.query.data
        if query == "":
            query = None
        for part in component_dict["cpus"]:
            if query:
                if query.lower() in part["name"].lower() and part["brand"] == brand:
                    options.append((part["id"], part["name"]))
            else:
                if part["brand"] == brand:
                    options.append((part["id"], part["name"]))
        flask.session["options"] = options
        return flask.redirect(flask.url_for("set_item"))
    return flask.render_template("set-cpus.html", title = "CPU Filters", cpu_form = cpu_form)

@app.route("/set-gpus", methods = ["GET", "POST"])
def set_gpus():
    options = []
    gpu_form = filters.GPUForm()
    if gpu_form.validate_on_submit():
        brand = gpu_form.brand.data
        query = gpu_form.query.data
        if query == "":
            query = None
        for part in component_dict["gpus"]:
            if query:
                if query.lower() in part["name"].lower() and part["brand"] == brand:
                    options.append((part["id"], part["name"]))
            else:
                if part["brand"] == brand:
                    options.append((part["id"], part["name"]))
        flask.session["options"] = options
        return flask.redirect(flask.url_for("set_item"))
    return flask.render_template("set-gpus.html", title = "Graphics Card Filters", gpu_form = gpu_form)

@app.route("/set-psus", methods = ['GET', 'POST'])
def set_psus():
    options = []
    psu_form = filters.PSUForm()
    if psu_form.validate_on_submit():
        efficiency = psu_form.efficiency.data
        form_factor = psu_form.form_factor.data
        wattage = psu_form.wattage.data
        modular = psu_form.modular.data
        for part in component_dict["psus"]:
            if part["efficiency"] == efficiency and part["form factor"] == form_factor and part["wattage"] == wattage and part["modular"] == modular:
                flask.session["item id"] = part["id"]
                return flask.redirect(flask.url_for("create_post"))
        flask.session["options"] = options
        return flask.redirect(flask.url_for("set_item"))
    return flask.render_template("set-psus.html", title = "Power Supply Filters", psu_form = psu_form)

@app.route("/set-ram", methods = ['GET', 'POST'])
def set_ram():
    options = []
    ram_form = filters.RAMForm()
    if ram_form.validate_on_submit():
        module_type = ram_form.module_type.data
        speed = ram_form.speed.data
        size = ram_form.size.data
        form_factor = ram_form.form_factor.data
        for part in component_dict["ram"]:
            if part["type"] == module_type and part["speed"] == speed and part["size"] == size and part["form factor"] == form_factor:
                flask.session["item id"] = part["id"]
                return flask.redirect(flask.url_for("create_post"))
        flask.session["options"] = options
        return flask.redirect(flask.url_for("set_item"))
    return flask.render_template("set-ram.html", title = "Memory Filters", ram_form = ram_form)

@app.route("/set-storage", methods = ['GET', 'POST'])
def set_storage():
    options = []
    storage_form = filters.StorageForm()
    if storage_form.validate_on_submit():
        size = storage_form.size.data
        drive_type = storage_form.drive_type.data
        form_factor = storage_form.form_factor.data
        interface = storage_form.interface.data
        rpm = storage_form.rpm.data
        if rpm == "SSD":
            fixed_rpm = "None"
        else:
            fixed_rpm = rpm
        for part in component_dict["storage"]:
            if part["size"] == size and part["type"] == drive_type and part["form factor"] == form_factor and part["interface"] == interface and part["rpm"] == fixed_rpm:
                flask.session["item id"] = part["id"]
                return flask.redirect(flask.url_for("create_post"))
        flask.session["options"] = options
        return flask.redirect(flask.url_for("set_item"))
    return flask.render_template("set-storage.html", title = "Storage Filters", storage_form = storage_form)

@app.route("/set-item", methods = ['GET', 'POST'])
def set_item():
    options = flask.session["options"]
    options.append((component_dict["other"]["id"], "Other"))
    item_form = ItemForm()
    item_form.item.choices = options
    if item_form.validate_on_submit():
        item = item_form.item.data
        flask.session["item id"] = item
        return flask.redirect(flask.url_for("create_post"))
    return flask.render_template("set-item.html", title = "Set Post Item", item_form = item_form)

@app.route("/create-post", methods = ['GET', 'POST'])
def create_post():
    item_id = flask.session["item id"]
    price_reccomendation = None
    price_reccomendation_error = None
    if (item_id >= component_dict["cpus"][0]["id"] and item_id <= component_dict["cpus"][-1]["id"]) or (item_id >= component_dict["ram"][0]["id"] and item_id <= component_dict["psus"][-1]["id"]):
        try:
            num = get_price_reccomendation(posts, item_id)
            price_reccomendation = "£{:.2f}".format(num)
        except ZeroDivisionError:
            price_reccomendation_error = "No other posts of this type exist, so can't obtain price reccomendation"
    form = PostCreationForm()
    if form.validate_on_submit():
        title = form.title.data
        price = form.price.data
        email = form.email.data
        description = form.description.data
        condition = form.condition.data
        location = form.location.data.replace(" ", "").upper()
        picture = form.picture.data
        upload_post(title, item_id, email, description, condition, location, picture, price, posts)
        flask.flash(f'Post: {form.title.data} submitted ', 'success')
        return flask.redirect(flask.url_for('home'))
    return flask.render_template('create-post.html', title = 'Create Post', form = form, price_reccomendation = price_reccomendation, price_reccomendation_error = price_reccomendation_error)

#attempted to do post creation with multiple forms on one page where each form was reliant on previous form 
#but didnt work as previous forms would be reset when submitting later forms making it impossible to validate the form that i want to validate
#instead each form will have its own page and data needed by later forms will be stored as cookies
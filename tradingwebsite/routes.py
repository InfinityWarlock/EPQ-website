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

data = ["Heading 1", "Heading 2", "Heading 3"] # will eventually be changed
@app.route("/")
@app.route("/home")
def home():
    return flask.render_template("home.html", data = data, title = "Home") # Will likely only have to worry about this part of the site when i do the frontend

#same for the about page
@app.route("/about")
def about():
    return flask.render_template("about.html", title = "About")

@app.route("/browse-posts", methods = ['GET', 'POST'])
def browse_posts():
    #the following is temporary
    return "hello"

@app.route("/browse-posts/cpus", methods= ['GET', 'POST'])
def cpus():
    cpu_search_form = search.CPUSearch()
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

@app.route("/browse-posts/video-cards")
def video_cards():
    pass

@app.route("/browse-posts/cases")
def cases():
    pass

@app.route("/browse-posts/motherboards")
def motherboards():
    pass

@app.route("/browse-posts/memory")
def memory():
    pass

@app.route("/browse-posts/storage")
def storage():
    pass

@app.route("/browse-posts/power-supplies")
def power_supplies():
    pass

@app.route("/browse-posts/other")
def other():
    pass

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
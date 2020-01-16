import time
from geopy.distance import geodesic
import geocoder
from tradingwebsite.search import get_choices

POST_EXPIRE_TIME = 2592000 #30 days in seconds
INVALID_TIME = 172800 #2 days in seconds

def upload_post(title, item, email, description, condition, location, picture, price, db):
    pic = None
    if picture != "":
        pic = picture
    post_dict = {"title": title, "item": item, "price": price, "email": email, "description": description, "condition": condition, "location": location, "picture": pic, "time created": time.time(), "expired": False}
    db.insert_one(post_dict)

def update_posts(db):
    timestamp = time.time()
    expired_time = timestamp - POST_EXPIRE_TIME
    invalid_time = timestamp + INVALID_TIME #If a user somehow (i dont even know if this is possible but might as well allow for it) managed to force
    #a time in the future as their time created for their post (ie so it would take much longer to expire) this will detect that and delete the post
    query = {"time created": {"$lt": expired_time}, "expired": False}
    update = {"$set": {"expired": True}}
    db.update_many(query, update)
    invalid_post_query = {"time created": {"$gt": invalid_time}}
    db.delete_many(invalid_post_query)

def get_posts(db, ids = None, search = None, condition = None, allow_expired = False):
    final_posts = []
    update_posts(db)
    if search:
        if allow_expired:
            title_query = {"title": {"$regex": search}}
            description_query = {"description": {"$regex": search}}
        else:
            title_query = {"title": {"$regex": search}, "expired": False}
            description_query = {"description": {"$regex": search}, "expired": False}
        if condition:
            title_query["condition"] = condition
            description_query["condition"] = condition
        title_posts = db.find(title_query)
        for post in title_posts:
            final_posts.append(post)
        description_posts = db.find(description_query)
        for post in description_posts:
            if post not in final_posts:
                final_posts.append(post)
        if ids:
            remove_list = []
            for post in range(len(final_posts)):
                if final_posts[post]["item"] not in ids:
                    remove_list.append(post)
            for i in remove_list:
                del final_posts[i]
                for j in range(len(remove_list)):
                    remove_list[j] += -1
    else:
        if ids:
            for val in ids:
                if allow_expired:
                    query = {"item": val}
                else:
                    query = {"item": val, "expired": False}
                if condition:
                    query["condition"] = condition
                posts = db.find(query)
                for post in posts:
                    final_posts.append(post)
        else:
            if allow_expired:
                if condition:
                    query = {"condition": condition}
                    posts = db.find(query)
                else:
                    posts = db.find()
            else:
                query = {"expired": False}
                if condition:
                    query["condition"] = condition
                posts = db.find(query)
            for post in posts:
                final_posts.append(post)
    return final_posts

def get_price_reccomendation(db, part_id):
    posts = get_posts(db, [part_id], allow_expired = True)
    weighted_sum = 0
    sum_of_weights = 0
    timestamp = time.time()
    for post in posts:
        post_age = timestamp - post["time created"]
        if post_age > 0:
            weight = 1/post_age
            price = post["price"]
            weighted_sum += price*weight
            sum_of_weights += weight
    weighted_average = weighted_sum/sum_of_weights
    return weighted_average

def get_distance(a, b): #a and b are 2 different postcodes (these will be verified already)
    alatlng = geocoder.google(a).latlng
    blatlng = geocoder.google(b).latlng
    distance = geodesic(alatlng, blatlng).miles
    return distance

def display_posts(posts, parts, category = None, query_param = None, sort = "t", postcode = None, max_distance = None, conditions_param = None, filters_param = None):
    if conditions_param == []:
        conditions = ["New", "Good", "Slightly Faulty", "Not working at all"]
    else:
        conditions = conditions_param
    if filters_param:
        filters = filters_param
        for key, value in filters.items():
            if value == []:
                filters[key] = get_choices(category, key)
        
    if query_param == "":
        query = None
    else:
        query = query_param
    if category:
        ids = []
        if postcode: #if postcode is passed as a parameter then others wont be empty
            for part in parts[category]:
                id_valid = True
                for key, value in filters.items():
                    filter_valid = False
                    for item in value:
                        if part[key] == item:
                            filter_valid = True
                            break
                    if filter_valid == False:
                        id_valid = False
                        break
                if id_valid:
                    ids.append(part["id"])
            post_matches = []
            for condition in conditions:
                condition_matches = get_posts(posts, ids = ids, search = query, condition = condition)
                for p in condition_matches:
                    if p not in post_matches and (get_distance(p["location"], postcode) <= max_distance or max_distance == 200): #add distance condition and function here
                        post_matches.append(p)
        else:
            for part in parts[category]:
                ids.append(part["id"])
            post_matches = get_posts(posts, ids)
    else:
        if postcode:
            post_matches = []
            for condition in conditions:
                condition_matches = get_posts(posts, search = query, condition = condition)
                for p in condition_matches:
                    if p not in post_matches and (get_distance(p["location"], postcode) <= max_distance or max_distance == 200): #add distance condition and function here
                        post_matches.append(p)
        else:
            post_matches = get_posts(posts)
    if sort == "t": #sort by time added
        post_matches = sorted(post_matches, key = lambda i: i['time created'], reverse = True)
    elif sort == "p": #sort by price
        post_matches = sorted(post_matches, key = lambda i: i['price'])
    elif sort == "d": #sort by distance
        post_matches = sorted(post_matches, key = lambda i: get_distance(i["location"], postcode)) #will do a similar thing to the above calling a to be created 'get distance' function that compares the postcode on the post to the postcode in params
    return post_matches


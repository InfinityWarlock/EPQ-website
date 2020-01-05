import time

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
        search = search
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
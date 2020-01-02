import flask
import pymongo
from pprint import pprint
from forms import PostCreationForm
from database import upload_post, get_posts

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = 'd214895cc0f65074680c2468af85c90d'

db_connection_string = "mongodb+srv://CatnipMasterRace:XuUrP6Ui5EErAcro@epq-trading-site-q3dcn.gcp.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(db_connection_string)
db = client.epq_trading_site
posts = db.posts

p = get_posts(posts, search="a")
print(p, "\n Done printing")
# serverStatusResult = db.command("serverStatus")
# pprint(serverStatusResult)

data = ["Heading 1", "Heading 2", "Heading 3"]
@app.route("/")
@app.route("/home")
def home():
    return flask.render_template("home.html", data = data, title = "Home")


@app.route("/about")
def about():
    return flask.render_template("about.html", title = "About")

@app.route("/create-post", methods = ['GET', 'POST'])
def create_post():
    form = PostCreationForm()
    if form.validate_on_submit():
        title = form.title.data
        item = form.item.data
        email = form.email.data
        description = form.description.data
        condition = form.condition.data
        location = form.location.data.replace(" ", "").upper()
        picture = form.picture.data
        upload_post(title, item, email, description, condition, location, picture, posts)
        flask.flash(f'Post: {form.title.data} submitted ', 'success')
        return flask.redirect(flask.url_for('home'))
    return flask.render_template('create-post.html', title = 'Create Post', form = form)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


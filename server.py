import flask
import pymongo
from pprint import pprint

app = flask.Flask(__name__)

db_connection_string = "mongodb+srv://CatnipMasterRace:XuUrP6Ui5EErAcro@epq-trading-site-q3dcn.gcp.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(db_connection_string)
db = client.epq_trading_site

serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)

data = ["Heading 1", "Heading 2", "Heading 3"]
@app.route("/")
@app.route("/home")
def home():
    return flask.render_template("home.html", data = data, title = "Home")


@app.route("/about")
def about():
    return flask.render_template("about.html", title = "About")

if __name__ == '__main__':
    app.run(debug=True, port=5000)


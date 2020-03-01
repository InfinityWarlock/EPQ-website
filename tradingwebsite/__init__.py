from flask import Flask
import pymongo


app = Flask(__name__)

app.config['SECRET_KEY'] = 'd214895cc0f65074680c2468af85c90d'

db_connection_string = MONGODB_URI
client = pymongo.MongoClient(db_connection_string)
db = client.epq_trading_site

from tradingwebsite import routes
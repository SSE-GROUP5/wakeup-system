from flask_pymongo import PyMongo
from constants import MONGODB_URL

mongo = PyMongo()

def init_app(app):
  app.config['MONGO_URI'] = MONGODB_URL
  mongo.init_app(app)

def get_db():
  return mongo.db
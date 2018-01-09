from flask import Flask
from flask_restful import Api 
from flask_jwt import JWT


from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
#from file import class/method

from security import authenticate, identity


#jsonify not needed, flask restful do it for us
#202 return when creating will take long time
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #it can be mysql, sqlOracle, postGre
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'francisco' #importan for jwt
api = Api(app)


@app.before_first_request
def create_tables():
	db.create_all() # 


jwt = JWT(app, authenticate, identity) # jwt creates a new endpoint --> /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') #http:127.0.0.1:8080/5000/student/Rolf
api.add_resource(ItemList,'/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
	print("Entered main")
	from db import db
	db.init_app(app) #passing the flask app
	app.run(port=8080, debug=True)
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
	#parser will belong directly to the Item class, and not to each specific resource , we have to access it bye using Item.parser 
	parser = reqparse.RequestParser()
	parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
	parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id.")
	#if an extra argument is passed, reqparser will erased, and we'll never see it
		
	#data = request.get_json() #json payload, this was used before using **reqparse**
	@jwt_required()
	def get(self,name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': "Item not found"}, 404
			
	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}, 400 #bad request, because item already exists			

		data = Item.parser.parse_args()

		item = ItemModel(name, data['price'], data['store_id'])
		try:
			item.save_to_db()
		except:
			return {"message": "An error ocurred inserting the item."}, 500 # 500 means internal Server error 


		return item.json(), 201 

	def delete(self, name):
		item = ItemModel.find_by_name(name)

		if item:
			item.delete_from_db()

		return {'message': 'Item deleted'}

	def put(self, name):
		data = Item.parser.parse_args()
		
		item = ItemModel.find_by_name(name)

		if item is None:
			item = ItemModel(name, **data) #ItemModel(name, data['price'], data['store_id'])
		else:
			item.price = data['price']

		item.save_to_db()
			
		
		return item.json()


class ItemList(Resource):
	def get(self):
		#return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} try to use map, only when your are programming other languages
		return {'item': [item.json() for item in ItemModel.query.all()]}

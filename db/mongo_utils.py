import pymongo
from pymongo import MongoClient

conf = {
	'MONGO_HOST': 'localhost',
	'MONGO_PORT': '27017',
	'MONGO_DB_NAME': 'clikipedia'
}

client = MongoClient('mongodb://' + conf['MONGO_HOST'] + ':' + conf['MONGO_PORT'])
db = client['MONGO_DB_NAME']


def verify_doc(doc):
	try:
		json.load(doc)
		return True
	except ValueError as err:
		return False


def insert_doc(doc, collection):
	if verify_doc(doc):
		try:
			collection = db.collection
			collection.insert_one(doc)
			return True
		except Exception as err:
			print(err)
			return False
	else:
		print('Not a valid JSON document.')
		return False


def get_result(filters={}):
	if not filters:
		try:
			scan = scans.find_one()
			return scan
		except Exception as err:
			print(err)
			return False
	else:
		try:
			try:
				json.load(filters)
			except ValueError as err:
				print(ValueError)
				print("Filters for query are not in valid JSON format.")
				return False
			scan = scans.find_one(filters)
			return scan
		except Exception as err:
			print(err)
			return False


def main():
	pass


if __name__ == '__main__':
	main()

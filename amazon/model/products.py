from amazon.model import db
from bson.objectid import ObjectId


def search_product(name):

    query = {'name': name}
    matching_products = db['products'].find(query)
    return list(matching_products)


def get_details(p_id):
    cursor = db.products.find({'_id': ObjectId(p_id)})
    if cursor.count() == 1:
        return cursor[0]
    else:
        return None


def add_product(product):
    db['products'].insert_one(product)


def update_product(product_id, updated_product):
    filter = {'_id': ObjectId(product_id)}
    update = {
        '$set': updated_product
    }

    #Update in DB
    db['products'].update_one(filter=filter, update=update)


from flask import Blueprint, request
from marshmallow import ValidationError
from api.models import Product
from api.schemas import ProductSchema

products_blueprint = Blueprint('products_blueprint', __name__)

@products_blueprint.route('/all', methods=['GET'])
def get_all_products():
    product_schema = ProductSchema(many=True)
    try:
        products = Product.select().dicts()
        products_serialized = product_schema.dump(products)
    except Exception as err:
        return { 'data': [], 'message': str(err) }, 500
    return { 'data': products_serialized, 'message': '' }, 200


from pytest import fixture
from app import PRODUCTS_URL
from api.blueprints.products import products_blueprint
from api.models import Customer, Product, Orders
import json

@fixture()
def test_client(test_app):
    test_app.register_blueprint(products_blueprint, url_prefix=PRODUCTS_URL)
    return test_app.test_client()

@fixture()
def init_db():
    customer = Customer(CustomerFirstName="Test1", CustomerLastName="McTest1")
    customer.save()

    active_product = Product(
        ProductName="Test1",
        ProductPhotoURL="/test1",
        ProductStatus="Active"
    )
    active_product.save()
    in_active_product = Product(
        ProductName="Test2",
        ProductPhotoURL="/test2",
        ProductStatus="InActive"
    )
    in_active_product.save()

    orders = [
        Orders(**{
            "OrderStatus": "Queued",
            "ProductID": active_product.ProductID,
            "CustomerID": customer.CustomerID,
        }),
        Orders(**{
            "OrderStatus": "Complete",
            "ProductID": active_product.ProductID,
            "CustomerID": customer.CustomerID,
        }),
        Orders(**{
            "OrderStatus": "Cancelled",
            "ProductID": active_product.ProductID,
            "CustomerID": customer.CustomerID,
        }),
        Orders(**{
            "OrderStatus": "Cancelled",
            "ProductID": in_active_product.ProductID,
            "CustomerID": customer.CustomerID,
        }),
    ]
    for order in orders: order.save()
    return orders, [active_product, in_active_product], [customer]

def test_get_all_orders(test_client, init_db):
    response = test_client.get(f"{PRODUCTS_URL}/all")
    assert response.status_code == 200
    deserialized_response = json.loads(response.data)
    data = deserialized_response.get('data')
    assert data is not None
    assert len(data) == 1
    order_statuses = {}
    for order in data:
        status = order.get("OrderStatus")
        if status in order_statuses.keys():
            order_statuses[status] += 1
        else: order_statuses[status] = 1
    assert len(order_statuses.keys()) == 1
    assert order_statuses.get("Queued") == 1

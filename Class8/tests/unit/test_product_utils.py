from bson import ObjectId


def test_validate_product_payload_accepts_valid_input(app_module):
    payload = {
        "name": "Test Product",
        "description": "Something",
        "price": 120000,
        "in_stock": True,
    }

    result = app_module.validate_product_payload(payload)
    assert result is None


def test_validate_product_payload_requires_name(app_module):
    payload = {
        "price": 120000,
    }

    result = app_module.validate_product_payload(payload)
    assert result == "Missing required field: name"


def test_validate_product_payload_requires_numeric_price(app_module):
    payload = {
        "name": "Keyboard",
        "price": "120000",
    }

    result = app_module.validate_product_payload(payload)
    assert result == "price must be a number"


def test_validate_product_payload_rejects_empty_name(app_module):
    payload = {
        "name": "   ",
        "price": 1000,
    }

    result = app_module.validate_product_payload(payload)
    assert result == "name must be a non-empty string"


def test_to_product_doc_maps_id_and_defaults(app_module):
    doc = {
        "_id": ObjectId(),
        "name": "Mouse",
        "price": 350000,
    }

    product = app_module.to_product_doc(doc)

    assert product["id"] == str(doc["_id"])
    assert product["name"] == "Mouse"
    assert product["description"] == ""
    assert product["price"] == 350000
    assert product["in_stock"] is True

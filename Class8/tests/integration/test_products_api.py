def test_products_crud_flow(api_client):
    create_payload = {
        "name": "Integration Product",
        "description": "created in integration test",
        "price": 789000,
        "in_stock": True,
    }

    create_response = api_client.post("/api/v1/products", json=create_payload)
    assert create_response.status_code == 201

    created = create_response.get_json()
    product_id = created["id"]
    assert created["name"] == create_payload["name"]

    list_response = api_client.get("/api/v1/products")
    assert list_response.status_code == 200
    listed = list_response.get_json()
    assert any(item["id"] == product_id for item in listed)

    get_response = api_client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["name"] == create_payload["name"]

    update_payload = {
        "name": "Integration Product Updated",
        "description": "updated",
        "price": 990000,
        "in_stock": False,
    }

    update_response = api_client.put(
        f"/api/v1/products/{product_id}",
        json=update_payload,
    )
    assert update_response.status_code == 200
    updated = update_response.get_json()
    assert updated["name"] == update_payload["name"]
    assert updated["in_stock"] is False

    delete_response = api_client.delete(f"/api/v1/products/{product_id}")
    assert delete_response.status_code == 204

    not_found_response = api_client.get(f"/api/v1/products/{product_id}")
    assert not_found_response.status_code == 404


def test_get_product_rejects_invalid_object_id(api_client):
    response = api_client.get("/api/v1/products/not-a-valid-objectid")
    assert response.status_code == 400
    assert response.get_json()["message"] == "Invalid product id"

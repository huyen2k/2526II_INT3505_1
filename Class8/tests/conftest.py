from pathlib import Path
import importlib.util

import mongomock
import pytest


@pytest.fixture(scope="session")
def app_module():
    root_dir = Path(__file__).resolve().parents[2]
    app_path = root_dir / "Class7" / "app.py"

    spec = importlib.util.spec_from_file_location("class7_app", app_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def fake_products_collection():
    mongo = mongomock.MongoClient()
    return mongo["class7_test_db"]["products"]


@pytest.fixture
def api_client(app_module, fake_products_collection):
    app_module.products_collection = fake_products_collection
    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as client:
        yield client

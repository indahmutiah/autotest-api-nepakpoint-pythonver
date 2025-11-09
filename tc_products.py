import pytest
from playwright.sync_api import APIRequestContext, sync_playwright

BASE_URL = "https://nepak-point-api.indahmutiah.com"
products_endpoint = f"{BASE_URL}/products"


@pytest.fixture(scope="session")
def request_context():
    """Fixture untuk membuat API request context"""
    with sync_playwright() as p:
        request = p.request.new_context(base_url=BASE_URL)
        yield request
        request.dispose()

# TS-01: Positive Test API Products
def test_p_01_get_all_products(request_context: APIRequestContext):
    response = request_context.get("/products")
    assert response.status == 200
    assert response.ok
    print("✅ TC-P-01: Get all products berhasil!")


def test_p_02_get_products_by_search(request_context: APIRequestContext):
    query = "yonex"
    response = request_context.get(f"/products/search?q={query}")
    assert response.status == 200
    assert response.ok
    print("✅ TC-P-02: Get product by search berhasil!")


def test_tc_03_get_product_by_slug(request_context: APIRequestContext):
    product_slug = "decathlon-kok-bulu-fsc-930-speed-77-x-12"
    response = request_context.get(f"/products/{product_slug}")
    assert response.status == 200
    assert response.ok
    print("✅ TC-P-03: Get product by slug berhasil!")

# TS-02: Negative Test API Products
def test_n_01_get_product_invalid_slug(request_context: APIRequestContext):
    invalid_slug = "invalid-slug"
    response = request_context.get(f"/products/{invalid_slug}")
    assert response.status == 404
    print("✅ TC-N-01: Invalid slug mengembalikan 404 seperti yang diharapkan.")

from app import app

def test_health_endpoint():
    """Verifica que el endpoint de salud responda HTTP 200."""
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_api_laptops_endpoint():
    """Verifica que la API retorne la lista de portátiles en JSON."""
    client = app.test_client()
    response = client.get("/api/laptops")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["total"] > 0

def test_index_html_renders():
    """Verifica que la página principal renderice el catálogo HTML."""
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Cat\xc3\xa1logo Automatizado de Port\xc3\xa1tiles" in response.data

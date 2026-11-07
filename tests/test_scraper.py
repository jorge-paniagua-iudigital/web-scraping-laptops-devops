import pytest
from src.scraper import extract_laptops

def test_extract_laptops_returns_data():
    data = extract_laptops()
    assert isinstance(data, list)
    assert len(data) > 0

def test_extract_laptops_schema():
    data = extract_laptops()
    first_item = data[0]
    expected_keys = {"Herramienta", "Titulo", "Precio", "Descripcion", "Enlace"}
    assert set(first_item.keys()) == expected_keys
    assert first_item["Titulo"] != "N/A"
    assert "$" in first_item["Precio"]

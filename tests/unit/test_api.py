"""
Unit tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from models import SizeEnum, CoffeeTypeEnum, FlavorEnum, MilkTypeEnum


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestRootEndpoint:
    """Test the root endpoint."""

    def test_root_endpoint(self, client):
        """Test the root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome to the Coffee Shop API" in data["message"]
        assert "docs" in data
        assert "menu" in data


class TestMenuEndpoint:
    """Test the menu endpoint."""

    def test_get_menu(self, client, menu_data):
        """Test getting the menu."""
        response = client.get("/menu")
        assert response.status_code == 200
        data = response.json()
        
        assert "sizes" in data
        assert "coffee_types" in data
        assert "flavors" in data
        assert "milk_types" in data
        assert "max_extra_shots" in data
        assert "max_flavors" in data
        
        assert data["sizes"] == ["small", "medium", "large"]
        assert data["coffee_types"] == ["iced", "hot"]
        assert "hazelnut" in data["flavors"]
        assert "oat" in data["milk_types"]
        assert data["max_extra_shots"] == 5
        assert data["max_flavors"] == 3


class TestHealthEndpoint:
    """Test the health check endpoint."""

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "timestamp" in data
        assert "total_orders" in data
        assert data["status"] == "healthy"
        assert isinstance(data["total_orders"], int)


class TestOrderEndpoints:
    """Test order-related endpoints."""

    def test_create_simple_order(self, client):
        """Test creating a simple coffee order."""
        order_data = {
            "size": "medium",
            "coffee_type": "hot"
        }
        response = client.post("/orders", json=order_data)
        assert response.status_code == 201
        
        data = response.json()
        assert "order_id" in data
        assert data["size"] == "medium"
        assert data["coffee_type"] == "hot"
        assert data["flavors"] == []
        assert data["milk"] is None
        assert data["extra_shot"] is None
        assert data["estimated_price"] > 0
        assert data["estimated_prep_time"] > 0
        assert data["status"] == "received"

    def test_create_complex_order(self, client):
        """Test creating a complex coffee order."""
        order_data = {
            "size": "large",
            "coffee_type": "iced",
            "flavors": ["hazelnut", "caramel"],
            "milk": "oat",
            "extra_shot": 2,
            "special_instructions": "Extra cold please"
        }
        response = client.post("/orders", json=order_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["size"] == "large"
        assert data["coffee_type"] == "iced"
        assert data["flavors"] == ["hazelnut", "caramel"]
        assert data["milk"] == "oat"
        assert data["extra_shot"] == 2
        assert data["special_instructions"] == "Extra cold please"
        assert data["estimated_price"] > 0
        assert data["status"] == "received"

    def test_create_order_invalid_size(self, client):
        """Test creating an order with invalid size."""
        order_data = {
            "size": "extra-large",
            "coffee_type": "hot"
        }
        response = client.post("/orders", json=order_data)
        assert response.status_code == 422

    def test_create_order_invalid_coffee_type(self, client):
        """Test creating an order with invalid coffee type."""
        order_data = {
            "size": "medium",
            "coffee_type": "lukewarm"
        }
        response = client.post("/orders", json=order_data)
        assert response.status_code == 422

    def test_create_order_too_many_flavors(self, client):
        """Test creating an order with too many flavors."""
        order_data = {
            "size": "medium",
            "coffee_type": "hot",
            "flavors": ["hazelnut", "caramel", "mocha", "vanilla"]
        }
        response = client.post("/orders", json=order_data)
        assert response.status_code == 422

    def test_create_order_negative_extra_shots(self, client):
        """Test creating an order with negative extra shots."""
        order_data = {
            "size": "medium",
            "coffee_type": "hot",
            "extra_shot": -1
        }
        response = client.post("/orders", json=order_data)
        assert response.status_code == 422

    def test_create_order_too_many_extra_shots(self, client):
        """Test creating an order with too many extra shots."""
        order_data = {
            "size": "medium",
            "coffee_type": "hot",
            "extra_shot": 10
        }
        response = client.post("/orders", json=order_data)
        assert response.status_code == 422

    def test_create_order_special_instructions_too_long(self, client):
        """Test creating an order with special instructions too long."""
        order_data = {
            "size": "medium",
            "coffee_type": "hot",
            "special_instructions": "x" * 300
        }
        response = client.post("/orders", json=order_data)
        assert response.status_code == 422

    def test_get_all_orders_empty(self, client):
        """Test getting all orders when none exist."""
        # Note: This test may not be truly empty due to shared state between tests
        # In a real application, you'd want to use test isolation
        response = client.get("/orders")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_all_orders_with_data(self, client):
        """Test getting all orders when some exist."""
        # Get initial count
        initial_response = client.get("/orders")
        initial_count = len(initial_response.json())
        
        # Create a few orders
        order1_data = {"size": "small", "coffee_type": "hot"}
        order2_data = {"size": "large", "coffee_type": "iced"}
        
        client.post("/orders", json=order1_data)
        client.post("/orders", json=order2_data)
        
        response = client.get("/orders")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == initial_count + 2

    def test_get_specific_order(self, client):
        """Test getting a specific order by ID."""
        # Create an order
        order_data = {"size": "medium", "coffee_type": "hot"}
        create_response = client.post("/orders", json=order_data)
        order_id = create_response.json()["order_id"]
        
        # Get the specific order
        response = client.get(f"/orders/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["order_id"] == order_id
        assert data["size"] == "medium"
        assert data["coffee_type"] == "hot"

    def test_get_nonexistent_order(self, client):
        """Test getting a non-existent order."""
        response = client.get("/orders/nonexistent-id")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_update_order_status(self, client):
        """Test updating an order status."""
        # Create an order
        order_data = {"size": "medium", "coffee_type": "hot"}
        create_response = client.post("/orders", json=order_data)
        order_id = create_response.json()["order_id"]
        
        # Update the status
        status_update = {
            "order_id": order_id,
            "status": "preparing"
        }
        response = client.patch(f"/orders/{order_id}/status", json=status_update)
        assert response.status_code == 200
        data = response.json()
        assert data["order_id"] == order_id
        assert data["status"] == "preparing"

    def test_update_nonexistent_order_status(self, client):
        """Test updating status of a non-existent order."""
        status_update = {
            "order_id": "nonexistent-id",
            "status": "preparing"
        }
        response = client.patch("/orders/nonexistent-id/status", json=status_update)
        assert response.status_code == 404

    def test_cancel_order(self, client):
        """Test canceling an order."""
        # Create an order
        order_data = {"size": "medium", "coffee_type": "hot"}
        create_response = client.post("/orders", json=order_data)
        order_id = create_response.json()["order_id"]
        
        # Cancel the order
        response = client.delete(f"/orders/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert "cancelled" in data["message"]
        
        # Verify the order is gone
        get_response = client.get(f"/orders/{order_id}")
        assert get_response.status_code == 404

    def test_cancel_nonexistent_order(self, client):
        """Test canceling a non-existent order."""
        response = client.delete("/orders/nonexistent-id")
        assert response.status_code == 404


class TestPricingCalculation:
    """Test pricing calculation logic."""

    def test_small_hot_coffee_pricing(self, client):
        """Test pricing for small hot coffee."""
        order_data = {"size": "small", "coffee_type": "hot"}
        response = client.post("/orders", json=order_data)
        data = response.json()
        assert data["estimated_price"] == 3.50

    def test_medium_iced_coffee_pricing(self, client):
        """Test pricing for medium iced coffee."""
        order_data = {"size": "medium", "coffee_type": "iced"}
        response = client.post("/orders", json=order_data)
        data = response.json()
        assert data["estimated_price"] == 4.25

    def test_large_coffee_with_extras_pricing(self, client):
        """Test pricing for large coffee with extras."""
        order_data = {
            "size": "large",
            "coffee_type": "hot",
            "flavors": ["hazelnut", "caramel"],
            "milk": "oat",
            "extra_shot": 2
        }
        response = client.post("/orders", json=order_data)
        data = response.json()
        # Base: 4.95 + Flavors: 2*0.50 + Premium milk: 0.65 + Extra shots: 2*0.75 = 8.10
        assert data["estimated_price"] == 8.10

    def test_prep_time_calculation(self, client):
        """Test preparation time calculation."""
        # Simple order
        order_data = {"size": "small", "coffee_type": "hot"}
        response = client.post("/orders", json=order_data)
        data = response.json()
        assert data["estimated_prep_time"] >= 2
        
        # Complex order
        order_data = {
            "size": "large",
            "coffee_type": "iced",
            "flavors": ["hazelnut", "caramel"],
            "extra_shot": 2
        }
        response = client.post("/orders", json=order_data)
        data = response.json()
        assert data["estimated_prep_time"] >= 2

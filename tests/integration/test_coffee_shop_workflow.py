"""
Integration tests for complete coffee shop workflows.
"""

import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
class TestCoffeeShopWorkflow:
    """Test complete coffee shop workflows."""

    async def test_complete_order_workflow(self, async_client: AsyncClient):
        """Test a complete order workflow from creation to completion."""
        # 1. Check API health
        response = await async_client.get("/health")
        assert response.status_code == 200
        health_data = response.json()
        assert health_data["status"] == "healthy"
        initial_order_count = health_data["total_orders"]

        # 2. Get menu
        response = await async_client.get("/menu")
        assert response.status_code == 200
        menu_data = response.json()
        assert "sizes" in menu_data
        assert "coffee_types" in menu_data

        # 3. Create a complex order
        order_data = {
            "size": "large",
            "coffee_type": "iced",
            "flavors": ["hazelnut", "caramel"],
            "milk": "oat",
            "extra_shot": 2,
            "special_instructions": "Extra cold, light ice"
        }
        response = await async_client.post("/orders", json=order_data)
        assert response.status_code == 201
        order_response = response.json()
        order_id = order_response["order_id"]

        # Verify order details
        assert order_response["size"] == "large"
        assert order_response["coffee_type"] == "iced"
        assert order_response["flavors"] == ["hazelnut", "caramel"]
        assert order_response["milk"] == "oat"
        assert order_response["extra_shot"] == 2
        assert order_response["special_instructions"] == "Extra cold, light ice"
        assert order_response["status"] == "received"
        assert order_response["estimated_price"] > 0
        assert order_response["estimated_prep_time"] > 0

        # 4. Get the specific order
        response = await async_client.get(f"/orders/{order_id}")
        assert response.status_code == 200
        retrieved_order = response.json()
        assert retrieved_order["order_id"] == order_id
        assert retrieved_order["status"] == "received"

        # 5. Update order status to preparing
        status_update = {
            "order_id": order_id,
            "status": "preparing"
        }
        response = await async_client.patch(f"/orders/{order_id}/status", json=status_update)
        assert response.status_code == 200
        status_response = response.json()
        assert status_response["order_id"] == order_id
        assert status_response["status"] == "preparing"

        # 6. Update order status to ready
        status_update = {
            "order_id": order_id,
            "status": "ready"
        }
        response = await async_client.patch(f"/orders/{order_id}/status", json=status_update)
        assert response.status_code == 200
        status_response = response.json()
        assert status_response["status"] == "ready"

        # 7. Update order status to completed
        status_update = {
            "order_id": order_id,
            "status": "completed"
        }
        response = await async_client.patch(f"/orders/{order_id}/status", json=status_update)
        assert response.status_code == 200
        status_response = response.json()
        assert status_response["status"] == "completed"

        # 8. Verify order count increased
        response = await async_client.get("/health")
        assert response.status_code == 200
        health_data = response.json()
        assert health_data["total_orders"] == initial_order_count + 1

        # 9. Get all orders and verify our order is there
        response = await async_client.get("/orders")
        assert response.status_code == 200
        all_orders = response.json()
        assert len(all_orders) >= 1
        our_order = next((order for order in all_orders if order["order_id"] == order_id), None)
        assert our_order is not None
        assert our_order["status"] == "completed"

    async def test_multiple_orders_workflow(self, async_client: AsyncClient):
        """Test creating and managing multiple orders."""
        # Create multiple orders
        orders = []
        order_configs = [
            {"size": "small", "coffee_type": "hot"},
            {"size": "medium", "coffee_type": "iced", "flavors": ["vanilla"]},
            {"size": "large", "coffee_type": "hot", "milk": "almond", "extra_shot": 1}
        ]

        for config in order_configs:
            response = await async_client.post("/orders", json=config)
            assert response.status_code == 201
            order_data = response.json()
            orders.append(order_data)

        # Verify all orders were created
        assert len(orders) == 3
        for order in orders:
            assert "order_id" in order
            assert order["status"] == "received"

        # Get all orders
        response = await async_client.get("/orders")
        assert response.status_code == 200
        all_orders = response.json()
        assert len(all_orders) >= 3

        # Update different orders to different statuses
        statuses = ["preparing", "ready", "completed"]
        for i, order in enumerate(orders):
            status_update = {
                "order_id": order["order_id"],
                "status": statuses[i]
            }
            response = await async_client.patch(f"/orders/{order['order_id']}/status", json=status_update)
            assert response.status_code == 200

        # Verify status updates
        for i, order in enumerate(orders):
            response = await async_client.get(f"/orders/{order['order_id']}")
            assert response.status_code == 200
            updated_order = response.json()
            assert updated_order["status"] == statuses[i]

    async def test_order_cancellation_workflow(self, async_client: AsyncClient):
        """Test order cancellation workflow."""
        # Create an order
        order_data = {
            "size": "medium",
            "coffee_type": "hot",
            "flavors": ["hazelnut"],
            "special_instructions": "Cancel this order"
        }
        response = await async_client.post("/orders", json=order_data)
        assert response.status_code == 201
        order_response = response.json()
        order_id = order_response["order_id"]

        # Verify order exists
        response = await async_client.get(f"/orders/{order_id}")
        assert response.status_code == 200

        # Cancel the order
        response = await async_client.delete(f"/orders/{order_id}")
        assert response.status_code == 200
        cancel_response = response.json()
        assert "cancelled" in cancel_response["message"]

        # Verify order no longer exists
        response = await async_client.get(f"/orders/{order_id}")
        assert response.status_code == 404

    async def test_error_handling_workflow(self, async_client: AsyncClient):
        """Test error handling in various scenarios."""
        # Test invalid order creation
        invalid_orders = [
            {"size": "extra-large", "coffee_type": "hot"},  # Invalid size
            {"size": "medium", "coffee_type": "lukewarm"},  # Invalid type
            {"size": "small", "coffee_type": "hot", "flavors": ["hazelnut", "vanilla", "caramel", "mocha"]},  # Too many flavors
            {"size": "medium", "coffee_type": "iced", "extra_shot": -1},  # Negative extra shots
        ]

        for invalid_order in invalid_orders:
            response = await async_client.post("/orders", json=invalid_order)
            assert response.status_code == 422

        # Test operations on non-existent order
        fake_order_id = "non-existent-order-id"
        
        # Get non-existent order
        response = await async_client.get(f"/orders/{fake_order_id}")
        assert response.status_code == 404

        # Update status of non-existent order
        status_update = {"order_id": fake_order_id, "status": "preparing"}
        response = await async_client.patch(f"/orders/{fake_order_id}/status", json=status_update)
        assert response.status_code == 404

        # Cancel non-existent order
        response = await async_client.delete(f"/orders/{fake_order_id}")
        assert response.status_code == 404

    async def test_pricing_consistency_workflow(self, async_client: AsyncClient):
        """Test that pricing is consistent across similar orders."""
        # Create identical orders and verify pricing is the same
        order_data = {
            "size": "large",
            "coffee_type": "iced",
            "flavors": ["hazelnut", "caramel"],
            "milk": "oat",
            "extra_shot": 1
        }

        prices = []
        for _ in range(3):
            response = await async_client.post("/orders", json=order_data)
            assert response.status_code == 201
            order_response = response.json()
            prices.append(order_response["estimated_price"])

        # All prices should be identical
        assert all(price == prices[0] for price in prices)
        assert prices[0] > 0

    async def test_preparation_time_consistency_workflow(self, async_client: AsyncClient):
        """Test that preparation time is consistent for similar orders."""
        # Create identical orders and verify prep time is the same
        order_data = {
            "size": "medium",
            "coffee_type": "hot",
            "flavors": ["vanilla"],
            "extra_shot": 2
        }

        prep_times = []
        for _ in range(3):
            response = await async_client.post("/orders", json=order_data)
            assert response.status_code == 201
            order_response = response.json()
            prep_times.append(order_response["estimated_prep_time"])

        # All prep times should be identical
        assert all(time == prep_times[0] for time in prep_times)
        assert prep_times[0] >= 2

    async def test_complete_api_coverage_workflow(self, async_client: AsyncClient):
        """Test that all API endpoints are accessible and functional."""
        # Test all GET endpoints
        endpoints = ["/", "/health", "/menu", "/orders"]
        for endpoint in endpoints:
            response = await async_client.get(endpoint)
            assert response.status_code == 200

        # Test POST endpoint
        order_data = {"size": "small", "coffee_type": "hot"}
        response = await async_client.post("/orders", json=order_data)
        assert response.status_code == 201
        order_id = response.json()["order_id"]

        # Test PATCH endpoint
        status_update = {"order_id": order_id, "status": "preparing"}
        response = await async_client.patch(f"/orders/{order_id}/status", json=status_update)
        assert response.status_code == 200

        # Test DELETE endpoint
        response = await async_client.delete(f"/orders/{order_id}")
        assert response.status_code == 200

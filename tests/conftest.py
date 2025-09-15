"""
Pytest configuration and shared fixtures for Coffee Shop API tests.
"""

import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app
from models import CoffeeOrder, SizeEnum, CoffeeTypeEnum, FlavorEnum, MilkTypeEnum


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client():
    """Create an async test client for the FastAPI app."""
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_coffee_order():
    """Sample coffee order for testing."""
    return CoffeeOrder(
        size=SizeEnum.MEDIUM,
        coffee_type=CoffeeTypeEnum.HOT,
        flavors=[FlavorEnum.HAZELNUT],
        milk=MilkTypeEnum.OAT,
        extra_shot=1,
        special_instructions="Extra hot please"
    )


@pytest.fixture
def simple_coffee_order():
    """Simple coffee order for testing (minimal fields)."""
    return CoffeeOrder(
        size=SizeEnum.SMALL,
        coffee_type=CoffeeTypeEnum.ICED
    )


@pytest.fixture
def invalid_coffee_order():
    """Invalid coffee order for testing validation."""
    return {
        "size": "extra-large",  # Invalid size
        "coffee_type": "lukewarm",  # Invalid type
        "flavors": ["hazelnut", "vanilla", "caramel", "mocha", "cinnamon"],  # Too many flavors
        "extra_shot": -1,  # Invalid negative value
        "special_instructions": "x" * 300  # Too long
    }


@pytest.fixture
def valid_order_data():
    """Valid order data as dictionary."""
    return {
        "size": "large",
        "coffee_type": "iced",
        "flavors": ["hazelnut", "caramel"],
        "milk": "oat",
        "extra_shot": 2,
        "special_instructions": "Light ice"
    }


@pytest.fixture
def menu_data():
    """Expected menu data structure."""
    return {
        "sizes": ["small", "medium", "large"],
        "coffee_types": ["iced", "hot"],
        "flavors": ["french vanilla", "hazelnut", "caramel", "mocha", "vanilla", "cinnamon"],
        "milk_types": ["whole", "oat", "almond", "soy", "none"],
        "max_extra_shots": 5,
        "max_flavors": 3
    }

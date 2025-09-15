"""
Test data fixtures for Coffee Shop API tests.
"""

from models import CoffeeOrder, SizeEnum, CoffeeTypeEnum, FlavorEnum, MilkTypeEnum


# Sample order data for testing
SAMPLE_ORDERS = {
    "simple_hot": {
        "size": "small",
        "coffee_type": "hot"
    },
    "simple_iced": {
        "size": "medium",
        "coffee_type": "iced"
    },
    "complex_order": {
        "size": "large",
        "coffee_type": "iced",
        "flavors": ["hazelnut", "caramel"],
        "milk": "oat",
        "extra_shot": 2,
        "special_instructions": "Extra cold, light ice"
    },
    "max_flavors": {
        "size": "medium",
        "coffee_type": "hot",
        "flavors": ["french vanilla", "hazelnut", "caramel"]
    },
    "max_extra_shots": {
        "size": "large",
        "coffee_type": "hot",
        "extra_shot": 5
    },
    "premium_milk": {
        "size": "medium",
        "coffee_type": "iced",
        "milk": "almond"
    },
    "all_options": {
        "size": "large",
        "coffee_type": "iced",
        "flavors": ["mocha", "vanilla"],
        "milk": "soy",
        "extra_shot": 3,
        "special_instructions": "Extra hot, no foam, decaf"
    }
}

# Invalid order data for testing validation
INVALID_ORDERS = {
    "invalid_size": {
        "size": "extra-large",
        "coffee_type": "hot"
    },
    "invalid_coffee_type": {
        "size": "medium",
        "coffee_type": "lukewarm"
    },
    "invalid_flavor": {
        "size": "small",
        "coffee_type": "hot",
        "flavors": ["chocolate-chip"]
    },
    "too_many_flavors": {
        "size": "medium",
        "coffee_type": "hot",
        "flavors": ["hazelnut", "caramel", "mocha", "vanilla"]
    },
    "negative_extra_shots": {
        "size": "large",
        "coffee_type": "iced",
        "extra_shot": -1
    },
    "too_many_extra_shots": {
        "size": "medium",
        "coffee_type": "hot",
        "extra_shot": 10
    },
    "special_instructions_too_long": {
        "size": "small",
        "coffee_type": "hot",
        "special_instructions": "x" * 300
    },
    "invalid_milk": {
        "size": "medium",
        "coffee_type": "iced",
        "milk": "coconut"
    }
}

# Expected pricing for different order configurations
EXPECTED_PRICING = {
    "small_hot": 3.50,
    "medium_hot": 4.25,
    "large_hot": 4.95,
    "small_iced": 3.50,
    "medium_iced": 4.25,
    "large_iced": 4.95,
    "with_flavor": 0.50,  # Per flavor
    "with_premium_milk": 0.65,  # For oat, almond, soy
    "with_extra_shot": 0.75,  # Per extra shot
}

# Expected preparation times (minimum values)
EXPECTED_PREP_TIMES = {
    "base_time": 3,
    "iced_bonus": 1,
    "extra_shot_time": 0.5,  # Per extra shot
    "multiple_flavors_bonus": 1,
    "minimum_time": 2
}

# Order status progression
ORDER_STATUSES = ["received", "preparing", "ready", "completed"]

# Menu data for validation
EXPECTED_MENU = {
    "sizes": ["small", "medium", "large"],
    "coffee_types": ["iced", "hot"],
    "flavors": ["french vanilla", "hazelnut", "caramel", "mocha", "vanilla", "cinnamon"],
    "milk_types": ["whole", "oat", "almond", "soy", "none"],
    "max_extra_shots": 5,
    "max_flavors": 3
}


def create_test_order(order_type: str) -> CoffeeOrder:
    """Create a test order from predefined data."""
    if order_type not in SAMPLE_ORDERS:
        raise ValueError(f"Unknown order type: {order_type}")
    
    order_data = SAMPLE_ORDERS[order_type]
    return CoffeeOrder(**order_data)


def get_invalid_order_data(order_type: str) -> dict:
    """Get invalid order data for testing validation."""
    if order_type not in INVALID_ORDERS:
        raise ValueError(f"Unknown invalid order type: {order_type}")
    
    return INVALID_ORDERS[order_type]


def calculate_expected_price(order_data: dict) -> float:
    """Calculate expected price for an order."""
    base_prices = {
        "small": 3.50,
        "medium": 4.25,
        "large": 4.95
    }
    
    price = base_prices.get(order_data["size"], 0)
    
    # Add flavor costs
    if "flavors" in order_data:
        price += len(order_data["flavors"]) * 0.50
    
    # Add premium milk cost
    if "milk" in order_data and order_data["milk"] in ["oat", "almond", "soy"]:
        price += 0.65
    
    # Add extra shot costs
    if "extra_shot" in order_data and order_data["extra_shot"]:
        price += order_data["extra_shot"] * 0.75
    
    return round(price, 2)


def calculate_expected_prep_time(order_data: dict) -> int:
    """Calculate expected preparation time for an order."""
    base_time = 3
    
    # Add time for iced coffee
    if order_data.get("coffee_type") == "iced":
        base_time += 1
    
    # Add time for extra shots
    if "extra_shot" in order_data and order_data["extra_shot"]:
        base_time += order_data["extra_shot"] * 0.5
    
    # Add time for multiple flavors
    if "flavors" in order_data and len(order_data["flavors"]) > 1:
        base_time += 1
    
    return max(2, int(base_time))

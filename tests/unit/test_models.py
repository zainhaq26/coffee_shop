"""
Unit tests for Pydantic models and validation.
"""

import pytest
from pydantic import ValidationError
from models import (
    CoffeeOrder, CoffeeOrderResponse, OrderStatus, MenuResponse,
    SizeEnum, CoffeeTypeEnum, FlavorEnum, MilkTypeEnum
)


class TestCoffeeOrder:
    """Test CoffeeOrder model validation."""

    def test_valid_coffee_order(self, sample_coffee_order):
        """Test creating a valid coffee order."""
        assert sample_coffee_order.size == SizeEnum.MEDIUM
        assert sample_coffee_order.coffee_type == CoffeeTypeEnum.HOT
        assert sample_coffee_order.flavors == [FlavorEnum.HAZELNUT]
        assert sample_coffee_order.milk == MilkTypeEnum.OAT
        assert sample_coffee_order.extra_shot == 1
        assert sample_coffee_order.special_instructions == "Extra hot please"

    def test_minimal_coffee_order(self, simple_coffee_order):
        """Test creating a minimal coffee order with only required fields."""
        assert simple_coffee_order.size == SizeEnum.SMALL
        assert simple_coffee_order.coffee_type == CoffeeTypeEnum.ICED
        assert simple_coffee_order.flavors == []
        assert simple_coffee_order.milk is None
        assert simple_coffee_order.extra_shot is None
        assert simple_coffee_order.special_instructions is None

    def test_invalid_size(self):
        """Test validation with invalid size."""
        with pytest.raises(ValidationError) as exc_info:
            CoffeeOrder(
                size="extra-large",
                coffee_type=CoffeeTypeEnum.HOT
            )
        assert "Input should be 'small', 'medium' or 'large'" in str(exc_info.value)

    def test_invalid_coffee_type(self):
        """Test validation with invalid coffee type."""
        with pytest.raises(ValidationError) as exc_info:
            CoffeeOrder(
                size=SizeEnum.MEDIUM,
                coffee_type="lukewarm"
            )
        assert "Input should be 'iced' or 'hot'" in str(exc_info.value)

    def test_invalid_flavor(self):
        """Test validation with invalid flavor."""
        with pytest.raises(ValidationError) as exc_info:
            CoffeeOrder(
                size=SizeEnum.MEDIUM,
                coffee_type=CoffeeTypeEnum.HOT,
                flavors=["chocolate-chip"]
            )
        assert "Input should be" in str(exc_info.value)

    def test_too_many_flavors(self):
        """Test validation with too many flavors."""
        with pytest.raises(ValidationError) as exc_info:
            CoffeeOrder(
                size=SizeEnum.MEDIUM,
                coffee_type=CoffeeTypeEnum.HOT,
                flavors=[
                    FlavorEnum.HAZELNUT,
                    FlavorEnum.CARAMEL,
                    FlavorEnum.MOCHA,
                    FlavorEnum.VANILLA
                ]
            )
        assert "Maximum 3 flavors allowed per coffee" in str(exc_info.value)

    def test_negative_extra_shots(self):
        """Test validation with negative extra shots."""
        with pytest.raises(ValidationError) as exc_info:
            CoffeeOrder(
                size=SizeEnum.MEDIUM,
                coffee_type=CoffeeTypeEnum.HOT,
                extra_shot=-1
            )
        assert "Input should be greater than or equal to 0" in str(exc_info.value)

    def test_too_many_extra_shots(self):
        """Test validation with too many extra shots."""
        with pytest.raises(ValidationError) as exc_info:
            CoffeeOrder(
                size=SizeEnum.MEDIUM,
                coffee_type=CoffeeTypeEnum.HOT,
                extra_shot=10
            )
        assert "Input should be less than or equal to 5" in str(exc_info.value)

    def test_special_instructions_too_long(self):
        """Test validation with special instructions too long."""
        with pytest.raises(ValidationError) as exc_info:
            CoffeeOrder(
                size=SizeEnum.MEDIUM,
                coffee_type=CoffeeTypeEnum.HOT,
                special_instructions="x" * 300
            )
        assert "String should have at most 200 characters" in str(exc_info.value)

    def test_valid_boundary_values(self):
        """Test valid boundary values."""
        # Maximum flavors
        order = CoffeeOrder(
            size=SizeEnum.LARGE,
            coffee_type=CoffeeTypeEnum.ICED,
            flavors=[FlavorEnum.HAZELNUT, FlavorEnum.CARAMEL, FlavorEnum.MOCHA]
        )
        assert len(order.flavors) == 3

        # Maximum extra shots
        order = CoffeeOrder(
            size=SizeEnum.MEDIUM,
            coffee_type=CoffeeTypeEnum.HOT,
            extra_shot=5
        )
        assert order.extra_shot == 5

        # Maximum special instructions length
        long_instructions = "x" * 200
        order = CoffeeOrder(
            size=SizeEnum.SMALL,
            coffee_type=CoffeeTypeEnum.HOT,
            special_instructions=long_instructions
        )
        assert len(order.special_instructions) == 200


class TestEnums:
    """Test enum values."""

    def test_size_enum_values(self):
        """Test SizeEnum values."""
        assert SizeEnum.SMALL == "small"
        assert SizeEnum.MEDIUM == "medium"
        assert SizeEnum.LARGE == "large"

    def test_coffee_type_enum_values(self):
        """Test CoffeeTypeEnum values."""
        assert CoffeeTypeEnum.ICED == "iced"
        assert CoffeeTypeEnum.HOT == "hot"

    def test_flavor_enum_values(self):
        """Test FlavorEnum values."""
        assert FlavorEnum.FRENCH_VANILLA == "french vanilla"
        assert FlavorEnum.HAZELNUT == "hazelnut"
        assert FlavorEnum.CARAMEL == "caramel"
        assert FlavorEnum.MOCHA == "mocha"
        assert FlavorEnum.VANILLA == "vanilla"
        assert FlavorEnum.CINNAMON == "cinnamon"

    def test_milk_type_enum_values(self):
        """Test MilkTypeEnum values."""
        assert MilkTypeEnum.WHOLE == "whole"
        assert MilkTypeEnum.OAT == "oat"
        assert MilkTypeEnum.ALMOND == "almond"
        assert MilkTypeEnum.SOY == "soy"
        assert MilkTypeEnum.NONE == "none"


class TestMenuResponse:
    """Test MenuResponse model."""

    def test_menu_response_creation(self):
        """Test creating a MenuResponse."""
        menu = MenuResponse(
            sizes=["small", "medium", "large"],
            coffee_types=["iced", "hot"],
            flavors=["hazelnut", "caramel"],
            milk_types=["whole", "oat"]
        )
        assert menu.sizes == ["small", "medium", "large"]
        assert menu.coffee_types == ["iced", "hot"]
        assert menu.flavors == ["hazelnut", "caramel"]
        assert menu.milk_types == ["whole", "oat"]
        assert menu.max_extra_shots == 5
        assert menu.max_flavors == 3


class TestOrderStatus:
    """Test OrderStatus model."""

    def test_order_status_creation(self):
        """Test creating an OrderStatus."""
        status = OrderStatus(
            order_id="test-123",
            status="preparing"
        )
        assert status.order_id == "test-123"
        assert status.status == "preparing"
        assert status.estimated_ready_time is None

    def test_invalid_order_status(self):
        """Test validation with invalid order status."""
        with pytest.raises(ValidationError) as exc_info:
            OrderStatus(
                order_id="test-123",
                status="invalid-status"
            )
        assert "Input should be 'received', 'preparing', 'ready' or 'completed'" in str(exc_info.value)


class TestModelSerialization:
    """Test model serialization and deserialization."""

    def test_coffee_order_json_serialization(self, sample_coffee_order):
        """Test CoffeeOrder JSON serialization."""
        json_data = sample_coffee_order.model_dump()
        assert json_data["size"] == "medium"
        assert json_data["coffee_type"] == "hot"
        assert json_data["flavors"] == ["hazelnut"]
        assert json_data["milk"] == "oat"
        assert json_data["extra_shot"] == 1

    def test_coffee_order_json_deserialization(self):
        """Test CoffeeOrder JSON deserialization."""
        json_data = {
            "size": "large",
            "coffee_type": "iced",
            "flavors": ["caramel", "mocha"],
            "milk": "almond",
            "extra_shot": 2,
            "special_instructions": "Extra cold"
        }
        order = CoffeeOrder.model_validate(json_data)
        assert order.size == SizeEnum.LARGE
        assert order.coffee_type == CoffeeTypeEnum.ICED
        assert order.flavors == [FlavorEnum.CARAMEL, FlavorEnum.MOCHA]
        assert order.milk == MilkTypeEnum.ALMOND
        assert order.extra_shot == 2
        assert order.special_instructions == "Extra cold"

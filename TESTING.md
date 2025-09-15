# Coffee Shop API Testing Guide

This document provides comprehensive information about testing the Coffee Shop API.

## 🧪 Test Structure

```
tests/
├── conftest.py                    # Shared fixtures and configuration
├── unit/                          # Unit tests
│   ├── test_models.py            # Pydantic model tests
│   └── test_api.py               # FastAPI endpoint tests
├── integration/                   # Integration tests
│   └── test_coffee_shop_workflow.py  # Complete workflow tests
└── fixtures/                      # Test data and utilities
    └── test_data.py              # Sample data and helper functions
```

## 🚀 Running Tests

### Quick Start
```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration

# Run with coverage
make test-coverage
```

### Using the Test Runner
```bash
# Run all tests
python run_tests.py

# Run unit tests only
python run_tests.py --type unit

# Run integration tests only
python run_tests.py --type integration

# Run with coverage report
python run_tests.py --type coverage

# Run in verbose mode
python run_tests.py --verbose

# Skip slow tests
python run_tests.py --fast
```

### Using pytest directly
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_models.py

# Run tests with markers
uv run pytest -m unit
uv run pytest -m integration

# Run with coverage
uv run pytest --cov=main --cov=models --cov-report=html
```

## 📋 Test Categories

### Unit Tests (`tests/unit/`)

#### Model Tests (`test_models.py`)
- **Purpose**: Test Pydantic model validation and serialization
- **Coverage**:
  - Valid order creation
  - Invalid input validation
  - Enum value validation
  - Boundary value testing
  - JSON serialization/deserialization

#### API Tests (`test_api.py`)
- **Purpose**: Test individual FastAPI endpoints
- **Coverage**:
  - All HTTP endpoints (GET, POST, PATCH, DELETE)
  - Request/response validation
  - Error handling
  - Status codes
  - Pricing calculation
  - Preparation time calculation

### Integration Tests (`tests/integration/`)

#### Workflow Tests (`test_coffee_shop_workflow.py`)
- **Purpose**: Test complete user workflows
- **Coverage**:
  - Complete order lifecycle (create → prepare → ready → complete)
  - Multiple order management
  - Order cancellation workflow
  - Error handling scenarios
  - Pricing consistency
  - API endpoint coverage

## 🔧 Test Configuration

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --color=yes
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    api: API endpoint tests
    model: Model validation tests
asyncio_mode = auto
```

### Test Fixtures (`conftest.py`)
- **client**: Synchronous test client
- **async_client**: Asynchronous test client
- **sample_coffee_order**: Complex order example
- **simple_coffee_order**: Minimal order example
- **invalid_coffee_order**: Invalid order for testing
- **valid_order_data**: Valid order as dictionary
- **menu_data**: Expected menu structure

## 📊 Test Data

### Sample Orders (`fixtures/test_data.py`)
```python
SAMPLE_ORDERS = {
    "simple_hot": {"size": "small", "coffee_type": "hot"},
    "complex_order": {
        "size": "large",
        "coffee_type": "iced",
        "flavors": ["hazelnut", "caramel"],
        "milk": "oat",
        "extra_shot": 2,
        "special_instructions": "Extra cold, light ice"
    }
}
```

### Invalid Orders
```python
INVALID_ORDERS = {
    "invalid_size": {"size": "extra-large", "coffee_type": "hot"},
    "too_many_flavors": {
        "size": "medium",
        "coffee_type": "hot",
        "flavors": ["hazelnut", "caramel", "mocha", "vanilla"]
    }
}
```

## 🎯 Test Coverage

### Model Validation Tests
- ✅ Valid order creation
- ✅ Invalid size validation
- ✅ Invalid coffee type validation
- ✅ Invalid flavor validation
- ✅ Too many flavors validation
- ✅ Negative extra shots validation
- ✅ Too many extra shots validation
- ✅ Special instructions length validation
- ✅ Boundary value testing
- ✅ JSON serialization/deserialization

### API Endpoint Tests
- ✅ Root endpoint (`/`)
- ✅ Health check (`/health`)
- ✅ Menu endpoint (`/menu`)
- ✅ Create order (`POST /orders`)
- ✅ Get all orders (`GET /orders`)
- ✅ Get specific order (`GET /orders/{id}`)
- ✅ Update order status (`PATCH /orders/{id}/status`)
- ✅ Cancel order (`DELETE /orders/{id}`)
- ✅ Error handling (404, 422)
- ✅ Pricing calculation
- ✅ Preparation time calculation

### Integration Workflow Tests
- ✅ Complete order lifecycle
- ✅ Multiple order management
- ✅ Order cancellation
- ✅ Error handling scenarios
- ✅ Pricing consistency
- ✅ Preparation time consistency
- ✅ API endpoint coverage

## 🚨 Test Scenarios

### Happy Path Tests
1. **Simple Order Creation**
   - Create order with minimal data
   - Verify order details
   - Check pricing and prep time

2. **Complex Order Creation**
   - Create order with all options
   - Verify all fields are correct
   - Check pricing calculation

3. **Order Status Updates**
   - Create order
   - Update status through lifecycle
   - Verify status changes

### Error Handling Tests
1. **Validation Errors**
   - Invalid enum values
   - Boundary violations
   - Required field missing

2. **Business Logic Errors**
   - Too many flavors
   - Negative extra shots
   - Special instructions too long

3. **API Errors**
   - Non-existent order operations
   - Invalid request formats
   - Server errors

### Edge Cases
1. **Boundary Values**
   - Maximum flavors (3)
   - Maximum extra shots (5)
   - Maximum special instructions (200 chars)

2. **Empty/Minimal Data**
   - Orders with only required fields
   - Empty flavor lists
   - No special instructions

## 📈 Coverage Reports

### Generate Coverage Report
```bash
make test-coverage
```

### View HTML Coverage Report
```bash
open htmlcov/index.html
```

### Coverage Targets
- **Models**: 100% coverage
- **API Endpoints**: 100% coverage
- **Business Logic**: 100% coverage
- **Error Handling**: 100% coverage

## 🔍 Debugging Tests

### Verbose Output
```bash
python run_tests.py --verbose
```

### Run Specific Test
```bash
uv run pytest tests/unit/test_models.py::TestCoffeeOrder::test_valid_coffee_order -v
```

### Debug Mode
```bash
uv run pytest --pdb tests/unit/test_models.py
```

### Show Local Variables
```bash
uv run pytest --tb=long tests/unit/test_models.py
```

## 🚀 Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.13
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run tests
        run: uv run pytest
      - name: Generate coverage
        run: uv run pytest --cov=main --cov=models --cov-report=xml
```

## 📝 Writing New Tests

### Test Naming Convention
- **Files**: `test_*.py`
- **Classes**: `Test*`
- **Methods**: `test_*`

### Test Structure
```python
def test_feature_description():
    """Test description explaining what is being tested."""
    # Arrange
    # Act
    # Assert
```

### Async Tests
```python
@pytest.mark.asyncio
async def test_async_feature():
    """Test async functionality."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/endpoint")
        assert response.status_code == 200
```

### Fixtures Usage
```python
def test_with_fixture(sample_coffee_order):
    """Test using a fixture."""
    assert sample_coffee_order.size == SizeEnum.MEDIUM
```

## 🎉 Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Names**: Test names should describe what is being tested
3. **Single Responsibility**: Each test should test one thing
4. **Arrange-Act-Assert**: Structure tests clearly
5. **Use Fixtures**: Reuse common test data
6. **Mock External Dependencies**: Keep tests fast and reliable
7. **Test Edge Cases**: Include boundary and error conditions
8. **Maintain Coverage**: Aim for high test coverage
9. **Document Tests**: Add docstrings to complex tests
10. **Regular Updates**: Keep tests in sync with code changes

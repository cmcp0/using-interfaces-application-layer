# Using Interfaces in Application Layer - Python Example

A practical example demonstrating how to use interfaces in the application layer to implement multiple variants of a use case while following Hexagonal Architecture and Domain-Driven Design (DDD) principles.

## 🎯 Purpose

This project demonstrates a real-world pattern where different business implementations (franchises) require different logic for the same use case. Using interfaces at the application layer allows us to:

- **Support multiple implementations** of the same use case for different franchises
- **Maintain clean separation** between business logic and implementation details
- **Enable dependency injection** for flexible and testable code
- **Follow the Open/Closed Principle** - open for extension, closed for modification
- **Isolate franchise-specific logic** while sharing common interfaces

## 📖 Use Case Example

The example implements a subscription verification system that works differently for two franchises:

- **Franchise 1**: Direct subscription verification using the Core API
- **Franchise 2**: Must first check subscription status with the Franchise API, then verify with the Core API

## 🏗️ Project Structure

```
src/app_services/users/
├── application/
│   ├── verify_subscription_interface.py      # Interface for subscription verification
│   ├── verify_subscription_franchise1.py     # Implementation for Franchise 1
│   └── verify_subscription_franchise2.py     # Implementation for Franchise 2
└── domain/
    ├── core_api_client.py                    # Interface for Core API operations
    └── franchise_api_client.py               # Interface for Franchise API operations
```

### 📂 `domain/`

Contains the interfaces (ports) for external services:
- `CoreApiClient`: Interface for core subscription operations
- `FranchiseApiClient`: Interface for franchise-specific operations

### 📂 `application/`

Contains the use case interface and its implementations:
- `VerifySubscriptionInterface`: The application-level interface defining the subscription verification contract
- `VerifySubscriptionFranchise1`: Implementation for Franchise 1
- `VerifySubscriptionFranchise2`: Implementation for Franchise 2 (with additional validation logic)

### 📂 `tests/`

Contains the tests for the application.

## 🏛️ Architectural Overview

This example demonstrates the power of **interfaces at the application layer** to handle varying business requirements:

### 1. **Domain Layer** (`domain/`)
Defines interfaces for external services that implementations will depend on:

```python
# CoreApiClient - Interface for core operations
class CoreApiClient(abc.ABC):
    @abc.abstractmethod
    def verify_subscription(self, subscription_id: UUID, metadata: dict) -> dict:
        pass

# FranchiseApiClient - Interface for franchise-specific operations
class FranchiseApiClient(abc.ABC):
    @abc.abstractmethod
    def get_user_subscription_info(self, subscription_external_id: str) -> dict:
        pass
```

### 2. **Application Layer** (`application/`)
Defines the use case interface and provides multiple implementations:

```python
# The application-level interface
class VerifySubscriptionInterface(abc.ABC):
    @abc.abstractmethod
    def verify(
        self, 
        metadata: dict, 
        subscription_id: Optional[UUID], 
        subscription_external_id: Optional[str]
    ) -> dict:
        pass
```

**Franchise 1 Implementation** (simple flow):
```python
class VerifySubscriptionFranchise1(VerifySubscriptionInterface):
    def __init__(self, core_api_client: CoreApiClient):
        self.core_api_client = core_api_client

    def verify(self, metadata: dict, subscription_id: Optional[UUID], 
               subscription_external_id: Optional[str]) -> dict:
        return self.core_api_client.verify_subscription(subscription_id, metadata)
```

**Franchise 2 Implementation** (complex flow with validation):
```python
class VerifySubscriptionFranchise2(VerifySubscriptionInterface):
    def __init__(self, core_api_client: CoreApiClient, 
                 franchise_api_client: FranchiseApiClient):
        self.franchise_api_client = franchise_api_client
        self.core_api_client = core_api_client

    def verify(self, metadata: dict, subscription_id: Optional[UUID], 
               subscription_external_id: Optional[str]) -> dict:
        # First, check with franchise API
        user_subscription_info = self.franchise_api_client.get_user_subscription_info(
            subscription_external_id
        )
        # Validate subscription status
        if user_subscription_info is None or user_subscription_info["status"] != "active":
            return {"status": "error", "message": "Invalid subscription"}
        # Then verify with core API
        subscription_id = user_subscription_info["id"]
        return self.core_api_client.verify_subscription(subscription_id, metadata)
```

### 3. **Infrastructure Layer** (`infrastructure/`)
Would implement the concrete adapters for `CoreApiClient` and `FranchiseApiClient` interfaces, connecting to actual APIs, databases, or external services.

## 🚀 Getting Started

1. Clone this repository:
```bash
git clone <repository-url>
cd using-interfaces-application-layer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements/dev.txt
```

## 📝 Usage

### Using the Interface Pattern

This project demonstrates how to use a factory or dependency injection to select the appropriate implementation:

```python
# Dependency injection based on franchise type
def get_subscription_verifier(franchise_type: str) -> VerifySubscriptionInterface:
    if franchise_type == "franchise1":
        core_client = CoreApiClientImpl()  # Your concrete implementation
        return VerifySubscriptionFranchise1(core_client)
    elif franchise_type == "franchise2":
        core_client = CoreApiClientImpl()  # Your concrete implementation
        franchise_client = FranchiseApiClientImpl()  # Your concrete implementation
        return VerifySubscriptionFranchise2(core_client, franchise_client)
    else:
        raise ValueError(f"Unknown franchise type: {franchise_type}")

# Usage
verifier = get_subscription_verifier("franchise2")
result = verifier.verify(
    metadata={"user_agent": "mobile"},
    subscription_id=None,
    subscription_external_id="ext_123456"
)
```

### Adding a New Franchise Implementation

1. Create a new class implementing `VerifySubscriptionInterface`:
   ```python
   class VerifySubscriptionFranchise3(VerifySubscriptionInterface):
       def verify(self, metadata, subscription_id, subscription_external_id) -> dict:
           # Your franchise-specific logic here
           pass
   ```

2. Inject the required dependencies in the constructor

3. Register it in your factory/dependency injection container

## 🧪 Testing

The interface pattern makes testing significantly easier:

```python
# Mock the domain interfaces for testing
class MockCoreApiClient(CoreApiClient):
    def verify_subscription(self, subscription_id: UUID, metadata: dict) -> dict:
        return {"status": "success", "verified": True}

# Test Franchise 1
def test_verify_subscription_franchise1():
    mock_client = MockCoreApiClient()
    verifier = VerifySubscriptionFranchise1(mock_client)
    result = verifier.verify(
        metadata={},
        subscription_id=UUID("12345678-1234-5678-1234-567812345678"),
        subscription_external_id=None
    )
    assert result["status"] == "success"
```

Run tests using:
```bash
pytest
```

## ✨ Benefits of This Pattern

1. **Flexibility**: Easily switch between implementations based on business rules (franchise type, feature flags, etc.)
2. **Testability**: Mock dependencies at the interface level for isolated unit tests
3. **Maintainability**: Each franchise implementation is isolated - changes to one don't affect others
4. **Scalability**: Adding a new franchise requires no changes to existing code (Open/Closed Principle)
5. **Clarity**: The interface clearly defines the contract that all implementations must follow
6. **Dependency Injection**: Enables IoC containers and makes the code more flexible

## 🎓 Key Concepts Demonstrated

- **Interface Segregation**: Each interface has a single, well-defined responsibility
- **Dependency Inversion**: High-level modules (application layer) depend on abstractions (interfaces), not concrete implementations
- **Strategy Pattern**: Different implementations of the same interface can be swapped at runtime
- **Hexagonal Architecture**: Clear separation between domain, application, and infrastructure concerns

## 📦 Project Dependencies

- **Development**: See `requirements/dev.txt`
- **Testing**: See `requirements/test.txt`
- **Production**: See `requirements/prod.txt`
- **Common**: See `requirements/common.txt`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 Additional Resources

- [Hexagonal Architecture (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design (Eric Evans)](https://domainlanguage.com/ddd/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Strategy Pattern](https://refactoring.guru/design-patterns/strategy)
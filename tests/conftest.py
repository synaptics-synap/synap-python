def pytest_collection_modifyitems(items):
    """Move marked integration tests to the end."""
    items.sort(key=lambda item: item.get_closest_marker("integration") is not None)

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )

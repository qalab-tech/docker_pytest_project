import pytest

def pytest_collection_modifyitems(config, items):
    slow_items = [item for item in items if "slow" in item.keywords]
    other_items = [item for item in items if "slow" not in item.keywords]

    # Clean the items list
    items.clear()

    # Get threads number
    num_workers = config.getoption("numprocesses")  # pytest-xdist передает значение в виде числа

    if num_workers is None:
        num_workers = 4  # Default value

    slow_items_per_worker = max(1, len(slow_items) // num_workers)

    # Add slow tests to every worker
    for i in range(num_workers):
        items.extend(slow_items[i * slow_items_per_worker:(i + 1) * slow_items_per_worker])

    # Add the remaining slow tests if they are not distributed evenly.
    items.extend(slow_items[num_workers * slow_items_per_worker:])

    # Add other tests
    items.extend(other_items)


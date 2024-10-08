import pytest

def pytest_collection_modifyitems(config, items):
    slow_items = [item for item in items if "slow" in item.keywords]
    other_items = [item for item in items if "slow" not in item.keywords]

    items.clear()

    # Get number of threads
    num_workers = config.getoption("numprocesses")  # pytest-xdist передает значение в виде числа

    if num_workers is None:
        num_workers = 4  # Number of workers by default

    slow_items_per_worker = max(1, len(slow_items) // num_workers)

    # Add slow tests to every worker
    for i in range(num_workers):
        items.extend(slow_items[i * slow_items_per_worker:(i + 1) * slow_items_per_worker])

    # Add the remaining slow tests if they are not distributed evenly.
    items.extend(slow_items[num_workers * slow_items_per_worker:])

    # Add ordinary tests
    items.extend(other_items)

import pytest


def pytest_collection_modifyitems(config, items):
    # Получаем количество потоков, указанных в команде
    num_processes = config.getoption("numprocesses")

    # Собираем тесты с маркером slow и те, у которых его нет
    slow_tests = [item for item in items if 'slow' in item.keywords]
    non_slow_tests = [item for item in items if 'slow' not in item.keywords]

    # Подготовим списки потоков
    chunked_items = [[] for _ in range(num_processes)]

    # Распределяем slow тесты по потокам
    for i, slow_test in enumerate(slow_tests):
        chunked_items[i % num_processes].append(slow_test)

    # Теперь распределяем остальные тесты
    for i, item in enumerate(non_slow_tests):
        chunked_items[i % num_processes].append(item)

    # Сортируем items так, чтобы pytest-xdist правильно распределил их по потокам
    items[:] = [item for chunk in chunked_items for item in chunk]

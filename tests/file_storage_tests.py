import builtins

import pytest

import api.file_storage as file_storage


@pytest.fixture
def mock_uuid4():
    return lambda: "12345678"


@pytest.fixture
def mock_os():
    class MockOS:
        def __init__(self):
            self.environ = {}

        def getcwd(self, *args, **kwargs):
            return "/path/to"

    return MockOS()


@pytest.fixture
def mock_open():
    class MockFile:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_traceback):
            ...

        def write(self, content):
            ...

    class MockOpen:
        def __call__(self, filename, *args, **kwargs):
            mock_file = MockFile()
            return mock_file

    return MockOpen()


def test_local_file_system(monkeypatch, mock_os, mock_open, mock_uuid4):
    monkeypatch.setattr(file_storage, "os", mock_os)
    monkeypatch.setattr(builtins, "open", mock_open)
    monkeypatch.setattr(file_storage, "uuid4", mock_uuid4)
    storage = file_storage.LocalFileSystem()
    path = storage.write("test.csv", "content")
    assert path == "/path/to/files/test-12345678.csv"

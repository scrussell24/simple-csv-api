import os
from abc import ABC
from uuid import uuid4


class FileStorage(ABC):
    """Base class to abstract differnt types of file storage methods"""

    def write(self, filename: str, content: str) -> str:
        ...


class LocalFileSystem(FileStorage):
    def write(self, filename: str, content: str) -> str:
        """Put file in local storage and return full path to file"""
        path = f"{os.getcwd()}/files/{filename.replace('.csv', '')}-{uuid4()}.csv"
        with open(path, "w") as f:
            f.write(content)
        return path

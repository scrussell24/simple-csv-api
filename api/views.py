from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from api.file_storage import LocalFileSystem
from api.parsers import CsvParser
from api.serializers import CsvFileSerializer


class CsvFileViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    parser_classes = [CsvParser]
    serializer_class = CsvFileSerializer

    def create(self, request, *args, **kwargs):
        storage = LocalFileSystem()
        path = storage.write(request.data["name"], request.data["content"])
        request.data["path"] = path
        return super().create(request, *args, **kwargs)
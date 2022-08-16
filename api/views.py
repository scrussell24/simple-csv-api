from rest_framework import mixins, viewsets

from api.file_storage import LocalFileSystem as FileStorage
from api.parsers import CsvParser
from api.serializers import CsvFileSerializer


class CsvFileViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    parser_classes = [CsvParser]
    serializer_class = CsvFileSerializer

    def create(self, request, *args, **kwargs):
        storage = FileStorage()
        path = storage.write(request.data["name"], request.data["content"])
        request.data["path"] = path
        return super().create(request, *args, **kwargs)

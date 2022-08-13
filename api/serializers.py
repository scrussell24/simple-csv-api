from rest_framework import serializers

from api.models import Column, CsvFile


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = (
            "id",
            "name",
            "column_datatype",
        )


class CsvFileSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True)

    class Meta:
        model = CsvFile
        fields = (
            "id",
            "name",
            "path",
            "columns",
        )

    def create(self, validated_data):
        columns_data = validated_data.pop("columns")
        csv_file = CsvFile.objects.create(**validated_data)
        for col in columns_data:
            Column.objects.create(csv_file=csv_file, **col)
        return csv_file

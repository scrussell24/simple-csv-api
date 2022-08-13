from django.db import models


class CsvFile(models.Model):
    name = models.CharField(max_length=512)
    path = models.CharField(max_length=512)


class Column(models.Model):
    COLUMN_DATATYPES = (
        ("TEXT", "TEXT"),
        ("NUMBER", "NUMBER"),
        ("DATETIME", "DATETIME"),
    )
    csv_file = models.ForeignKey(
        CsvFile, on_delete=models.CASCADE, related_name="columns"
    )
    name = models.CharField(max_length=512)
    column_datatype = models.CharField(max_length=8, choices=COLUMN_DATATYPES)

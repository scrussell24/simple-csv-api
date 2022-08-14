import json

import pytest
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import serializers

import api.views as views
from api.file_storage import FileStorage

EXAMPLE_CSV = """Start Date,End Date,Tactic,Event Type,Pay Type,Attendance,Investment
2/1/2017,2/28/17,Events,Internal,Service,15,3567
2/1/2017,6/30/2017,Events,Internal,Sponsorship,65,3874
2/14/2017,10/31/2018,Events,Internal,Service,10,6474,
2/15/2017,5/17/2017,Events,External,Passive sponsorship,75,6622"""


@pytest.fixture
def mock_file_storage():
    class MockFileStorage(FileStorage):
        def write(self, filename, content):
            return f"/path/to/{filename}"

    return MockFileStorage


CLIENT = Client()


def test_create_file_success():
    response = CLIENT.post(
        reverse("csv_files-list"), data=EXAMPLE_CSV, content_type="text/plain"
    )
    assert response.status_code == 415


def test_create_file_missing_filename_header():
    headers = {
        "HTTP_X_Delimiter": ",",
        "HTTP_X_Quotechar": "",
    }
    response = CLIENT.post(
        reverse("csv_files-list"),
        data=EXAMPLE_CSV,
        content_type="text/csv",
        **headers,
    )
    assert response.status_code == 400


def test_create_file_missing_delimiter():
    headers = {
        "HTTP_X_Filename": "test.csv",
        "HTTP_X_Quotechar": "",
    }
    response = CLIENT.post(
        reverse("csv_files-list"),
        data=EXAMPLE_CSV,
        content_type="text/csv",
        **headers,
    )
    assert response.status_code == 400


def test_create_file_missing_quotechar():
    headers = {
        "HTTP_X_Filename": "test.csv",
        "HTTP_X_Delimiter": ",",
    }
    response = CLIENT.post(
        reverse("csv_files-list"),
        data=EXAMPLE_CSV,
        content_type="text/csv",
        **headers,
    )
    assert response.status_code == 400


def test_create_file_missing_value_row():
    headers = {
        "HTTP_X_Filename": "test.csv",
        "HTTP_X_Delimiter": ",",
        "HTTP_X_Quotechar": "",
    }
    response = CLIENT.post(
        reverse("csv_files-list"),
        data="header1,header2",
        content_type="text/csv",
        **headers,
    )
    assert response.status_code == 400


@pytest.mark.django_db()
def test_create_file_success(monkeypatch, mock_file_storage):
    monkeypatch.setattr(views, "FileStorage", mock_file_storage, raising=True)

    headers = {
        "HTTP_X_Filename": "test.csv",
        "HTTP_X_Delimiter": ",",
        "HTTP_X_Quotechar": "",
    }
    response = CLIENT.post(
        reverse("csv_files-list"),
        data=EXAMPLE_CSV,
        content_type="text/csv",
        **headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "test.csv"
    assert len(response.json()["columns"]) == 7


@pytest.mark.django_db()
def test_create_file_predicted_columns(monkeypatch, mock_file_storage):
    monkeypatch.setattr(views, "FileStorage", mock_file_storage, raising=True)

    headers = {
        "HTTP_X_Filename": "test.csv",
        "HTTP_X_Delimiter": ",",
        "HTTP_X_Quotechar": "",
    }
    response = CLIENT.post(
        reverse("csv_files-list"),
        data=EXAMPLE_CSV,
        content_type="text/csv",
        **headers,
    )

    assert response.status_code == 201
    columns = response.json()["columns"]
    assert columns[0]["column_datatype"] == "DATETIME"
    assert columns[1]["column_datatype"] == "DATETIME"
    assert columns[2]["column_datatype"] == "TEXT"
    assert columns[3]["column_datatype"] == "TEXT"
    assert columns[4]["column_datatype"] == "TEXT"
    assert columns[5]["column_datatype"] == "NUMBER"
    assert columns[6]["column_datatype"] == "NUMBER"

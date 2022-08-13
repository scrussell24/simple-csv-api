from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns, include

from api import views

router = DefaultRouter()
router.register("csv_files", views.CsvFileViewSet, basename="csv_files")

urlpatterns = [
    path("api/", include(router.urls)),
]

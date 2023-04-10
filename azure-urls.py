# urls.py

from django.urls import path
from .views import AzureSQLTable

urlpatterns = [
    path('azure-sql-table/', AzureSQLTable.as_view()),
]

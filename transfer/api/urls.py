from django.urls import path

from transfer.api.views import TransferCreateAPIView, TransferDownloadAPIView

urlpatterns = [
    path('create/', TransferCreateAPIView.as_view()),
    path('download/<str:option>/<slug:url_hash>', TransferDownloadAPIView.as_view()),
]

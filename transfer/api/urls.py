from django.urls import path

from transfer.api.views import TransferCreateAPIView, TransferDownloadAPIView, TransferStatisticsAPIView

urlpatterns = [
    path('create/', TransferCreateAPIView.as_view()),
    path('statistics/', TransferStatisticsAPIView.as_view()),
    path('download/<slug:url_hash>', TransferDownloadAPIView.as_view()),
]

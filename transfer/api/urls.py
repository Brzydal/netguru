from django.urls import path

from transfer.api.views import TransferCreateAPIView

urlpatterns = [
    path('create/', TransferCreateAPIView.as_view()),
]

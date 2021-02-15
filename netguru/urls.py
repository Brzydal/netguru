"""netguru URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic import TemplateView

from transfer.views import TransferDetail, TransferCreate, TransferPassword, TransferDownload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('transfer/create/', TransferCreate.as_view(), name='transfer-create'),
    path('transfer/password/<slug:url_hash>', TransferPassword.as_view(), name='transfer-password'),
    path('transfer/download/<slug:url_hash>/<slug:url_password>', TransferDownload.as_view(), name='transfer-download'),
    path('transfer/<slug:url_hash>/', TransferDetail.as_view(), name='transfer-detail'),
    path('transfer/invalid', TemplateView.as_view(
        template_name='transfer/transfer_invalid.html'), name='transfer-invalid'
         ),
    path('api/', include('transfer.api.urls'))
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

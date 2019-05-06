from django.contrib import admin
from django.urls import path
from core.views import AccountInfoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ussd/', AccountInfoView.as_view())
]

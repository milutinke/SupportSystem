from django.contrib import admin
from django.urls import path, include
from . import views

support_urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register_view),
    path('tickets', views.tickets),
    path('tickets/<int:ticket_id>', views.ticket)
]
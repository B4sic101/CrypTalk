from django.urls import path
from . import views

urlpatterns = [
    path('api/add-contact', views.addContact),
    path('api/get-userid', views.getUserID),
    path('api/acceptFR', views.acceptFR),
    path('api/rejectFR', views.rejectFR)
]
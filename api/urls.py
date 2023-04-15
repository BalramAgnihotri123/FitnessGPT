from django.urls import path
from . import views 


urlpatterns = [
    path("", views.getRoutes),
    path("sessions/", views.createSession, name = 'create-session'),
    path("sessions/<str:id>/", views.getSession, name = 'get-session'),
    path("sessions/<str:id>/prompt/", views.getResponse, name = 'get-response'),
]
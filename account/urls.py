from . import views
from django.urls import path

urlpatterns=[
    path("registeruser/",views.registeruser,name='register')
]
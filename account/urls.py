from . import views
from django.urls import path

urlpatterns=[
    path("registeruser/",views.registeruser,name='register'),
    path("registervendor/",views.registerVendor,name='vendor'),
    path("myaccount/",views.myaccount,name='myaccount'),
    path("login/",views.login,name='login'),
    path("logout/",views.logout,name='logout'),
    # path("dashboard/",views.dashboard,name='dashboard'),
    path("custDashboard/",views.custDashboard,name='custDashboard'),
    path("vendorDashboard/",views.vendorDashboard,name='vendorDashboard'),        
]
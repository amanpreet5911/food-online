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
    path("activate/<uidb64>/<token>/",views.activate,name='activate'),
    path("forgot_password/",views.forgot_password,name='forgotpassword'),
    path("reset-password-validate/<uidb64>/<token>/",views.reset_password_validate,name='reset-password-validate'),
    path("reset-password/",views.reset_password,name='reset_password'),
]
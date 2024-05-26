from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("course/<str:slug>", coursepage, name="coursepage"),
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("check-out/<str:slug>", check_out, name="check-out"),
    path("payment/", payment, name="payment"),
    path("success/", success, name="success"),
]

from django.urls import path
from .views import *

urlpatterns = [
    path("register", Register_User.as_view()),
    path("login", Login_User.as_view()),
    path('products', Products_View.as_view()),
    path("cart", Cart_View.as_view())
]

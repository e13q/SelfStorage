from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("boxes/", views.boxes, name="boxes"),
    path("rent/", views.rent, name="rent"),
    path(
        "register/",
        views.UserRegistrationView.as_view(),
        name="user_registration",
    ),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
]

from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("boxes/", views.boxes, name="boxes"),
    path("faq/", views.faq, name="faq"),
    path('create-order/', views.create_order, name='create_order'),
    path(
        'filter-boxes/<int:warehouse_id>/',
        views.filter_boxes,
        name='filter_boxes'
    ),
    path(
        "register/",
        views.UserRegistrationView.as_view(),
        name="user_registration",
    ),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
    path(
        "profile/",
        login_required(views.UserProfileView.as_view()),
        name="user_profile",
    ),
]

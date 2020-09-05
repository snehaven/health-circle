
from django.urls import path

from . import views
app_name = "heal"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("makepost", views.makepost, name="makepost"),
    path("community", views.community, name="community"),
    path('edit_post/', views.edit_post),
    path("profile/<int:userid>", views.profile, name="profile"),
]

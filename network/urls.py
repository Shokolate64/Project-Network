from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.all_posts, name="all_posts"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("toggle_follow/<int:user_id>", views.toggle_follow, name="toggle_follow"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("toggle_like/<int:post_id>", views.toggle_like, name="toggle_like"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("create_post", views.create_post, name="create_post"),

]

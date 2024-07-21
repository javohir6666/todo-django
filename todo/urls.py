from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name="login"),
    path('signup/', views.signup_view, name='signup'),
    path('', views.indexPage, name="index"),
    path('create/', views.create_todo, name='create_todo'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_todo, name='search_todo'),
]
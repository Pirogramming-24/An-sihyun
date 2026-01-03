from django.urls import path
from . import views

urlpatterns = [
    path('', views.idea_list, name="idea_list"),
    path('idea/register/', views.idea_register, name='idea_register'),
    path('idea/<int:pk>/', views.idea_detail, name='idea_detail'),
    path('idea/<int:pk>/update/', views.idea_update, name='idea_update'),
    path('idea/<int:pk>/delete/', views.idea_delete, name='idea_delete'),
    path('star_toggle/', views.star_toggle, name='star_toggle'),
    path('interest_update/', views.interest_update, name='interest_update'),


    path('devtool', views.dev_list, name="dev_list"),
    path('devtool/register', views.dev_register, name="dev_register"),
    path('devtool/<int:pk>/', views.dev_detail, name="dev_detail"),
    path('devtool/<int:pk>/update/', views.dev_update, name="dev_update"),
    path('devtool/<int:pk>/delete/', views.dev_delete, name="dev_delete"),
]
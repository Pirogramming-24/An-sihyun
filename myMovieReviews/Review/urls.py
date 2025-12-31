from django.urls import path
from . import views

app_name='Review'

urlpatterns = [
	path('', views.review_list, name='review_list'),
        path('add_a_new_review/', views.add_a_new_review, name="new_review"),
        path('<int:pk>/', views.detail, name="detail"),
        path('<int:pk>/update/', views.review_update, name="review_update"),
        path('<int:pk>/delete/', views.review_delete, name="review_delete"),
]
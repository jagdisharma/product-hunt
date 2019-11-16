from django.urls import path
from . import views
urlpatterns = [
    path('create', views.create, name='create'),
    path('<int:product_id>', views.details, name='details'),
    path('<int:product_id>/upvote', views.upvote, name='upvote'),
    path('my-posts', views.myposts, name='myposts'),
    path('<int:post_id>/delete', views.delete, name='delete_post'),
    path('<int:post_id>/edit', views.edit, name='edit_post'),
]

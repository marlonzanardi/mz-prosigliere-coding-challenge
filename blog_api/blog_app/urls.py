from django.urls import path
from .views import (
    BlogPostListCreateView,
    BlogPostDetailView,
    CommentCreateView,
)

urlpatterns = [
    # Blog post endpoints
    path('posts/', BlogPostListCreateView.as_view(), name='blog-post-list-create'),
    path('posts/<int:id>/', BlogPostDetailView.as_view(), name='blog-post-detail'),
    
    # Comment endpoints
    path('posts/<int:post_id>/comments/', CommentCreateView.as_view(), name='comment-create'),
] 
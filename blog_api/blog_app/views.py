from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import BlogPost, Comment
from .serializers import (
    BlogPostListSerializer, 
    BlogPostDetailSerializer, 
    BlogPostCreateUpdateSerializer,
    CommentSerializer
)


@extend_schema(
    tags=['Blog Posts'],
    description='List all blog posts or create a new blog post',
    responses={
        200: BlogPostListSerializer(many=True),
        201: BlogPostDetailSerializer,
    }
)
class BlogPostListCreateView(generics.ListCreateAPIView):
    """
    GET /api/posts: List all blog posts with comment counts.
    POST /api/posts: Create a new blog post.
    """
    
    def get_queryset(self):
        return BlogPost.objects.prefetch_related('comments')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogPostCreateUpdateSerializer
        return BlogPostListSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the new blog post
        blog_post = serializer.save()
        
        # Return detailed representation of the created post
        detail_serializer = BlogPostDetailSerializer(blog_post)
        return Response(
            detail_serializer.data, 
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=['Blog Posts'],
    description='Retrieve a specific blog post with all comments',
    responses={
        200: BlogPostDetailSerializer,
        404: OpenApiResponse(description='Blog post not found'),
    }
)
class BlogPostDetailView(generics.RetrieveAPIView):
    """
    GET /api/posts/{id}: Retrieve a specific blog post with all comments.
    """
    lookup_field = 'id'
    serializer_class = BlogPostDetailSerializer
    
    def get_queryset(self):
        return BlogPost.objects.prefetch_related('comments')
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            return Response(
                {'error': 'Blog post not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    tags=['Comments'],
    description='Add a new comment to a specific blog post',
    responses={
        201: CommentSerializer,
        404: OpenApiResponse(description='Blog post not found'),
    }
)
class CommentCreateView(generics.CreateAPIView):
    """
    POST /api/posts/{id}/comments: Add a new comment to a specific blog post.
    """
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'post_id'
    
    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        
        # Ensure the blog post exists
        blog_post = get_object_or_404(BlogPost, id=post_id)
        
        # Validate comment data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save comment with the blog post relationship
        comment = serializer.save(blog_post=blog_post)
        
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        ) 
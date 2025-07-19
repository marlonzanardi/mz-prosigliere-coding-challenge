from rest_framework import serializers
from .models import BlogPost, Comment


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'content', 'created_at']
        
    def validate_author_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Author name cannot be empty.")
        return value.strip()
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment content cannot be empty.")
        return value.strip()


class BlogPostListSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'comment_count', 'created_at', 'updated_at']


class BlogPostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'comments', 'comment_count', 
                 'created_at', 'updated_at']


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']
        
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value.strip() 
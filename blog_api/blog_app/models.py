from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class BlogPost(models.Model):
    """
    Model representing a blog post.
    
    A blog post has a title and content, and can have multiple comments.
    """
    title = models.CharField(
        max_length=200, 
        validators=[MinLengthValidator(5)],
        help_text="Title of the blog post (5-200 characters)"
    )
    content = models.TextField(
        validators=[MinLengthValidator(10)],
        help_text="Content of the blog post (minimum 10 characters)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    """
    Model representing a comment on a blog post.
    
    Each comment belongs to one blog post.
    """
    blog_post = models.ForeignKey(
        BlogPost, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text="The blog post this comment belongs to"
    )
    author_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        help_text="Name of the comment author (2-100 characters)"
    )
    content = models.TextField(
        validators=[MinLengthValidator(5)],
        help_text="Content of the comment (minimum 5 characters)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['blog_post', '-created_at']),
        ]
    
    def __str__(self):
        return f"Comment by {self.author_name} on {self.blog_post.title}" 
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json

from .models import BlogPost, Comment


class BlogPostModelTest(TestCase):    
    def setUp(self):
        self.blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            content="This is test content for the blog post."
        )
    
    def test_blog_post_creation(self):
        """Test blog post is created correctly."""
        self.assertEqual(self.blog_post.title, "Test Blog Post")
        self.assertEqual(self.blog_post.content, "This is test content for the blog post.")
        self.assertTrue(self.blog_post.created_at)
        self.assertTrue(self.blog_post.updated_at)
    
    def test_blog_post_str_representation(self):
        """Test string representation of blog post."""
        self.assertEqual(str(self.blog_post), "Test Blog Post")
    
    def test_comment_count_property(self):
        """Test comment count property."""
        self.assertEqual(self.blog_post.comment_count, 0)
        
        # Add a comment
        Comment.objects.create(
            blog_post=self.blog_post,
            author_name="Test Author",
            content="Test comment content"
        )
        
        self.assertEqual(self.blog_post.comment_count, 1)


class CommentModelTest(TestCase):
    """Test Comment model functionality."""
    
    def setUp(self):
        self.blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            content="This is test content."
        )
        self.comment = Comment.objects.create(
            blog_post=self.blog_post,
            author_name="Test Author",
            content="This is a test comment."
        )
    
    def test_comment_creation(self):
        """Test comment is created correctly."""
        self.assertEqual(self.comment.author_name, "Test Author")
        self.assertEqual(self.comment.content, "This is a test comment.")
        self.assertEqual(self.comment.blog_post, self.blog_post)
        self.assertTrue(self.comment.created_at)
    
    def test_comment_str_representation(self):
        """Test string representation of comment."""
        expected = f"Comment by Test Author on {self.blog_post.title}"
        self.assertEqual(str(self.comment), expected)


class BlogPostListCreateAPITest(APITestCase):
    """Test GET /api/posts/ and POST /api/posts/ endpoints."""
    
    def setUp(self):
        self.url = reverse('blog-post-list-create')
        self.blog_post = BlogPost.objects.create(
            title="Existing Post",
            content="Existing content"
        )
        # Add a comment to test comment count
        Comment.objects.create(
            blog_post=self.blog_post,
            author_name="Commenter",
            content="Test comment"
        )
    
    def test_get_blog_posts_list(self):
        """Test retrieving list of blog posts."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        post_data = response.data['results'][0]
        self.assertEqual(post_data['title'], "Existing Post")
        self.assertEqual(post_data['comment_count'], 1)
        self.assertIn('id', post_data)
        self.assertIn('created_at', post_data)
    
    def test_create_blog_post_valid_data(self):
        """Test creating a blog post with valid data."""
        data = {
            'title': 'New Blog Post',
            'content': 'This is new blog post content.'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 2)
        
        # Verify response includes all fields
        self.assertEqual(response.data['title'], 'New Blog Post')
        self.assertEqual(response.data['content'], 'This is new blog post content.')
        self.assertEqual(response.data['comment_count'], 0)
        self.assertIn('id', response.data)
    
    def test_create_blog_post_invalid_data(self):
        """Test creating blog post with invalid data."""
        # Test empty title
        data = {'title': '', 'content': 'Valid content'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test empty content
        data = {'title': 'Valid title', 'content': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test missing fields
        data = {'title': 'Only title'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BlogPostDetailAPITest(APITestCase):
    """Test GET /api/posts/{id}/ endpoint."""
    
    def setUp(self):
        self.blog_post = BlogPost.objects.create(
            title="Detail Test Post",
            content="Content for detail testing"
        )
        self.comment = Comment.objects.create(
            blog_post=self.blog_post,
            author_name="Comment Author",
            content="Comment for detail testing"
        )
        self.url = reverse('blog-post-detail', kwargs={'id': self.blog_post.id})
    
    def test_get_blog_post_detail(self):
        """Test retrieving specific blog post with comments."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify all fields are present
        self.assertEqual(response.data['title'], "Detail Test Post")
        self.assertEqual(response.data['content'], "Content for detail testing")
        self.assertEqual(response.data['comment_count'], 1)
        self.assertEqual(len(response.data['comments']), 1)
        
        # Verify comment data
        comment_data = response.data['comments'][0]
        self.assertEqual(comment_data['author_name'], "Comment Author")
        self.assertEqual(comment_data['content'], "Comment for detail testing")
    
    def test_get_nonexistent_blog_post(self):
        """Test retrieving non-existent blog post."""
        url = reverse('blog-post-detail', kwargs={'id': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentCreateAPITest(APITestCase):
    """Test POST /api/posts/{id}/comments/ endpoint."""
    
    def setUp(self):
        self.blog_post = BlogPost.objects.create(
            title="Post for Comments",
            content="Content for comment testing"
        )
        self.url = reverse('comment-create', kwargs={'post_id': self.blog_post.id})
    
    def test_create_comment_valid_data(self):
        """Test creating comment with valid data."""
        data = {
            'author_name': 'Test Commenter',
            'content': 'This is a test comment.'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        
        # Verify response data
        self.assertEqual(response.data['author_name'], 'Test Commenter')
        self.assertEqual(response.data['content'], 'This is a test comment.')
        self.assertIn('id', response.data)
        
        # Verify comment is linked to correct post
        comment = Comment.objects.first()
        self.assertEqual(comment.blog_post, self.blog_post)
    
    def test_create_comment_invalid_data(self):
        """Test creating comment with invalid data."""
        # Test empty author name
        data = {'author_name': '', 'content': 'Valid content'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test empty content
        data = {'author_name': 'Valid Author', 'content': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_comment_nonexistent_post(self):
        """Test creating comment for non-existent blog post."""
        url = reverse('comment-create', kwargs={'post_id': 99999})
        data = {
            'author_name': 'Test Commenter',
            'content': 'This comment should fail.'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class APIIntegrationTest(APITestCase):
    """Integration tests for complete API workflows."""
    
    def test_complete_blog_workflow(self):
        """Test complete workflow: create post, retrieve it, add comment."""
        # 1. Create a blog post
        post_data = {
            'title': 'Integration Test Post',
            'content': 'Content for integration testing.'
        }
        
        create_response = self.client.post(
            reverse('blog-post-list-create'), 
            post_data, 
            format='json'
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        post_id = create_response.data['id']
        
        # 2. Retrieve the blog post
        detail_response = self.client.get(
            reverse('blog-post-detail', kwargs={'id': post_id})
        )
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['comment_count'], 0)
        
        # 3. Add a comment
        comment_data = {
            'author_name': 'Integration Tester',
            'content': 'Great integration test post!'
        }
        
        comment_response = self.client.post(
            reverse('comment-create', kwargs={'post_id': post_id}),
            comment_data,
            format='json'
        )
        self.assertEqual(comment_response.status_code, status.HTTP_201_CREATED)
        
        # 4. Verify comment appears in post detail
        final_detail_response = self.client.get(
            reverse('blog-post-detail', kwargs={'id': post_id})
        )
        self.assertEqual(final_detail_response.data['comment_count'], 1)
        self.assertEqual(len(final_detail_response.data['comments']), 1)
        self.assertEqual(
            final_detail_response.data['comments'][0]['author_name'], 
            'Integration Tester'
        ) 
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Post, Like, Comment


class PostModelTest(TestCase):
    """Test Post model functionality."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_post_creation(self):
        """Test creating a post."""
        post = Post.objects.create(
            content='Test post content',
            author=self.user
        )
        self.assertEqual(post.content, 'Test post content')
        self.assertEqual(post.author, self.user)
        self.assertEqual(str(post), f"{self.user.username}: Test post content")
    
    def test_post_likes_count(self):
        """Test post likes count property."""
        post = Post.objects.create(content='Test post', author=self.user)
        self.assertEqual(post.likes_count, 0)
        
        Like.objects.create(user=self.user, post=post)
        self.assertEqual(post.likes_count, 1)


class PostAPITest(APITestCase):
    """Test Post API endpoints."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            content='Test post content',
            author=self.user
        )
    
    def test_get_posts_list(self):
        """Test getting list of posts."""
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_post_authenticated(self):
        """Test creating a post when authenticated."""
        self.client.force_authenticate(user=self.user)
        url = reverse('post-list')
        data = {'content': 'New test post'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
    
    def test_create_post_unauthenticated(self):
        """Test creating a post when not authenticated."""
        url = reverse('post-list')
        data = {'content': 'New test post'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_own_post(self):
        """Test updating own post."""
        self.client.force_authenticate(user=self.user)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'content': 'Updated content'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'Updated content')
    
    def test_update_other_user_post(self):
        """Test updating another user's post (should fail)."""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'content': 'Updated content'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_like_post(self):
        """Test liking a post."""
        self.client.force_authenticate(user=self.user)
        url = reverse('post-like', kwargs={'pk': self.post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
    
    def test_unlike_post(self):
        """Test unliking a post."""
        Like.objects.create(user=self.user, post=self.post)
        self.client.force_authenticate(user=self.user)
        url = reverse('post-unlike', kwargs={'pk': self.post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)

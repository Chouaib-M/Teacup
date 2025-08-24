from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import UserProfile, Follow


class UserModelTest(TestCase):
    """Test User and UserProfile model functionality."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_creation(self):
        """Test that UserProfile is automatically created with User."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
    
    def test_follow_creation(self):
        """Test creating a follow relationship."""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        follow = Follow.objects.create(follower=self.user, followed=other_user)
        self.assertEqual(follow.follower, self.user)
        self.assertEqual(follow.followed, other_user)
    
    def test_followers_count(self):
        """Test followers count property."""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.assertEqual(self.user.profile.followers_count, 0)
        Follow.objects.create(follower=other_user, followed=self.user)
        self.assertEqual(self.user.profile.followers_count, 1)


class UserAPITest(APITestCase):
    """Test User API endpoints."""
    
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
    
    def test_create_user(self):
        """Test user registration."""
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
    
    def test_get_users_list(self):
        """Test getting list of users."""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_follow_user(self):
        """Test following a user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('user-follow', kwargs={'pk': self.other_user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)
    
    def test_unfollow_user(self):
        """Test unfollowing a user."""
        Follow.objects.create(follower=self.user, followed=self.other_user)
        self.client.force_authenticate(user=self.user)
        url = reverse('user-unfollow', kwargs={'pk': self.other_user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Follow.objects.count(), 0)
    
    def test_cannot_follow_self(self):
        """Test that users cannot follow themselves."""
        self.client.force_authenticate(user=self.user)
        url = reverse('user-follow', kwargs={'pk': self.user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_own_profile(self):
        """Test updating own profile."""
        self.client.force_authenticate(user=self.user)
        url = reverse('user-update-profile', kwargs={'pk': self.user.pk})
        data = {'bio': 'Updated bio'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Updated bio')
    
    def test_cannot_update_other_profile(self):
        """Test that users cannot update other users' profiles."""
        self.client.force_authenticate(user=self.user)
        url = reverse('user-update-profile', kwargs={'pk': self.other_user.pk})
        data = {'bio': 'Hacked bio'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

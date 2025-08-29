from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import UserProfile, Follow
from .serializers import (
    UserSerializer, UserListSerializer, UserProfileUpdateSerializer,
    FollowSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User CRUD operations.
    
    TODO: Maybe add rate limiting for user creation to prevent spam accounts
    """
    queryset = User.objects.all().select_related('profile')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'profile__bio']
    ordering_fields = ['username', 'date_joined']
    ordering = ['username']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer

    def get_permissions(self):
        """Set permissions based on action."""
        # Allow anyone to create accounts (registration)
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        # Only authenticated users can modify/delete
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated] 
        else:
            # Default: read-only for anonymous, full access for authenticated
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        """Only allow users to update their own profile."""
        user = self.get_object()
        if request.user != user:
            return Response(
                {'error': 'You can only update your own profile.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Only allow users to delete their own account."""
        user = self.get_object()
        if request.user != user:
            return Response(
                {'error': 'You can only delete your own account.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request, pk=None):
        """Update user profile information."""
        user = self.get_object()
        if request.user != user:
            return Response(
                {'error': 'You can only update your own profile.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = UserProfileUpdateSerializer(
            user.profile, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        """Follow a user."""
        user_to_follow = self.get_object()
        
        # Prevent users from following themselves (that would be weird lol)
        if request.user == user_to_follow:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            followed=user_to_follow
        )
        
        if not created:
            return Response(
                {'error': 'You are already following this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {'message': f'You are now following {user_to_follow.username}.'},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, pk=None):
        """Unfollow a user."""
        user_to_unfollow = self.get_object()
        
        try:
            follow = Follow.objects.get(
                follower=request.user,
                followed=user_to_unfollow
            )
            follow.delete()
            return Response(
                {'message': f'You have unfollowed {user_to_unfollow.username}.'},
                status=status.HTTP_200_OK
            )
        except Follow.DoesNotExist:
            return Response(
                {'error': 'You are not following this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        """Get list of user's followers."""
        user = self.get_object()
        followers = Follow.objects.filter(followed=user).select_related('follower__profile')
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        """Get list of users this user is following."""
        user = self.get_object()
        following = Follow.objects.filter(follower=user).select_related('followed__profile')
        serializer = FollowSerializer(following, many=True)
        return Response(serializer.data)

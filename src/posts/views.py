from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from .models import Post, Like, Comment
from .serializers import (
    PostSerializer, PostListSerializer, PostCreateUpdateSerializer,
    CommentSerializer, LikeSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post CRUD operations.
    
    Note: Using select_related and prefetch_related for performance
    because we had some N+1 query issues in testing
    """
    queryset = Post.objects.all().select_related('author__profile').prefetch_related('likes', 'comments__author')
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['content', 'author__username']
    filterset_fields = ['author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostSerializer

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['create', 'like', 'unlike', 'add_comment']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        """Only allow post authors to update their posts."""
        post = self.get_object()
        if request.user != post.author:
            return Response(
                {'error': 'You can only update your own posts.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Only allow post authors to delete their posts."""
        post = self.get_object()
        if request.user != post.author:
            return Response(
                {'error': 'You can only delete your own posts.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Like a post."""
        post = self.get_object()
        
        # Using get_or_create to avoid race conditions
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )
        
        if not created:
            return Response(
                {'error': 'You have already liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: Maybe add notification system here later?
        return Response(
            {'message': 'Post liked successfully.'},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        """Unlike a post."""
        post = self.get_object()
        
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response(
                {'message': 'Post unliked successfully.'},
                status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            return Response(
                {'error': 'You have not liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        """Add a comment to a post."""
        post = self.get_object()
        
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a post."""
        post = self.get_object()
        comments = Comment.objects.filter(post=post).select_related('author__profile')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        """Get all likes for a post."""
        post = self.get_object()
        likes = Like.objects.filter(post=post).select_related('user__profile')
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment CRUD operations."""
    queryset = Comment.objects.all().select_related('author__profile', 'post')
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['content', 'author__username']
    filterset_fields = ['post', 'author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        """Only allow comment authors to update their comments."""
        comment = self.get_object()
        if request.user != comment.author:
            return Response(
                {'error': 'You can only update your own comments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Only allow comment authors to delete their comments."""
        comment = self.get_object()
        if request.user != comment.author:
            return Response(
                {'error': 'You can only delete your own comments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

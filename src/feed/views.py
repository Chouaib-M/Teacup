from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from posts.models import Post
from posts.serializers import PostListSerializer
from users.models import Follow


class FeedPagination(PageNumberPagination):
    """Custom pagination for feed."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for personalized feed functionality."""
    serializer_class = PostListSerializer
    pagination_class = FeedPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['content', 'author__username']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return posts from users that the current user follows."""
        user = self.request.user
        
        # Get users that the current user follows
        following_users = Follow.objects.filter(follower=user).values_list('followed', flat=True)
        
        # Include the user's own posts in the feed
        feed_users = list(following_users) + [user.id]
        
        return Post.objects.filter(
            author__in=feed_users
        ).select_related('author__profile').prefetch_related('likes', 'comments')

    @action(detail=False, methods=['get'])
    def my_feed(self, request):
        """Get the authenticated user's personalized feed."""
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def discover(self, request):
        """Get posts from all users for discovery."""
        queryset = Post.objects.all().select_related('author__profile').prefetch_related('likes', 'comments')
        queryset = self.filter_queryset(queryset)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending posts (posts with most likes in the last 7 days)."""
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Count
        
        week_ago = timezone.now() - timedelta(days=7)
        
        queryset = Post.objects.filter(
            created_at__gte=week_ago
        ).annotate(
            likes_count_week=Count('likes')
        ).order_by('-likes_count_week', '-created_at').select_related('author__profile').prefetch_related('likes', 'comments')
        
        queryset = self.filter_queryset(queryset)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

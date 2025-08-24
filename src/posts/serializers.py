from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like, Comment


class PostAuthorSerializer(serializers.ModelSerializer):
    """Simplified serializer for post authors."""
    profile_picture = serializers.CharField(source='profile.profile_picture', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_picture']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    author = PostAuthorSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Create comment with authenticated user as author."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for Like model."""
    user = PostAuthorSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model."""
    author = PostAuthorSerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'content', 'author', 'media_url', 'created_at', 'updated_at',
            'likes_count', 'comments_count', 'is_liked', 'comments'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        """Check if the current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False

    def create(self, validated_data):
        """Create post with authenticated user as author."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """Simplified serializer for post lists."""
    author = PostAuthorSerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'content', 'author', 'media_url', 'created_at',
            'likes_count', 'comments_count', 'is_liked'
        ]

    def get_is_liked(self, obj):
        """Check if the current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating posts."""
    
    class Meta:
        model = Post
        fields = ['content', 'media_url']
        
    def create(self, validated_data):
        """Create post with authenticated user as author."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

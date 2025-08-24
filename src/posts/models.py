from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Post(models.Model):
    """Model for user posts in the social media platform."""
    content = models.TextField(
        max_length=2000,
        validators=[MinLengthValidator(1)],
        help_text="Post content (required)"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="The user who created this post"
    )
    media_url = models.URLField(
        blank=True,
        null=True,
        help_text="Optional URL to media (image, video, etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Most recent posts first
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}{'...' if len(self.content) > 50 else ''}"

    @property
    def likes_count(self):
        """Return the number of likes for this post."""
        return self.likes.count()

    @property
    def comments_count(self):
        """Return the number of comments for this post."""
        return self.comments.count()


class Like(models.Model):
    """Model for post likes."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liked_posts'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"


class Comment(models.Model):
    """Model for post comments."""
    content = models.TextField(
        max_length=500,
        validators=[MinLengthValidator(1)]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']  # Oldest comments first

    def __str__(self):
        return f"{self.author.username} on {self.post.id}: {self.content[:30]}{'...' if len(self.content) > 30 else ''}"

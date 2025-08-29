# Teacup Social Media API - Complete Manual

## Overview
Teacup is a Django REST Framework-based social media API that provides functionality for users, posts, comments, likes, follows, and personalized feeds.

## Project Architecture

### Core Components
- **Django REST Framework** - API framework
- **SQLite Database** - Data storage (development)
- **drf-spectacular** - API documentation
- **django-filters** - Filtering and search

### Apps Structure
```
src/
├── teacup/          # Main Django project
├── users/           # User management & profiles
├── posts/           # Posts, comments, likes
└── feed/            # Personalized feeds
```

## Getting Started

### 1. Setup & Installation
```bash
# Install dependencies
pip install Django djangorestframework django-filter drf-spectacular python-dotenv whitenoise

# Navigate to project
cd c:\Users\tanki\social-media-api-starter\social-media-api-starter\src

# Create database tables
python manage.py makemigrations users posts feed
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### 2. Access Points
- **API Root**: http://127.0.0.1:8000/
- **Interactive Docs**: http://127.0.0.1:8000/api/docs/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Schema**: http://127.0.0.1:8000/api/schema/

## Authentication
All endpoints use Django's session authentication. Login via:
- Admin panel: http://127.0.0.1:8000/admin/
- API docs: Click "Authorize" button at http://127.0.0.1:8000/api/docs/

## API Endpoints Reference

### Users Endpoints (`/api/v1/users/`)

#### 1. List/Create Users
- **GET** `/api/v1/users/` - List all users
- **POST** `/api/v1/users/` - Create new user

**Create User Example:**
```json
POST /api/v1/users/
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure123",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### 2. User Details
- **GET** `/api/v1/users/{id}/` - Get user details
- **PUT** `/api/v1/users/{id}/` - Update user (own profile only)
- **DELETE** `/api/v1/users/{id}/` - Delete user (own profile only)

#### 3. User Actions
- **POST** `/api/v1/users/{id}/follow/` - Follow a user
- **POST** `/api/v1/users/{id}/unfollow/` - Unfollow a user
- **GET** `/api/v1/users/{id}/followers/` - Get user's followers
- **GET** `/api/v1/users/{id}/following/` - Get users they follow
- **PUT** `/api/v1/users/{id}/update_profile/` - Update profile info

**Update Profile Example:**
```json
PUT /api/v1/users/{id}/update_profile/
{
    "bio": "Software developer and coffee enthusiast",
    "website": "https://johndoe.dev",
    "location": "San Francisco, CA"
}
```

### Posts Endpoints (`/api/v1/posts/`)

#### 1. List/Create Posts
- **GET** `/api/v1/posts/` - List all posts (with pagination)
- **POST** `/api/v1/posts/` - Create new post

**Create Post Example:**
```json
POST /api/v1/posts/
{
    "content": "Just built an amazing Django API! 🚀",
    "media_url": "https://example.com/image.jpg"
}
```

#### 2. Post Details
- **GET** `/api/v1/posts/{id}/` - Get post details
- **PUT** `/api/v1/posts/{id}/` - Update post (author only)
- **DELETE** `/api/v1/posts/{id}/` - Delete post (author only)

#### 3. Post Actions
- **POST** `/api/v1/posts/{id}/like/` - Like a post
- **POST** `/api/v1/posts/{id}/unlike/` - Unlike a post
- **GET** `/api/v1/posts/{id}/likes/` - Get post likes
- **POST** `/api/v1/posts/{id}/add_comment/` - Add comment to post
- **GET** `/api/v1/posts/{id}/comments/` - Get post comments

**Add Comment Example:**
```json
POST /api/v1/posts/{id}/add_comment/
{
    "content": "Great post! Thanks for sharing."
}
```

### Comments Endpoints (`/api/v1/comments/`)

#### 1. List/Create Comments
- **GET** `/api/v1/comments/` - List all comments
- **POST** `/api/v1/comments/` - Create new comment

#### 2. Comment Details
- **GET** `/api/v1/comments/{id}/` - Get comment details
- **PUT** `/api/v1/comments/{id}/` - Update comment (author only)
- **DELETE** `/api/v1/comments/{id}/` - Delete comment (author only)

### Feed Endpoints (`/api/v1/feed/`)

#### 1. Personalized Feeds
- **GET** `/api/v1/feed/` - Get your personalized feed
- **GET** `/api/v1/feed/my_feed/` - Alternative feed endpoint
- **GET** `/api/v1/feed/discover/` - Discover new content
- **GET** `/api/v1/feed/trending/` - Get trending posts

## Data Models

### User Profile
```json
{
    "id": 1,
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "bio": "Software developer",
    "profile_picture": "https://example.com/avatar.jpg",
    "website": "https://johndoe.dev",
    "location": "San Francisco",
    "followers_count": 150,
    "following_count": 200,
    "created_at": "2024-01-01T12:00:00Z"
}
```

### Post
```json
{
    "id": 1,
    "content": "Hello world! 🌍",
    "media_url": "https://example.com/image.jpg",
    "author": {
        "id": 1,
        "username": "john_doe"
    },
    "likes_count": 25,
    "comments_count": 5,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
}
```

### Comment
```json
{
    "id": 1,
    "content": "Great post!",
    "author": {
        "id": 2,
        "username": "jane_doe"
    },
    "post": 1,
    "created_at": "2024-01-01T12:30:00Z"
}
```

## Common Workflows

### 1. New User Registration & Setup
```bash
# 1. Create user account
POST /api/v1/users/
{
    "username": "newuser",
    "email": "user@example.com",
    "password": "secure123"
}

# 2. Update profile
PUT /api/v1/users/{id}/update_profile/
{
    "bio": "New to the platform!",
    "location": "New York"
}

# 3. Follow some users
POST /api/v1/users/{other_user_id}/follow/
```

### 2. Creating & Interacting with Posts
```bash
# 1. Create a post
POST /api/v1/posts/
{
    "content": "My first post!"
}

# 2. Like the post
POST /api/v1/posts/{post_id}/like/

# 3. Add a comment
POST /api/v1/posts/{post_id}/add_comment/
{
    "content": "Welcome to the platform!"
}
```

### 3. Building Your Feed
```bash
# 1. Follow interesting users
POST /api/v1/users/{user_id}/follow/

# 2. Check your personalized feed
GET /api/v1/feed/

# 3. Discover new content
GET /api/v1/feed/discover/
```

## Filtering & Search

### Posts Filtering
```bash
# Filter by author
GET /api/v1/posts/?author=1

# Search in content
GET /api/v1/posts/?search=django

# Order by date
GET /api/v1/posts/?ordering=-created_at
```

### Users Filtering
```bash
# Search users
GET /api/v1/users/?search=john

# Filter by location
GET /api/v1/users/?profile__location=San Francisco
```

## Pagination
All list endpoints support pagination:
```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/v1/posts/?page=2",
    "previous": null,
    "results": [...]
}
```

## Error Handling

### Common HTTP Status Codes
- **200 OK** - Success
- **201 Created** - Resource created
- **400 Bad Request** - Invalid data
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Permission denied
- **404 Not Found** - Resource not found

### Error Response Format
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## Testing the API

### Using the Interactive Docs
1. Go to http://127.0.0.1:8000/api/docs/
2. Click "Authorize" and login
3. Try different endpoints directly in the browser

### Using curl Examples
```bash
# Get all users
curl -X GET http://127.0.0.1:8000/api/v1/users/

# Create a post (requires authentication)
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello from curl!"}'
```

## Troubleshooting

### Common Issues
1. **404 on root URL** - Normal, use /api/v1/ endpoints
2. **Empty feed** - Need to follow users and create posts first
3. **Authentication errors** - Login via /admin/ or API docs first
4. **Migration errors** - Run `makemigrations` then `migrate`

### Database Reset
```bash
# If you need to reset the database
rm db.sqlite3
python manage.py makemigrations users posts feed
python manage.py migrate
python manage.py createsuperuser
```

## Next Steps
- Add profile pictures upload
- Implement real-time notifications
- Add post media upload
- Deploy to production (Heroku/Railway)
- Add email verification
- Implement OAuth authentication

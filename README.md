# Teacup Social Media API

A Django REST Framework social media API I built for learning purposes. Started as a simple CRUD app but ended up adding a bunch of social features like following, feeds, etc.

## ✨ Features (Implemented)
- **User Management**: CRUD operations with extended profiles (bio, profile picture, website, location)
- **Posts**: Create, read, update, delete posts with content and optional media URLs
- **Social Features**: Follow/unfollow users, likes, comments
- **Personalized Feed**: View posts from followed users, discover new content, trending posts
- **Authentication & Permissions**: Secure endpoints with proper user permissions
- **Admin Interface**: Django admin for managing all models
- **API Documentation**: Swagger UI and ReDoc documentation
- **Search & Filtering**: Search posts and users, filter by various criteria
- **Pagination**: Efficient pagination for all list endpoints

## 🧱 Tech Stack
- **Python 3.11+**
- **Django 5**
- **Django REST Framework**
- **django-filter**, **drf-spectacular**
- **gunicorn** + **whitenoise** (Heroku-friendly)
- **python-dotenv**

## 🚀 Setup Instructions

```bash
# 1) Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 2) Install dependencies (if not already installed)
pip install -r requirements.txt

# 3) Navigate to src directory
cd src

# 4) Create and run migrations
# Note: Sometimes you need to run makemigrations for each app separately
python manage.py makemigrations users
python manage.py makemigrations posts
python manage.py makemigrations
python manage.py migrate

# 5) Create superuser for admin access
python manage.py createsuperuser

# 6) Run development server
python manage.py runserver
```

## 📋 API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - Login
- `POST /api/v1/auth/logout/` - Logout

### Users
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user (register)
- `GET /api/v1/users/{id}/` - Get user details
- `PUT /api/v1/users/{id}/` - Update user
- `DELETE /api/v1/users/{id}/` - Delete user
- `PATCH /api/v1/users/{id}/update_profile/` - Update profile
- `POST /api/v1/users/{id}/follow/` - Follow user
- `POST /api/v1/users/{id}/unfollow/` - Unfollow user
- `GET /api/v1/users/{id}/followers/` - Get followers
- `GET /api/v1/users/{id}/following/` - Get following

### Posts
- `GET /api/v1/posts/` - List posts
- `POST /api/v1/posts/` - Create post
- `GET /api/v1/posts/{id}/` - Get post details
- `PUT /api/v1/posts/{id}/` - Update post
- `DELETE /api/v1/posts/{id}/` - Delete post
- `POST /api/v1/posts/{id}/like/` - Like post
- `POST /api/v1/posts/{id}/unlike/` - Unlike post
- `POST /api/v1/posts/{id}/add_comment/` - Add comment
- `GET /api/v1/posts/{id}/comments/` - Get comments
- `GET /api/v1/posts/{id}/likes/` - Get likes

### Comments
- `GET /api/v1/comments/` - List comments
- `POST /api/v1/comments/` - Create comment
- `GET /api/v1/comments/{id}/` - Get comment
- `PUT /api/v1/comments/{id}/` - Update comment
- `DELETE /api/v1/comments/{id}/` - Delete comment

### Feed
- `GET /api/v1/feed/my_feed/` - Personal feed (posts from followed users)
- `GET /api/v1/feed/discover/` - Discover posts (all posts)
- `GET /api/v1/feed/trending/` - Trending posts (most liked in last 7 days)

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **Admin Interface**: http://127.0.0.1:8000/admin/

## 🔧 Environment Variables
Copy `.env.example` to `.env` at the repo root and adjust values as needed.

## 📦 Repository Structure
```
social-media-api/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ .env.example
├─ LICENSE
├─ docs/
│  └─ PART3_SUBMISSION_TEMPLATE.md
└─ src/
   ├─ manage.py
   ├─ teacup/           # Django project settings
   │  ├─ __init__.py
   │  ├─ settings.py
   │  ├─ urls.py
   │  └─ wsgi.py
   ├─ users/            # User management app
   │  ├─ models.py      # UserProfile, Follow models
   │  ├─ serializers.py # User serializers
   │  ├─ views.py       # User viewsets
   │  ├─ urls.py        # User URLs
   │  └─ admin.py       # User admin
   ├─ posts/            # Posts app
   │  ├─ models.py      # Post, Like, Comment models
   │  ├─ serializers.py # Post serializers
   │  ├─ views.py       # Post viewsets
   │  ├─ urls.py        # Post URLs
   │  └─ admin.py       # Post admin
   └─ feed/             # Feed app
      ├─ views.py       # Feed viewsets
      └─ urls.py        # Feed URLs
```

## 🚀 Next Steps

1. **Run the setup commands** above to create your database and start the server
2. **Test the API** using the Swagger UI at `/api/docs/`
3. **Create some test data** through the admin interface or API
4. **Deploy to production** (Heroku, PythonAnywhere, etc.)

## 🎯 What I Built

✅ **Post Management**: Basic CRUD for posts - users can create, edit, delete their posts  
✅ **User Profiles**: Extended the default User model with bio, profile pic, etc.  
✅ **Follow System**: Users can follow/unfollow each other (took a while to get the constraints right)  
✅ **Personalized Feed**: Shows posts from people you follow + your own posts  
✅ **Social Features**: Likes and comments (might add reactions later)  
✅ **Search & Filters**: Can search posts and users  
✅ **API Docs**: Auto-generated with drf-spectacular  
✅ **Admin Interface**: For managing content

**TODO**: Add real-time notifications, maybe websockets for live updates

---

## 🚀 Deployment

### Heroku Deployment
The project is configured for easy Heroku deployment:

1. **Create Heroku app**: `heroku create your-app-name`
2. **Set environment variables**: 
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```
3. **Deploy**: `git push heroku main`

### Local Production Testing
```bash
# Collect static files
python manage.py collectstatic

# Run with gunicorn
gunicorn teacup.wsgi --bind 0.0.0.0:8000
```

## 🎯 Key Features Showcase

### 🔐 **Authentication & User Management**
- Complete user registration and profile management
- Extended profiles with bio, profile picture, website, location
- Follow/unfollow system with relationship tracking

### 📝 **Content Management** 
- Full CRUD operations for posts with rich content support
- Media URL support for images and videos
- Like and comment system with real-time counts

### 📱 **Social Features**
- Personalized feed showing posts from followed users
- Discover feed for exploring new content  
- Trending posts based on engagement metrics
- Search functionality across posts and users

### 🔧 **Technical Excellence**
- RESTful API design with proper HTTP methods
- Comprehensive pagination and filtering
- Interactive API documentation (Swagger/ReDoc)
- Admin interface for content management
- Production-ready deployment configuration

## 📄 License
MIT License - See LICENSE file for details.

---

**🎉 Teacup Social Media API - Complete & Production Ready!**

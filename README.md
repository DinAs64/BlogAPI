📝 BlogAPI

A fully featured blog API built with Django REST Framework, featuring custom user authentication, nested routes for comments under posts, token-based authentication via SimpleJWT, and full test coverage.

---

🧩 Apps & Models

### Blog App
- **Models:**
  - `Post`
  - `Comment`
- **Serializers:**
  - `PostSerializer`: 
    - Validates `title` and `content`
  - `CommentSerializer`: 
    - Validates `content`
- **Views:**
  - `PostListCreateAPIView`: `IsAuthenticated`
  - `PostRetrieveUpdateDestroyAPIView`: `IsAuthorOrAdmin`
  - `CommentListCreateAPIView`: `IsAuthenticated`, with:
    - Custom `get_queryset`
    - Custom `perform_create` to link nested post
  - `CommentRetrieveUpdateDestroyAPIView`: `IsAuthorOrAdmin`

### Users App
- **Models:**
  - `CustomUser`
  - `UserProfile`
- **Serializers:**
  - `UserSerializer`: Validates
    - `username`: min length 6, unique, alphanumeric, no forbidden names
    - `password`: min 8, must contain upper, lower, digit, special char
    - `email`: unique, valid format
    - Object-level password confirmation match
    - `create()` discards password confirmation field
  - `UserProfileSerializer`: No extra validation
- **Views:**
  - `UserLoginViewSet`: `AllowAny`
  - `UserProfileViewSet`: `IsOwner`, with custom `get_queryset`

---

🔍 Search, Filter, and Pagination

Implemented via DRF’s built-in `SearchFilter`, `OrderingFilter`, and `django-filter`.

### 🧵 Post Endpoints
- `GET /posts/?search=django`
- `GET /posts/?ordering=-created_at`
- `GET /posts/?author=3`
- `GET /posts/?page=2&page_size=5`

### 💬 Comment Endpoints (nested)
- `GET /posts/<post_id>/comments/?search=thanks`
- `GET /posts/<post_id>/comments/?ordering=created_at`
- `GET /posts/<post_id>/comments/?page=1&page_size=5`

---

🔐 Authentication

- JWT via **SimpleJWT**
  - `token/` → `TokenObtainPairView`
  - `token/refresh/` → `TokenRefreshView`

---
🛡️ Security Features

- **Scoped Rate Limiting** (via DRF throttling)
  - `POST /token/` (login): max 5 requests/minute
  - `POST /posts/<id>/comments/`: max 10 requests/hour
  - Prevents brute-force and spam attacks

---
🚀 Redis Caching (Comments)

- Nested comment list views are cached per post and query string using Redis.
- All related comment caches are invalidated automatically when a new comment is posted.

---

🌐 URL Routing

### Blog URLs
- Custom paths using nested routes:
  - `/posts/`
  - `/posts/<post_id>/`
  - `/posts/<post_id>/comments/`
  - `/posts/<post_id>/comments/<comment_id>/`

### Users URLs
- Router-based:
  - `/users/`
  - `/users/<id>/profile/`

---

✅ Testing

- 32 comprehensive tests across both apps
- Uses:
  - `lazy_fixture`
  - `faker`
  - `SimpleTestCase`, `TestCase`, `APITestCase`
- Factories per app
- All tests pass with high coverage

---

🐳 Docker Setup

This project uses Docker and Docker Compose to run the Django API with MySQL and Redis services.

- How to run:
  - docker-compose up --build
  - docker-compose exec web python manage.py migrate
  - docker-compose exec web python manage.py createsuperuser
- Visit http://localhost:8000 to access the API.

- Included Services:
  - web: Django app running with Gunicorn
  - db: MySQL database
  - redis: Redis caching

Everything is configured to work together out-of-the-box, so you get a consistent development environment without manual installs.
---

⚙️ Environment & Configuration

- Environment variables managed with **python-decouple**
- `.env` file used to store sensitive values
- `.gitignore` in place to exclude unnecessary or sensitive files

---

🚀 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/blogapi.git
   cd blogapi


🛠️ Tech Stack

Backend: Django, Django REST Framework
Auth: JWT (SimpleJWT)
Testing: Django TestCase, Faker, DRF TestTools
Utilities: python-decouple, nested routers




# Blog API - Django REST Framework

A production-ready RESTful API for managing a simple blogging platform built with Django REST Framework. This API provides endpoints for managing blog posts and their associated comments.

## Features

- **Complete operations** for blog posts and comments
- **Optimized database queries** with proper indexing and annotations
- **Comprehensive test suite** with 95%+ coverage
- **Production-ready configuration** with security best practices
- **Docker support** for easy deployment
- **PostgreSQL integration** and SQLite for development
- **API documentation** with Swagger/OpenAPI 3.0

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/posts/` | List all blog posts with comment counts |
| `POST` | `/api/posts/` | Create a new blog post |
| `GET` | `/api/posts/{id}/` | Retrieve a specific blog post with comments |
| `POST` | `/api/posts/{id}/comments/` | Add a comment to a blog post |

## Technology Stack

- **Backend**: Django 4.2 + Django REST Framework 3.14
- **Database**: PostgreSQL (production) / SQLite (development)
- **Containerization**: Docker + Docker Compose
- **Testing**: pytest-django
- **Code Quality**: Production-ready with unit tests

Environment used to develop and test: Ubuntu 22.04 WSL 2 Distribution

## Architecture

```
blog_api/
├── blog_project/          # Django project configuration
│   ├── settings.py        # Environment-based settings
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI application
├── blog_app/             # Main application
│   ├── models.py         # Data models (BlogPost, Comment)
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views
│   ├── urls.py           # API URL routing
│   ├── admin.py          # Django admin configuration
│   └── tests.py          # Comprehensive test suite
└── manage.py             # Django management commands
```

## Quick Start

**Three commands to get started:**

```bash
# 1. Complete setup (install deps, create DB, configure everything)
./setup.sh setup

# 2. Start the API server
./setup.sh run

# 3. Run all tests
./setup.sh test-all
```

**Swagger UI** available at http://localhost:8000/swagger/

### Additional Commands

```bash
./setup.sh superuser  # Create admin user for http://localhost:8000/admin/
./setup.sh docker     # Alternative: run with Docker Compose
./setup.sh help       # Show all available commands
```

## Alternative Setup Options

### Option 1: Docker (No Dependencies Required)

```bash
docker-compose up --build
```
- Zero local setup required
- PostgreSQL database included
- Production-like environment

### Option 2: Manual Setup

1. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp env.example blog_api/.env
   # Edit .env with your settings
   ```

3. **Set up database**
   ```bash
   cd blog_api
   python manage.py migrate
   python manage.py createsuperuser  # Optional: for admin access
   ```

4. **Run the server**
   ```bash
   python manage.py runserver
   ```

## Testing

Run the comprehensive test suite:

```bash
cd blog_api
pytest

or

./setup.sh test-all # All test with coverage results
```

**Test Coverage**: 95%+ with unit, integration, and API tests.

### API Testing

#### Create a Blog Post
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post."
  }'
```

#### List All Posts
```bash
curl http://localhost:8000/api/posts/
```

#### Get Specific Post
```bash
curl http://localhost:8000/api/posts/1/
```

#### Add Comment to Post
```bash
curl -X POST http://localhost:8000/api/posts/1/comments/ \
  -H "Content-Type: application/json" \
  -d '{
    "author_name": "John Doe",
    "content": "Great post!"
  }'
```

## Sample API Response

**GET /api/posts/1/**
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "comment_count": 2,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "comments": [
    {
      "id": 1,
      "author_name": "Marlon Zanardi",
      "content": "Great post!",
      "created_at": "2024-01-15T11:00:00Z"
    },
    {
      "id": 2,
      "author_name": "Jane Smith",
      "content": "Very informative!",
      "created_at": "2024-01-15T12:00:00Z"
    }
  ]
}
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `False` |
| `SECRET_KEY` | Django secret key | Required |
| `DATABASE_URL` | Database connection URL | SQLite |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |



## Production Deployment

### Docker Production Build

```bash
# Build production image
docker build -t blog-api:production .

# Run with production settings
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=your-production-secret \
  -e DATABASE_URL=postgresql://... \
  blog-api:production
```

### Security Checklist

- Secret key properly configured
- Debug mode disabled in production
- Database connections secured
- CORS properly configured
- Input validation on all endpoints


## Next Steps

If I had additional time, I would implement:

1. **Authentication & Authorization**
   - JWT token authentication
   - User roles and permissions
   - Author-based post management

2. **Advanced Features**
   - Full-text search for posts
   - Post categories and tags
   - Image uploads for posts
   - Comment threading/replies

### Screeshots
```bash
GET http://localhost:8000/api/posts/
```
<img width="588" height="670" alt="image" src="https://github.com/user-attachments/assets/f2b69ca3-c3b6-47ec-b6dd-9721c2ea3bfe" />

```bash
GET http://localhost:8000/api/posts/1
```
<img width="611" height="791" alt="image" src="https://github.com/user-attachments/assets/c31b883d-15ca-4dcb-a0c2-34d5de94771a" />

```bash
POST http://localhost:8000/api/posts/
```
<img width="641" height="568" alt="image" src="https://github.com/user-attachments/assets/d0cc596a-1112-4752-8cb8-23d20bd9577d" />

```bash
POST http://localhost:8000/api/posts/](http://localhost:8000/api/posts/2/comments/
```
<img width="637" height="515" alt="image" src="https://github.com/user-attachments/assets/0982ee4d-1920-4bca-8871-03d95bb20f60" />

```bash
./setup.sh test-all
```
<img width="437" height="545" alt="image" src="https://github.com/user-attachments/assets/ee348b19-3e8a-406d-af3e-46ce4f1b5ebb" />

```bash
http://localhost:8000/admin/
```
![admin-portal](https://github.com/user-attachments/assets/0a6f3401-5cce-4d6e-aaab-0f57fc659b98)

```bash
http://localhost:8000/swagger/
```
<img width="1716" height="716" alt="image" src="https://github.com/user-attachments/assets/3a05418c-f69f-4aba-824c-7b259b63df04" />



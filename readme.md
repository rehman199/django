# Django REST API Starter Template

A production-ready Django REST Framework starter template with JWT authentication and Celery integration for asynchronous task processing.

## Features

- 🔐 JWT Authentication using `djangorestframework-simplejwt`
- 🚀 Celery integration for background tasks
- 🔄 REST API using Django REST Framework
- 🛡️ Secure by default configuration

## Prerequisites

- Python 3.8+
- Redis (for Celery)
- PostgreSQL

## Quick Start

1. Clone the repository

```bash
git clone https://github.com/rehman199/django
cd django
```

2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate
# On Windows use: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations

```bash
python manage.py migrate
```

6. Start the development server

```bash
python manage.py runserver
```

7. Start Celery worker

```bash
celery -A django worker -l info
```

## API Endpoints

### Authentication

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and obtain JWT tokens
- `POST /api/auth/token/refresh` - Refresh JWT token
- `POST /api/auth/verify-email` - Verify user's email address
- `GET /api/auth/me` - Get current user's details
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/reset-password` - Request password reset
- `POST /api/auth/reset-password/verify` - Verify password reset token
- `POST /api/auth/reset-password/submit` - Submit new password

Each endpoint expects and returns JSON data. For detailed request/response formats, refer to the API documentation.

Note: All endpoints except `register`, `login`, and password reset-related endpoints require a valid JWT token in the Authorization header: `Authorization: Bearer <token>`.

## Celery Tasks

The project includes Celery for handling asynchronous tasks. Tasks can be found in the respective app directories under the `tasks.py` files.

## Development

1. Make sure all tests pass:

```bash
python manage.py test
```

2. Check code style:

```bash
flake8
```

## Deployment

This project is deployment-ready for platforms like:

- Heroku
- DigitalOcean
- AWS

Refer to the deployment documentation for platform-specific instructions.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

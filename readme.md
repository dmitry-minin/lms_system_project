LMS sysem project.
This system allows you to create courses, lessons, and manage users.

# Features
Cotains models:
- User
- Course
- Lesson
- Payments

Feature2:
- added lessons_count field to course serializer
- new model Payments(user, payment_date, course, lesson, amount, payment_method) - created


# Quick Start with Docker Compose
Start the Project
docker-compose up -d --build
Stop the Project
docker-compose down
Verify Services
Django App: http://localhost:8000
Admin Panel: http://localhost:8000/admin
Celery Worker: docker-compose logs -f celery_worker
Celery Beat: docker-compose logs -f celery_beat
Redis: docker-compose exec redis redis-cli ping
PostgreSQL: docker-compose exec db psql -U $DB_USER -d $DB_NAME -c "SELECT 1"
Common Commands
Create superuser: docker-compose exec lms_project python manage.py createsuperuser
Run migrations: docker-compose exec lms_project python manage.py migrate
View logs: docker-compose logs -f [service_name]
Troubleshooting
Check logs: docker-compose logs
Rebuild containers: docker-compose up -d --build
Clear volumes: docker-compose down -v

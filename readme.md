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


# Quick Start with Docker Compose (local)

Services (via docker-compose.yml):
- Django app: lms_project (port 8000 inside, proxied by nginx)
- PostgreSQL: db (exposed on 5434 locally)
- Redis: redis (exposed on 6379 locally)
- Celery worker: celery_worker
- Celery beat: celery_beat
- Nginx: nginx (exposes 80 locally and proxies to lms_project:8000)

Start the project
- docker compose up -d --build

Stop the project
- docker compose down

Verify services
- App via nginx: http://localhost
- Admin: http://localhost/admin
- Django direct (dev only): http://localhost:8000
- Celery Worker logs: docker compose logs -f celery_worker
- Celery Beat logs: docker compose logs -f celery_beat
- Redis: docker compose exec redis redis-cli ping
- PostgreSQL: docker compose exec db psql -U $DB_USER -d $DB_NAME -c "SELECT 1"

Common commands
- Create superuser: docker compose exec lms_project python manage.py createsuperuser
- Run migrations: docker compose exec lms_project python manage.py migrate
- Collect static: docker compose exec lms_project python manage.py collectstatic --noinput
- View logs: docker compose logs -f [service_name]

Troubleshooting
- Check logs: docker compose logs
- Rebuild containers: docker compose up -d --build
- Clear volumes: docker compose down -v


# CI/CD and Deployment to a Remote Server (GitHub Actions)

Workflow file: `.github/workflows/ci.yml`

Pipeline stages
- test: runs Poetry install, prepares CI .env, runs migrations and tests with coverage (artifact `coverage.xml`).
- lint: flake8, isort --check, black --check.
- build: builds and pushes Docker image to Docker Hub with tags `:latest` and `:${{ github.sha }}`.
- deploy: SSH to server, clones/updates repo at the target commit, copies server `.env` next to `docker-compose.yml`, runs `docker compose up -d`, then `migrate` and `collectstatic` inside `lms_project`.

One-time server preparation
1) Install Docker + Compose V2 and ensure Docker is running.
2) Create directory for environment file and put .env there (example keys, without secrets in Git):
   - Path used by workflow: `/root/lms_app_test/.env`
   - Required keys include: SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, CELERY_BROKER_URL, CELERY_RESULT_BACKEND, email credentials as needed.
   - For Compose stack: typically `DB_HOST=db`, `DB_PORT=5432`, `CELERY_BROKER_URL=redis://redis:6379/0`, `CELERY_RESULT_BACKEND=redis://redis:6379/0`.
3) Create GitHub repository secrets (Settings → Secrets and variables → Actions):
   - DOCKER_HUB_USERNAME
   - DOCKER_HUB_ACCESS_TOKEN
   - SSH_KEY (private key, OpenSSH format)
   - SSH_USER (e.g. `dmitry`)
   - SERVER_IP (e.g. `51.250.44.255`)

How deploy works
- The workflow connects to the server, ensures repo at `/root/lms_app_repo` is on the current commit, copies `/root/lms_app_test/.env` to `/root/lms_app_repo/.env` (so env_file: .env works), then executes:
  - `docker compose pull || true`
  - `docker compose up -d --remove-orphans`
  - `docker compose exec -T lms_project python manage.py migrate --noinput`
  - `docker compose exec -T lms_project python manage.py collectstatic --noinput`

Triggering deploy
- Any push or pull request runs test + lint; on success build runs, and then deploy.
- To limit deploy to a specific branch, add an `if:` condition to the `deploy` job (not enabled by default).

Server URL
- Application via nginx (production): `http://<SERVER_IP>/`
- Admin: `http://<SERVER_IP>/admin/`

What not to commit
- `.env`, virtual environments, caches, `__pycache__`, IDE folders — covered by `.gitignore`.
- Keep `.env.sample` in the repo with variable names only (no secrets).

Local development note
- For convenience, the Django container also exposes `8000:8000`. In production access should go through nginx on port 80.

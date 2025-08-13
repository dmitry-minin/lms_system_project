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




## CI/CD and Deployment to a Remote Server (GitHub Actions)

Below are the steps to prepare the server and enable automatic deployment after tests pass.

### 1) Server preparation (one-time)
- Install Docker and start the service:
  - Ubuntu: `sudo apt update && sudo apt install -y docker.io`
  - `sudo systemctl enable --now docker`
- (Optional) Allow your user to run Docker without sudo:
  - `sudo usermod -aG docker $USER` then re-login, or keep using `sudo docker ...`.
- Create a directory for the env file:
  - `sudo mkdir -p /root/lms_app_test`
- Create the environment file for the container (example):
  - `sudo tee /root/lms_app_test/.env > /dev/null <<'EOF'
SECRET_KEY=...
DEBUG=0
ALLOWED_HOSTS=51.250.44.255

DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=51.250.44.255
DB_PORT=5433

STRIPE_SECRET_KEY=...
CELERY_BROKER_URL=redis://51.250.44.255:6379/0
CELERY_RESULT_BACKEND=redis://51.250.44.255:6379/0

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
DEFAULT_FROM_EMAIL=...
EOF`

Notes:
- `.env` may only contain lines in `KEY=VALUE` format or comments starting with `#`.
- If Postgres/Redis are on the same server, ensure they listen on the external interface (server IP) and not only on `127.0.0.1`.

### 2) GitHub Secrets
Create repository secrets: Settings → Secrets and variables → Actions → New repository secret
- `DOCKER_HUB_USERNAME` — your Docker Hub username
- `DOCKER_HUB_ACCESS_TOKEN` — Docker Hub access token with Read/Write
- `SSH_KEY` — private SSH key (multiline OpenSSH format, no passphrase)
- `SSH_USER` — server user (e.g., `dmitry`)
- `SERVER_IP` — server IP (e.g., `51.250.44.255`)

### 3) How the workflow works
File: `.github/workflows/ci.yml`
- Triggers on every `push` and `pull_request`.
- Job `test`:
  - Starts Postgres service.
  - Installs dependencies via Poetry.
  - Creates a CI `.env`.
  - Runs migrations and tests with coverage (artifact `coverage.xml`).
- Job `build` (after tests):
  - Logs in to Docker Hub and builds/pushes the image: `DOCKER_HUB_USERNAME/myapp:<sha>`, and `:latest`.
- Job `deploy` (after build):
  - SSH to the server.
  - Runs `docker login`, `pull`, stops and removes `myapp` container if exists, then starts a new one:
    - Publishes port `80:8000`.
    - Uses env file: `/root/lms_app_test/.env`.
  - Falls back to `sudo docker` if the user has no direct access to the Docker daemon.

(Optional) Restrict deployment to a branch by adding to `deploy` job:
```
if: github.ref == 'refs/heads/main'
```
(or replace `main` with `develop`, etc.).

### 4) Run and rollback
- Any `push` runs tests; on success it builds and deploys.
- Check the container on the server:
  - `sudo docker ps -a | grep myapp`
  - Logs: `sudo docker logs -f myapp`
- Restart container manually:
  - `sudo docker restart myapp`
- Stop and remove:
  - `sudo docker stop myapp || true && sudo docker rm myapp || true`

### 5) Troubleshooting
- Error `invalid env file`: ensure `.env` has only `KEY=VALUE` lines and no CRLF. Remove CR: `sudo sed -i 's/\r$//' /root/lms_app_test/.env`.
- No access to Docker: add your user to the `docker` group or use `sudo docker`.
- DB/Redis connectivity: ensure services listen on server IP and ports are reachable from the container.
- Port 80 is busy: change port mapping in the workflow to `-p 8000:8000` and open `http://SERVER_IP:8000`.

### 6) What not to commit
- `.env`, virtual environments, caches, etc. — already covered by `.gitignore`.
- Keep an `.env.sample` listing keys without secrets in the repo instead.

### 7) Local development (reminder)
See the "Quick Start with Docker Compose" section above for local `docker-compose` usage.

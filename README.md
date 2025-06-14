# Secure File Storage & Sharing System

A Django-based secure file storage and sharing system with built-in authentication, access control, virus scanning, and expiring public links. This project is ideal for learning how to build security-focused web applications using Django and related tools.

---

## 🔐 Features

- **User Authentication:** Token-based authentication with JWT.
- **Secure File Upload:** Files scanned using ClamAV for viruses before saving.
- **File Access Control:** Files are only accessible to their owners or via valid share links.
- **Expiring Public Links:** Generate shareable URLs with expiration time.
- **Download Monitoring:** Logs file download events including user and timestamp.
- **Centralized Logging:** Logs warnings and suspicious actions to `access.log`.
- **Rate Limiting:** (Optional enhancement) Rate limiting to prevent abuse.
- **Security Testing:** Automated test suite with Django's `TestCase` and `coverage.py`.

---

## 🛠 Tech Stack

- **Backend:** Python, Django, Django REST Framework (DRF)
- **Security:** ClamAV, JWT, Middleware for access logging
- **Testing:** Django TestCase, Coverage.py
- **Task Queue:** Celery + Redis (for async virus scanning)

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/secure-file-storage.git
cd secure-file-storage

#2.Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # on Windows use: venv\Scripts\activate

#3. Install dependencies
pip install -r requirements.txt

#4. Setup environment variables (Optional)
#Create a .env file for secret settings:

SECRET_KEY=your_django_secret_key
DEBUG=True

#5. Apply migrations
python manage.py migrate

#6. Run the server
python manage.py runserver

#Run Tests & Coverage
coverage run manage.py test
coverage report


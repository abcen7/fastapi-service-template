# 🚀 FastAPI Service Template

[![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/github/license/abcen7/fastapi-service-template?style=for-the-badge)](LICENSE)

A clean, modular, and ready-to-use FastAPI template for building scalable microservices.

---

## 📖 Overview

This template simplifies the creation of FastAPI-based backend services with pre-configured tools for efficient development:

- **FastAPI** for modern, fast, and intuitive APIs.
- **Docker & Docker Compose** for containerized environments.
- **Pydantic Settings** for flexible configuration.
- **Async SQLAlchemy & PostgreSQL** integration out-of-the-box.
- Structured codebase optimized for readability and maintainability.

## ✨ Features

- ✅ Fully asynchronous design for performance.
- ✅ Robust configuration management using `.env` files.
- ✅ Database integration with async support.
- ✅ Automatic documentation with Swagger UI.
- ✅ Docker support for easy deployment.

## 🛠️ Tech Stack

- **Python 3.11**
- **FastAPI**
- **Async SQLAlchemy & PostgreSQL**
- **Pydantic**
- **Docker & Docker Compose**

## 🚧 Project Structure

```text
fastapi-service-template/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core application logic
│   ├── db/             # Database connection and models
│   ├── schemas/        # Data validation schemas
│   └── services/       # Business logic and services
├── tests/              # Unit tests
├── .env.example        # Environment variable example
├── Dockerfile
└── docker-compose.yml
```

## 🚀 Getting Started

### Clone the repository:
```bash
git clone https://github.com/abcen7/fastapi-service-template.git
```

### Configure environment variables:

Copy `.env.example` to `.env` and update values:
```bash
cp .env.example .env
```

### Build & Run with Docker Compose:
```bash
docker-compose up --build
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to view your API documentation.

## 🧪 Running Tests

Run unit tests easily using:
```bash
docker-compose run app pytest
```

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

Made with ❤️ by [abcen7](https://github.com/abcen7)

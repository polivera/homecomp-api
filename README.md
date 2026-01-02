# HomeComp API

A production-ready RESTful API for personal finance management built with **FastAPI** and **Domain-Driven Design** principles. This project demonstrates modern Python backend development practices, including clean architecture, CQRS patterns, and comprehensive structured logging.

## Overview

HomeComp API is a backend service designed to help users track household finances, including bank accounts, credit cards, recurring entries (income/expenses), and household management. The application follows strict architectural boundaries through DDD, ensuring maintainable and testable code.

## Key Features

- **Authentication System**: Session-based authentication with login throttling and account lockout protection
- **User Account Management**: CRUD operations for bank accounts with multi-currency support
- **Credit Card Tracking**: Manage credit cards with payment limits and billing cycles
- **Entry Management**: Track income and expenses across accounts and credit cards
- **Household Management**: Organize accounts and cards by household
- **Structured Logging**: Production-ready logging with Loki integration and Grafana visualization

## Technology Stack

### Core Technologies
- **Python 3.13+** - Modern Python with latest features
- **FastAPI 0.125** - High-performance async web framework
- **SQLAlchemy 2.0** - Async ORM with type safety
- **PostgreSQL 16** - Production database
- **Alembic** - Database migration management

### Security & Infrastructure
- **Argon2** - Modern password hashing algorithm
- **Structlog** - Structured logging for observability
- **UV** - Fast Python package manager
- **Docker Compose** - Local development environment

## Architecture Highlights

### Domain-Driven Design (DDD)

The codebase is organized into **bounded contexts**, each with a strict 4-layer architecture:

```
📁 app/context/{context_name}/
├── 📂 domain/              # Core business logic (framework-agnostic)
│   ├── contracts/          # Service interfaces
│   ├── services/           # Business rules
│   ├── value_objects/      # Immutable validated objects
│   └── dto/               # Domain data transfer objects
│
├── 📂 application/         # Use case orchestration (CQRS)
│   ├── commands/          # Write operations
│   ├── queries/           # Read operations
│   └── handlers/          # Command/query handlers
│
├── 📂 infrastructure/      # External concerns
│   ├── repositories/      # Data access implementations
│   ├── models/           # SQLAlchemy ORM models
│   └── mappers/          # DTO ↔ Model conversion
│
└── 📂 interface/          # External interfaces
    └── rest/             # REST API layer
        ├── controllers/   # Route handlers
        └── schemas/      # Request/response models
```

### CQRS (Command Query Responsibility Segregation)

- **Commands** - Write operations (CreateAccountCommand, UpdateCardCommand)
- **Queries** - Read operations (FindAccountQuery, ListCardsQuery)
- **Handlers** - Process commands/queries with error handling via Result pattern

### Key Patterns

- **Repository Pattern** - All data access abstracted behind contracts
- **Mapper Pattern** - Clean separation between domain and persistence layers
- **Value Objects** - Type-safe, validated domain primitives (Email, Currency, Money)
- **Dependency Injection** - FastAPI's DI system for loose coupling
- **Result Pattern** - Type-safe error handling without exceptions in application layer

## Project Structure

```
homecomp-api/
├── app/
│   ├── context/                    # Bounded contexts
│   │   ├── auth/                  # Authentication & authorization
│   │   ├── user_account/          # Bank account management
│   │   ├── credit_card/           # Credit card tracking
│   │   ├── entry/                 # Income/expense entries
│   │   └── household/             # Household management
│   │
│   ├── shared/                    # Shared kernel
│   │   ├── domain/               # Shared value objects & contracts
│   │   └── infrastructure/       # Database, logging, middleware
│   │
│   └── main.py                   # Application entry point
│
├── migrations/                    # Alembic database migrations
├── tests/                        # Unit and integration tests
├── docs/                         # Architecture documentation
├── docker/                       # Docker configurations
│   ├── loki/                     # Loki config
│   ├── promtail/                 # Promtail config
│   └── grafana/                  # Grafana dashboards
├── Dockerfile                    # Multi-stage production image
├── docker-compose.yml            # Complete development stack
├── .dockerignore                 # Docker build exclusions
├── justfile                      # Development commands
└── pyproject.toml               # Project dependencies (UV)
```

## Getting Started

### Prerequisites

- Python 3.13 or higher
- Docker & Docker Compose
- UV package manager ([installation guide](https://github.com/astral-sh/uv))
- Just command runner (optional) ([installation guide](https://github.com/casey/just))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/homecomp-api.git
   cd homecomp-api
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Start PostgreSQL**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   just migrate
   # or: uv run alembic upgrade head
   ```

5. **Start the development server**
   ```bash
   just run
   # or: uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
   ```

The API will be available at:
- **API**: http://localhost:8080
- **Interactive Docs**: http://localhost:8080/docs (Swagger UI)
- **ReDoc**: http://localhost:8080/redoc

### Docker Deployment (Recommended)

The easiest way to run the entire stack (API + PostgreSQL + Valkey + Logging) is with Docker Compose:

1. **Clone the repository**
   ```bash
   git clone https://github.com/polivera/homecomp-api.git
   cd homecomp-api
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and start all services**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec api uv run alembic upgrade head
   ```

The application stack will be available at:
- **API**: http://localhost:8090
- **Interactive Docs**: http://localhost:8090/docs
- **Grafana**: http://localhost:3000 (admin/admin)
- **PostgreSQL**: localhost:5432

**Useful Docker commands:**
```bash
# View logs
docker-compose logs -f api

# Rebuild after code changes
docker-compose up -d --build api

# Stop all services
docker-compose down

# Stop and remove volumes (reset database)
docker-compose down -v
```

### Environment Configuration

Create a `.env` file in the project root:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=uhomecomp
DB_PASS=homecomppass
DB_NAME=homecomp

# Application
APP_ENV=dev  # dev, test, or production
```

## API Documentation

Once the server is running, explore the API through:

- **Swagger UI**: http://localhost:8080/docs - Interactive API testing
- **ReDoc**: http://localhost:8080/redoc - Clean API documentation

### Available Endpoints

#### Authentication (`/api/auth`)
- `POST /api/auth/login` - User login with session creation

#### User Accounts (`/api/user-accounts`)
- `POST /api/user-accounts` - Create a new account
- `GET /api/user-accounts` - List all user accounts
- `GET /api/user-accounts/{id}` - Get account details
- `PUT /api/user-accounts/{id}` - Update account information
- `DELETE /api/user-accounts/{id}` - Delete an account

#### Credit Cards (`/api/credit-cards`)
- Full CRUD operations for credit card management

#### Entries (`/api/entries`)
- Income and expense tracking across accounts and cards

#### Households (`/api/households`)
- Household organization and management

## Development

### Local Development (Without Docker)

For local development without Docker, ensure PostgreSQL is running separately:

```bash
# Start development server with hot reload
just run
# or: uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov

# Generate new migration
just migration-generate "description of changes"

# Run pending migrations
just migrate

# Connect to PostgreSQL CLI
just pgcli

# Format code
uv run ruff format

# Lint code
uv run ruff check
```

### Docker Development

When using Docker Compose, the API has hot-reload enabled via volume mounting:

```bash
# Start all services in development mode
docker-compose up -d

# View API logs (with hot-reload feedback)
docker-compose logs -f api

# Run migrations inside container
docker-compose exec api uv run alembic upgrade head

# Run tests inside container
docker-compose exec api uv run pytest

# Access Python shell inside container
docker-compose exec api uv run python

# Rebuild after dependency changes
docker-compose up -d --build api
```

### Database Migrations

```bash
# Create a new migration
just migration-generate "add_user_preferences_table"

# Apply migrations
just migrate

# Rollback one migration
uv run alembic downgrade -1
```

## Testing

The project uses pytest with async support:

```bash
# Run all tests
uv run pytest

# Run unit tests only
uv run pytest -m unit

# Run integration tests only
uv run pytest -m integration

# Run with coverage report
uv run pytest --cov --cov-report=html
```

## Architecture Decisions

### Why DDD?

Domain-Driven Design provides:
- **Clear boundaries** - Each context owns its data and logic
- **Testability** - Domain logic is framework-agnostic
- **Maintainability** - Changes are localized to bounded contexts
- **Team scalability** - Contexts can be worked on independently

### Why CQRS?

Command Query Responsibility Segregation offers:
- **Separation of concerns** - Read and write models can evolve independently
- **Optimized queries** - Read operations don't need full domain logic
- **Clear intent** - Commands vs queries make code easier to understand

### Why Value Objects?

Type-safe value objects provide:
- **Compile-time validation** - Invalid data can't exist in the domain
- **Self-documenting code** - `Email` is clearer than `str`
- **Encapsulation** - Validation logic lives in one place

### Why Repository Pattern?

Repositories offer:
- **Testability** - Easy to mock data access
- **Flexibility** - Can swap ORMs or databases without changing domain
- **Abstraction** - Domain doesn't depend on SQLAlchemy

## Logging & Observability

The application uses **structlog** with:
- Structured JSON logging for production
- Colored console logs for development
- Loki integration for log aggregation
- Grafana dashboards for visualization

All logs include contextual information (user_id, email, operation) making debugging and monitoring straightforward.

## Security Features

- **Argon2 password hashing** - Memory-hard algorithm resistant to GPU attacks
- **Session-based authentication** - Secure token management with expiration
- **Login throttling** - Progressive delays to prevent brute-force attacks
- **Account lockout** - Temporary blocks after failed login attempts
- **Input validation** - Pydantic models validate all request data
- **SQL injection protection** - SQLAlchemy ORM with parameterized queries

## Contributing

This is a personal portfolio project, but suggestions and feedback are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## What I Learned

Building this project taught me:

- **Clean Architecture** - Strict layer dependencies and separation of concerns
- **Async Python** - Modern async/await patterns with FastAPI and SQLAlchemy 2.0
- **Type Safety** - Comprehensive type hints and domain-driven value objects
- **Production Practices** - Structured logging, error handling, and observability
- **Database Design** - Alembic migrations, PostgreSQL optimization, and async sessions
- **Testing Strategy** - Unit vs integration tests with proper mocking
- **API Design** - RESTful conventions and comprehensive OpenAPI documentation

## Future Enhancements

- [ ] Credit card expenses tracking
- [ ] JWT-based authentication as an alternative to sessions
- [ ] Real-time notifications via WebSockets
- [ ] Budget planning and forecasting features
- [ ] Data export/import (CSV, JSON)
- [ ] Multi-tenancy support for household sharing
- [ ] Mobile app integration
- [ ] Shared account for household

## License

This project is open source and available under the MIT License.

## Contact

**Pablo** - [GitHub](https://github.com/polivera)

---

Built with ❤️ using FastAPI, DDD, and modern Python practices.

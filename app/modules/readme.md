# The Key Components and Their Responsibilities

| Component      | Layer          | Responsibility                          | FastAPI Equivalent       | Example Contents                          |
|---------------|----------------|----------------------------------------|-------------------------|------------------------------------------|
| **Entity**    | Database Layer | Pure database representation           | SQLAlchemy Model        | `id`, `created_at`, field definitions    |
| **DTO**       | API Layer      | Data transfer shape for API            | Pydantic Model          | Input validation, serialization rules    |
| **Model**     | Business Layer | Domain business objects                | Python class (optional) | Business logic methods                   |

## Key Conversion Points

1. **API → Service**:
   - Controller receives DTO
   - Service converts DTO to Entity data for repository

2. **Repository → Service**:
   - Returns Entity
   - Service converts to Business Model

3. **Service → API**:
   - Converts Model/Entity to Response DTO

## When to Use Business Models?

For simple CRUD apps, you can often skip the business model layer and work directly with Entities and DTOs. Add business models when:

1. You have complex business logic
2. Your domain objects behave differently than storage
3. You need to enforce business rules

## Team Workflow Recommendation

1. **Frontend-focused devs**: Work primarily with DTOs and controllers
2. **Backend-focused devs**: Work with services, models, repositories
3. **Database experts**: Focus on entities and migrations

This separation naturally creates boundaries where team members can work without stepping on each other's code.

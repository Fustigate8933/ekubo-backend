# GitHub Copilot Instructions

## Project Overview
- **Purpose**: Ekubo is a Japanese listening practice application backend API that manages songs, lyrics, user libraries, and practice progress for improving Japanese listening skills through music.
- **Tech Stack**: FastAPI, Python 3.13, Supabase (via REST API)

## Coding Standards

### General Guidelines
- Use Python 3.13+ features and type hints
- Follow PEP 8 style guidelines
- Write meaningful variable and function names using snake_case
- Add docstrings for modules, classes, and complex functions
- Use async/await for all I/O operations

### FastAPI Specific
- Define Pydantic models in `/models` directory, organized by domain
- Use dependency injection for shared resources
- Implement proper error handling with HTTPException
- Use response_model in route decorators for automatic validation
- Keep router files focused on HTTP handling, delegate business logic to services

### Error Handling
- Use HTTPException with appropriate status codes
- Provide clear error messages in the `detail` field
- Wrap service calls in try-except blocks
- Log errors appropriately for debugging

## Project Structure
```
/models         # Pydantic schemas for request/response validation
/routers        # FastAPI route handlers organized by domain
/services       # Business logic and external API integrations
/tests          # Unit and integration tests
main.py         # Application entry point and router configuration
config.py       # Application settings and environment variables
```

## Testing Guidelines
- Use the provided `test_api.sh` script for endpoint testing
- Test with curl commands from `curl_examples.md`
- Run development server: `python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- Access interactive docs at `http://localhost:8000/docs`
- Aim for meaningful test coverage over arbitrary percentages
- Do not fix tests without understanding the root cause

## Common Patterns

### API Routes
- Legacy routes: `/songs`, `/auth` (for backward compatibility)
- New API routes: `/api/songs`, `/api/lyrics`, `/api/matched`, `/api/library`
- Use descriptive endpoint names and proper HTTP methods
- Include query parameters with Query() for validation and documentation

### Database Operations
- Use `SupabaseService` for all database operations
- All database methods are async
- Common operations: `get()`, `get_multi()`, `create()`, `update()`, `delete()`, `search()`
- Use `search_with_pattern()` for ILIKE queries

### External API Integration
- Spotify API: `search_spotify_song()`, `get_spotify_access_token()`
- LRCLIB API: `fetch_lyrics()`
- Use httpx.AsyncClient for all HTTP requests
- Implement proper error handling for external API failures

### Response Models
- Use Pydantic BaseModel with `ConfigDict(from_attributes=True)`
- Create separate schemas for Create, Update, Response, and WithDetails
- Export all models from `models/__init__.py`
- Use Optional[] for nullable fields, Field() for validation

## Build and Development
- Dockerfile included for containerized deployment
- Heroku deployment configured via `heroku.yml`
- Dependencies managed in `requirements.txt`
- Port configured via PORT environment variable (default: 8000)
- Run `python -m uvicorn main:app --reload` for development
- Run `python test_api.sh` to test endpoints

## Important Notes
- Always review generated code for accuracy and adherence to standards
- Always validate user input with Pydantic models
- Use async/await consistently throughout the codebase
- Handle database connection errors gracefully
- Implement proper CORS middleware for frontend integration
- Follow RESTful conventions for API design
- Return appropriate HTTP status codes (200, 201, 400, 404, 500)

### Authentication
- JWT tokens generated with `jwt.encode()`
- Password hashing using bcrypt
- User data stored in Supabase `users` table
- Auth endpoints: `/auth/signup`, `/auth/login`
- JWT_SECRET environment variable required

### Environment Variables
Required in `.env`:
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase API key
- `JWT_SECRET`: Secret key for JWT signing
- `SPOTIFY_CLIENT_ID`: Spotify API client ID
- `SPOTIFY_CLIENT_SECRET`: Spotify API client secret

### Database Schema
Key tables:
- `songs`: Song metadata (title, artist, album, spotify_id)
- `lyrics`: Synced lyrics content
- `lyric_lines`: Individual parsed lyric lines with timestamps
- `matched`: Song-lyrics pairings
- `user_library`: User's saved songs
- `users`: User accounts and authentication
- `user_progress`: Practice session tracking

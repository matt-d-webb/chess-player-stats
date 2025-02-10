# Chess Stats API

A FastAPI-based REST API for retrieving and analyzing chess player statistics. This API provides endpoints for accessing player information, ratings, and various statistical analyses across different chess formats (standard, rapid, and blitz).

## Features

- Player lookup by FIDE ID
- Search players by name, country, rating range, and title
- Country-specific statistics and top players
- Rating distribution analysis
- Titled player statistics
- Support for standard, rapid, and blitz ratings
- Caching for improved performance
- Database indexing for efficient queries

## Tech Stack

- Python 3.9+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pandas
- Docker

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 14 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/chess-stats-api.git
cd chess-stats-api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file (see `.env.template` for reference) and set your environment variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/chess_players
DEBUG=False
```

5. Initialize the database:

```bash
python -c "from app.database import init_db; init_db()"
```

6. Import chess player data:

```bash
python -c "from app.database import import_xml; import_xml('path/to/your/players.xml')"
```

## Running the API

### Development

```bash
uvicorn app.main:app --reload
```

### Production

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Docker Deployment

1. Build the image:

```bash
docker build -t chess-stats-api .
```

2. Run with Docker Compose:

```bash
docker-compose up -d
```

## API Documentation

Once the server is running, you can access:

- Interactive API documentation: `http://localhost:8000/docs`
- Alternative documentation: `http://localhost:8000/redoc`

## API Endpoints

- `GET /api/v1/player/{fide_id}` - Get player by FIDE ID
- `GET /api/v1/search` - Search players with filters
- `GET /api/v1/country/{country}/top` - Get top players by country
- `GET /api/v1/country/{country}/stats` - Get statistics for a country
- `GET /api/v1/rating-distribution` - Get rating distribution
- `GET /api/v1/titled-players/stats` - Get titled players statistics

## Acknowledgments

- FIDE for providing the chess player data
- The FastAPI and SQLAlchemy communities for their excellent tools

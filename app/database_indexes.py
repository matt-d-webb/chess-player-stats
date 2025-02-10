# app/database_indexes.py
from sqlalchemy import text
from app.database import engine

def create_indexes():
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_country ON players(country)",
        "CREATE INDEX IF NOT EXISTS idx_rating ON players(rating DESC NULLS LAST)",
        "CREATE INDEX IF NOT EXISTS idx_title ON players(title)",
        "CREATE INDEX IF NOT EXISTS idx_name ON players(name)",
        "CREATE INDEX IF NOT EXISTS idx_birthday ON players(birthday)",
        "CREATE INDEX IF NOT EXISTS idx_country_rating ON players(country, rating DESC NULLS LAST)",
        "CREATE INDEX IF NOT EXISTS idx_title_rating ON players(title, rating DESC NULLS LAST)",
        "CREATE INDEX IF NOT EXISTS idx_rapid_rating ON players(rapid_rating DESC NULLS LAST)",
        "CREATE INDEX IF NOT EXISTS idx_blitz_rating ON players(blitz_rating DESC NULLS LAST)",
        "CREATE INDEX IF NOT EXISTS idx_sex ON players(sex)"
    ]
    
    with engine.connect() as conn:
        for idx in indexes:
            conn.execute(text(idx))
            conn.commit()
            print(f"Created index: {idx}")

if __name__ == "__main__":
    create_indexes()
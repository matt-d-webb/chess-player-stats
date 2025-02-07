from sqlalchemy import text
from app.database import engine

def create_indexes():
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_federation ON players(federation)",
        "CREATE INDEX IF NOT EXISTS idx_standard_rating ON players(standard_rating DESC NULLS LAST)",
        "CREATE INDEX IF NOT EXISTS idx_title ON players(title)",
        "CREATE INDEX IF NOT EXISTS idx_name ON players(name)",
        "CREATE INDEX IF NOT EXISTS idx_birth_year ON players(birth_year)",
        "CREATE INDEX IF NOT EXISTS idx_fed_rating ON players(federation, standard_rating DESC NULLS LAST)",
        "CREATE INDEX IF NOT EXISTS idx_title_rating ON players(title, standard_rating DESC NULLS LAST)"
    ]
    
    with engine.connect() as conn:
        for idx in indexes:
            conn.execute(text(idx))
            conn.commit()
            print(f"Created index: {idx}")

if __name__ == "__main__":
    create_indexes()
from sqlalchemy import create_engine, Column, Integer, String, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np

DATABASE_URL = "postgresql://matthew@localhost/chess_players" # Change to your database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PlayerDB(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    fide_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    federation = Column(String, index=True)
    sex = Column(String)
    title = Column(String)
    w_title = Column(String)
    o_title = Column(String)
    foa = Column(String)
    standard_rating = Column(Integer)
    standard_games = Column(Integer)
    standard_k = Column(Integer)
    rapid_rating = Column(Integer)
    rapid_games = Column(Integer)
    rapid_k = Column(Integer)
    blitz_rating = Column(Integer)
    blitz_games = Column(Integer)
    blitz_k = Column(Integer)
    birth_year = Column(Integer)
    flag = Column(String)

    __table_args__ = (
        Index('idx_federation_rating', 'federation', 'standard_rating'),
    )

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def import_txt(file_path):
    print("Starting file import...")
    
    try:
        rows = []
        with open(file_path, 'r') as file:
            # Skip header
            next(file)
            
            for line_num, line in enumerate(file, 1):
                try:
                    line = line.rstrip('\n')
                    
                    row = {
                        'fide_id': line[0:10].strip(),
                        'name': line[10:72].strip(),
                        'federation': line[72:75].strip(),
                        'sex': line[75:76].strip(),
                        'title': line[76:79].strip(),
                        'w_title': line[79:82].strip(),
                        'o_title': line[82:85].strip(),
                        'foa': line[85:88].strip(),
                        'standard_rating': line[88:94].strip() or None,
                        'standard_games': line[94:98].strip() or None,
                        'standard_k': line[98:100].strip() or None,
                        'rapid_rating': line[100:106].strip() or None,
                        'rapid_games': line[106:110].strip() or None,
                        'rapid_k': line[110:112].strip() or None,
                        'blitz_rating': line[112:118].strip() or None,
                        'blitz_games': line[118:122].strip() or None,
                        'blitz_k': line[122:124].strip() or None,
                        'birth_year': line[124:128].strip() or None,
                        'flag': line[128:].strip() if len(line) > 128 else None
                    }
                    
                    if row['federation'] and len(row['federation']) != 3:
                        print(f"Warning: Invalid federation code on line {line_num}: {row['federation']}")
                        continue
                        
                    rows.append(row)
                    
                    if line_num % 100000 == 0:
                        print(f"Processed {line_num} records...")
                        
                except Exception as e:
                    print(f"Error parsing line {line_num}: {line[:50]}... Error: {str(e)}")
                    continue

        print(f"Read {len(rows)} rows")
        
        df = pd.DataFrame(rows)
        
        numeric_cols = {
            'fide_id': 'Int64',
            'standard_rating': 'Int64',
            'standard_games': 'Int64',
            'standard_k': 'Int64',
            'rapid_rating': 'Int64',
            'rapid_games': 'Int64',
            'rapid_k': 'Int64',
            'blitz_rating': 'Int64',
            'blitz_games': 'Int64',
            'blitz_k': 'Int64',
            'birth_year': 'Int64'
        }
        
        for col, dtype in numeric_cols.items():
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(dtype)

        print("\nData validation:")
        print(f"Total rows: {len(df)}")
        print(f"Unique federations: {df['federation'].nunique()}")
        print(f"Players with ratings: {df['standard_rating'].notna().sum()}")
        print(f"Rating range: {df['standard_rating'].min()} - {df['standard_rating'].max()}")
        
        print("\nWriting to database...")
        df.to_sql('players', engine, if_exists='replace', index=True, index_label='id')
        print("Import completed successfully!")
        
        with engine.connect() as conn:
            result = conn.execute("SELECT COUNT(*) FROM players").scalar()
            print(f"\nVerified {result} records in database")
            
    except Exception as e:
        print(f"Error during import: {str(e)}")
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
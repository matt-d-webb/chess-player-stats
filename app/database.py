from sqlalchemy import create_engine, Column, String, Index, text, BigInteger, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get DATABASE_URL from environment variable, fallback to local for development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://matthew@localhost/chess_players"
)

# Render adds 'postgres://', but SQLAlchemy needs 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PlayerDB(Base):
    __tablename__ = "players"

    id = Column(BigInteger, primary_key=True)  # Added primary_key=True here
    fide_id = Column(BigInteger, unique=True, index=True)
    name = Column(String)
    country = Column(String, index=True)
    sex = Column(String)
    title = Column(String)
    w_title = Column(String)
    o_title = Column(String)
    foa_title = Column(String)
    rating = Column(Float)
    games = Column(Float)
    k = Column(Float)
    rapid_rating = Column(Float)
    rapid_games = Column(Float)
    rapid_k = Column(Float)
    blitz_rating = Column(Float)
    blitz_games = Column(Float)
    blitz_k = Column(Float)
    birthday = Column(Float)
    flag = Column(String)

    __table_args__ = (
        Index('idx_country_rating', 'country', 'rating'),
    )

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def import_xml(file_path):
    print("Starting XML import...")
    
    try:
        # Parse XML
        print("Parsing XML file...")
        tree = ET.iterparse(file_path, events=('end',))
        
        # Create list to store player data
        players = []
        count = 0
        
        # Process XML elements
        for event, elem in tree:
            if elem.tag == 'player':
                try:
                    player = {}
                    for child in elem:
                        # Convert empty strings to None for numeric fields
                        if child.text in ('', '0') and child.tag in [
                            'rating', 'games', 'k', 
                            'rapid_rating', 'rapid_games', 'rapid_k',
                            'blitz_rating', 'blitz_games', 'blitz_k',
                            'birthday', 'fideid'
                        ]:
                            player[child.tag] = None
                        else:
                            player[child.tag] = child.text.strip() if child.text else None
                    
                    players.append(player)
                    count += 1
                    
                    # Progress reporting
                    if count % 10000 == 0:
                        print(f"Processed {count} players...")
                    
                    # Clear element to save memory
                    elem.clear()
                except Exception as e:
                    print(f"Error processing player: {str(e)}")
                    continue
        
        print(f"\nProcessed total of {count} players")
        
        # Convert to DataFrame
        print("Converting to DataFrame...")
        df = pd.DataFrame(players)
        
        # Rename fideid column to fide_id to match our database schema
        df = df.rename(columns={'fideid': 'fide_id'})
        
        # Convert numeric columns
        numeric_cols = [
            'fide_id', 'rating', 'games', 'k',
            'rapid_rating', 'rapid_games', 'rapid_k',
            'blitz_rating', 'blitz_games', 'blitz_k',
            'birthday'
        ]
        
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Data validation
        print("\nData validation:")
        print(f"Total rows: {len(df)}")
        print(f"Unique countries: {df['country'].nunique()}")
        print("Country distribution:")
        print(df['country'].value_counts().head())
        print(f"\nPlayers with ratings: {df['rating'].notna().sum()}")
        if df['rating'].notna().any():
            print(f"Rating range: {df['rating'].min()} - {df['rating'].max()}")
        
        # Write to database
        print("\nWriting to database...")
        df.to_sql('players', engine, if_exists='replace', index=True, index_label='id')
        
        # Verify import
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM players")).scalar()
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
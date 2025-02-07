from app.database import init_db, import_csv
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python import_players.py <csv_file_path>")
        sys.exit(1)
        
    csv_path = sys.argv[1]
    print(f"Initializing database...")
    init_db()
    print(f"Importing data from {csv_path}...")
    import_csv(csv_path)
    print("Import completed!")

if __name__ == "__main__":
    main()
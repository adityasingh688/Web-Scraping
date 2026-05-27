import argparse
import csv
import os
import sys
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.models import ListingMaster  # noqa: E402


def database_url() -> str:
    load_dotenv(ROOT / ".env")
    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = os.getenv("MYSQL_PORT", "3306")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "password")
    database = os.getenv("MYSQL_DATABASE", "business_dashboard")
    return f"mysql+pymysql://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{database}?charset=utf8mb4"


def main():
    parser = argparse.ArgumentParser(description="Load CSV business listings into MySQL.")
    parser.add_argument("--csv", default="sample_listings.csv")
    args = parser.parse_args()

    engine = create_engine(database_url(), pool_pre_ping=True)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    with open(args.csv, newline="", encoding="utf-8") as csv_file:
        rows = [ListingMaster(**row) for row in csv.DictReader(csv_file)]

    session.add_all(rows)
    session.commit()
    session.close()
    print(f"Inserted {len(rows)} listings")


if __name__ == "__main__":
    main()

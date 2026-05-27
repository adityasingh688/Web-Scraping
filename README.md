# Business Listings Dashboard

Full-stack internship assignment solution using React, FastAPI, and MySQL.

The app stores business listings and shows dashboard summaries by city, category, and source. It includes a sample-data generator for 600 listings because many business directory websites block scraping or restrict automated extraction in their terms.

## Tech Stack

- Frontend: React.js, Vite, Recharts
- Backend: FastAPI, SQLAlchemy, PyMySQL
- Database: MySQL
- Data: Python sample-data generator with a scraper-ready structure

## Project Structure

```text
backend/
  app/
    main.py
    database.py
    models.py
    schemas.py
  database/
    schema.sql
    business_listings_dump.sql
  scripts/
    generate_sample_data.py
    load_sample_data.py
  requirements.txt
  .env.example
frontend/
  src/
    App.jsx
    api.js
    main.jsx
    styles.css
  package.json
```

## Database Setup

1. Create the database and table:

```sql
SOURCE backend/database/schema.sql;
```

2. Optional: load the SQL dump with generated sample data:

```sql
SOURCE backend/database/business_listings_dump.sql;
```

3. Or generate and load fresh sample data through the backend script:

```bash
cd backend
python scripts/generate_sample_data.py --count 600 --output sample_listings.csv
python scripts/load_sample_data.py --csv sample_listings.csv
```

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Update `.env` if your MySQL username, password, host, or database name is different.

FastAPI runs at:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

React runs at:

```text
http://127.0.0.1:5173
```

## APIs

### Health Check

```http
GET /health
```

### Bulk Insert Listings

```http
POST /api/listings/bulk
```

Request body:

```json
[
  {
    "business_name": "Apex Dental Care 1",
    "category": "Dental Clinic",
    "city": "Mumbai",
    "address": "12 MG Road, Mumbai",
    "phone": "+91 98765 43210",
    "source": "Justdial"
  }
]
```

### Dashboard Summary

```http
GET /api/dashboard/summary
```

Returns city-wise, category-wise, and source-wise counts.

## Scraping Approach

For a real production version, the scraper would:

1. Choose a business directory that allows automated collection.
2. Read listing cards from search/category pages.
3. Extract business name, category, city, address, phone, and source.
4. Normalize missing values and duplicate records.
5. Insert cleaned rows through the FastAPI bulk insert endpoint.

Because many sites such as Google Maps, Justdial, and Sulekha may restrict automated scraping, this project uses a reproducible sample-data generator. This keeps the assignment focused on the required logic, database design, APIs, and dashboard.

## Challenges Faced

- Business directory pages often use dynamic rendering and anti-bot protections.
- Phone numbers and addresses may be hidden until user interaction.
- Listing names can repeat across cities, so deduplication should use more than one field.
- Dashboard APIs need grouped queries that remain fast as the dataset grows.

## Demo Video Checklist

- Show the generated 600-listing dataset.
- Open MySQL and show `listing_master`.
- Run FastAPI and open `/docs`.
- Test the bulk insert or dashboard summary API.
- Run React dashboard and show city, category, and source charts.

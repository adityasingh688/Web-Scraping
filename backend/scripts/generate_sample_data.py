import argparse
import csv
import random


CITIES = [
    "Mumbai",
    "Delhi",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Lucknow",
]

CATEGORIES = [
    "Restaurant",
    "Dental Clinic",
    "Salon",
    "Gym",
    "Pharmacy",
    "Grocery Store",
    "Electronics Store",
    "Travel Agency",
    "Coaching Centre",
    "Real Estate Agency",
]

SOURCES = ["Google Maps", "Justdial", "Sulekha", "IndiaMART"]
AREAS = ["MG Road", "Station Road", "Link Road", "Park Street", "Ring Road", "Market Lane"]
PREFIXES = ["Apex", "Urban", "Prime", "Green", "Metro", "Royal", "Sunrise", "Classic"]


def phone_for(index: int) -> str:
    return f"+91 9{700000000 + index:09d}"


def build_rows(count: int) -> list[dict[str, str]]:
    rows = []
    for index in range(1, count + 1):
        city = CITIES[index % len(CITIES)]
        category = CATEGORIES[index % len(CATEGORIES)]
        source = SOURCES[index % len(SOURCES)]
        name = f"{random.choice(PREFIXES)} {category} {index}"
        address = f"{10 + index % 90}, {random.choice(AREAS)}, {city}"
        rows.append(
            {
                "business_name": name,
                "category": category,
                "city": city,
                "address": address,
                "phone": phone_for(index),
                "source": source,
            }
        )
    return rows


def main():
    parser = argparse.ArgumentParser(description="Generate sample business listings.")
    parser.add_argument("--count", type=int, default=600)
    parser.add_argument("--output", default="sample_listings.csv")
    args = parser.parse_args()

    random.seed(2026)
    rows = build_rows(args.count)
    with open(args.output, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows at {args.output}")


if __name__ == "__main__":
    main()

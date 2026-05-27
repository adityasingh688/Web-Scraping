CREATE DATABASE IF NOT EXISTS business_dashboard
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE business_dashboard;

DROP TABLE IF EXISTS listing_master;

CREATE TABLE listing_master (
  id INT AUTO_INCREMENT PRIMARY KEY,
  business_name VARCHAR(255) NOT NULL,
  category VARCHAR(120) NOT NULL,
  city VARCHAR(120) NOT NULL,
  address TEXT NOT NULL,
  phone VARCHAR(40) NULL,
  source VARCHAR(80) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_listing_city (city),
  INDEX idx_listing_category (category),
  INDEX idx_listing_source (source),
  INDEX idx_listing_business_name (business_name)
);

INSERT INTO listing_master (business_name, category, city, address, phone, source)
WITH RECURSIVE seq AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n + 1 FROM seq WHERE n < 600
)
SELECT
  CONCAT(
    ELT((n MOD 8) + 1, 'Apex', 'Urban', 'Prime', 'Green', 'Metro', 'Royal', 'Sunrise', 'Classic'),
    ' ',
    ELT((n MOD 10) + 1, 'Restaurant', 'Dental Clinic', 'Salon', 'Gym', 'Pharmacy', 'Grocery Store', 'Electronics Store', 'Travel Agency', 'Coaching Centre', 'Real Estate Agency'),
    ' ',
    n
  ) AS business_name,
  ELT((n MOD 10) + 1, 'Restaurant', 'Dental Clinic', 'Salon', 'Gym', 'Pharmacy', 'Grocery Store', 'Electronics Store', 'Travel Agency', 'Coaching Centre', 'Real Estate Agency') AS category,
  ELT((n MOD 10) + 1, 'Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow') AS city,
  CONCAT(10 + (n MOD 90), ', ', ELT((n MOD 6) + 1, 'MG Road', 'Station Road', 'Link Road', 'Park Street', 'Ring Road', 'Market Lane'), ', ', ELT((n MOD 10) + 1, 'Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow')) AS address,
  CONCAT('+91 9', LPAD(700000000 + n, 9, '0')) AS phone,
  ELT((n MOD 4) + 1, 'Google Maps', 'Justdial', 'Sulekha', 'IndiaMART') AS source
FROM seq;

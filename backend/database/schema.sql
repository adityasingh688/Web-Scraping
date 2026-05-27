CREATE DATABASE IF NOT EXISTS business_dashboard
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE business_dashboard;

CREATE TABLE IF NOT EXISTS listing_master (
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

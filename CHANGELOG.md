# Changelog

All notable changes to the DataSentry project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Project plan documentation with mandatory tracking workflow guidelines
- Tracking documents (CHANGELOG, PROGRESS, DECISIONS, README, PROMPTS_LOG, FAULT_SCENARIOS)
- Docker Compose configuration for PostgreSQL 15
- Database schema with customers, orders, payments, products, and order_items tables
- Python data generation script (100k records with injected data quality issues)
- Data loading script for PostgreSQL
- Python package structure with __init__.py files
- .env.example and .gitignore files
- Requirements.txt with core dependencies (psycopg2, sqlalchemy, pandas, faker)
- FAULT_SCENARIOS.md with detailed interview talking points for all 9 data quality issues
- Tracking workflow section in project_plan.md for persistence across sessions

### Data Quality Issues Injected
- NULL payment_status (18.7% of payments - simulates API schema change)
- NULL customer_id in orders (2% - orphaned orders)
- Duplicate customer emails and product SKUs
- Negative product prices (invalid data)
- Invalid order status values
- Future order dates
- High revenue outliers
- Referential integrity issues (orphaned product references)

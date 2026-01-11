"""
Configuration file for Location Analytics Platform
Copy this file to 'config.py' and add your API keys
"""

# SafeGraph API Configuration
# Get your API key from: https://www.safegraph.com/
SAFEGRAPH_API_KEY = "your_safegraph_api_key_here"

# US Census Bureau API Configuration
# Get free API key from: https://api.census.gov/data/key_signup.html
CENSUS_API_KEY = "your_census_api_key_here"

# Google Places API Configuration (Optional)
# Get from: https://console.cloud.google.com/
GOOGLE_PLACES_API_KEY = "your_google_api_key_here"

# SerpAPI Configuration (Optional - for Google Popular Times scraping)
# Get from: https://serpapi.com/
SERPAPI_KEY = "your_serpapi_key_here"

# Database Configuration
DATABASE_TYPE = "sqlite"  # Options: "sqlite", "postgresql", "duckdb"
DATABASE_PATH = "chamber_analytics.db"  # For SQLite

# PostgreSQL configuration (if using PostgreSQL)
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "chamber_analytics",
    "user": "postgres",
    "password": "your_password_here"
}

# Chamber Configuration
CHAMBER_NAME = "Your Chamber of Commerce"
CHAMBER_LOCATION = {
    "city": "San Diego",
    "state": "CA",
    "state_fips": "06",  # California FIPS code
    "county": "San Diego County",
    "county_fips": "073",  # San Diego County FIPS code
    "center_lat": 32.7157,
    "center_lon": -117.1611
}

# Member Data Directory
MEMBER_DATA_DIR = "member_data"
EXPORT_DATA_DIR = "exports"
LOG_DIR = "logs"

# Data Update Schedule
UPDATE_SCHEDULE = {
    "safegraph": "monthly",  # How often to fetch SafeGraph data
    "census": "annually",    # Census data updates annually
    "member_data": "monthly" # How often members should submit data
}

# Privacy Settings
PRIVACY_CONFIG = {
    "minimum_aggregation": 10,  # Never show data for fewer than N visitors
    "anonymize_zip_codes": False,  # Show first 3 digits only
    "retention_days": 730  # Keep data for 2 years
}

# Dashboard Settings
DASHBOARD_CONFIG = {
    "default_date_range": "last_90_days",
    "theme": "light",  # or "dark"
    "refresh_interval_minutes": 60
}

# Email Configuration (for automated reports)
EMAIL_CONFIG = {
    "enabled": False,
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "from_email": "analytics@chamber.org",
    "from_name": "Chamber Analytics",
    "username": "your_email@gmail.com",
    "password": "your_app_password_here"
}

# Report Configuration
REPORT_CONFIG = {
    "monthly_reports": True,
    "email_to": ["president@chamber.org", "director@chamber.org"],
    "include_member_benchmarks": True
}

# Cost Tracking
COST_CONFIG = {
    "safegraph_monthly_cost": 99.00,
    "serpapi_monthly_cost": 50.00,
    "hosting_monthly_cost": 20.00,
    "total_monthly_budget": 500.00
}

# Feature Flags
FEATURES = {
    "use_safegraph": True,
    "use_census": True,
    "use_google_places": False,
    "use_member_data": True,
    "enable_predictions": False,  # Future feature
    "enable_benchmarking": True,
    "enable_exports": True
}

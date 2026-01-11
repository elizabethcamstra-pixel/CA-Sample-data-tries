"""
Data Source Integration Module
Handles data ingestion from multiple sources for location analytics
"""

import requests
import pandas as pd
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import time
from pathlib import Path


class SafeGraphClient:
    """
    Client for SafeGraph Patterns API
    Provides foot traffic, visitor origin, and cross-shopping data
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize SafeGraph client

        Args:
            api_key: SafeGraph API key (get from https://www.safegraph.com/)
        """
        self.api_key = api_key
        self.base_url = "https://api.safegraph.com/v2/graphql"

    def get_foot_traffic(
        self,
        placekey: str,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """
        Get foot traffic data for a specific location

        Args:
            placekey: SafeGraph Placekey identifier
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            DataFrame with columns: date, raw_visit_counts, raw_visitor_counts
        """
        if not self.api_key:
            print("⚠️  No SafeGraph API key provided. Using sample data.")
            return self._generate_sample_foot_traffic(start_date, end_date)

        # SafeGraph GraphQL query
        query = """
        query($placekey: String!, $startDate: String!, $endDate: String!) {
            patterns(
                placekey: $placekey
                startDate: $startDate
                endDate: $endDate
            ) {
                placekey
                date
                raw_visit_counts
                raw_visitor_counts
                visits_by_day
            }
        }
        """

        variables = {
            "placekey": placekey,
            "startDate": start_date,
            "endDate": end_date
        }

        try:
            response = requests.post(
                self.base_url,
                json={"query": query, "variables": variables},
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            data = response.json()

            return pd.DataFrame(data['data']['patterns'])

        except Exception as e:
            print(f"❌ Error fetching SafeGraph data: {e}")
            return self._generate_sample_foot_traffic(start_date, end_date)

    def get_visitor_origins(
        self,
        placekey: str,
        date: str
    ) -> pd.DataFrame:
        """
        Get visitor home locations (census block groups)

        Args:
            placekey: SafeGraph Placekey
            date: Date (YYYY-MM-DD)

        Returns:
            DataFrame with columns: census_block_group, visitor_count
        """
        if not self.api_key:
            return self._generate_sample_visitor_origins()

        # Implementation for real API call
        # For now, return sample data
        return self._generate_sample_visitor_origins()

    def get_cross_shopping(
        self,
        placekey: str,
        date: str,
        top_n: int = 10
    ) -> pd.DataFrame:
        """
        Get brands/locations visited by same customers

        Args:
            placekey: SafeGraph Placekey
            date: Date (YYYY-MM-DD)
            top_n: Number of top co-visited brands to return

        Returns:
            DataFrame with columns: brand_name, co_visit_percentage
        """
        if not self.api_key:
            return self._generate_sample_cross_shopping(top_n)

        # Implementation for real API call
        return self._generate_sample_cross_shopping(top_n)

    def _generate_sample_foot_traffic(
        self,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """Generate realistic sample foot traffic data"""
        import numpy as np

        dates = pd.date_range(start=start_date, end=end_date, freq='D')

        # Realistic foot traffic pattern
        base_traffic = 150
        data = []

        for date in dates:
            # Weekend boost
            weekend_factor = 1.4 if date.weekday() >= 5 else 1.0

            # Seasonal variation
            month_factor = 1 + 0.3 * np.sin((date.month - 1) / 12 * 2 * np.pi)

            # Random daily variation
            random_factor = np.random.uniform(0.8, 1.2)

            visits = int(base_traffic * weekend_factor * month_factor * random_factor)
            visitors = int(visits * np.random.uniform(0.7, 0.9))  # Some repeat visitors

            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'raw_visit_counts': visits,
                'raw_visitor_counts': visitors,
                'day_of_week': date.day_name()
            })

        return pd.DataFrame(data)

    def _generate_sample_visitor_origins(self) -> pd.DataFrame:
        """Generate sample visitor origin data"""
        import numpy as np

        # Sample census block groups with realistic ZIP-like patterns
        origins = [
            {'census_block_group': '060730001001', 'zip_area': '94105', 'distance_miles': 2.3},
            {'census_block_group': '060730001002', 'zip_area': '94107', 'distance_miles': 3.1},
            {'census_block_group': '060730002001', 'zip_area': '94103', 'distance_miles': 1.8},
            {'census_block_group': '060730002002', 'zip_area': '94110', 'distance_miles': 4.2},
            {'census_block_group': '060730003001', 'zip_area': '94115', 'distance_miles': 5.5},
            {'census_block_group': '060730003002', 'zip_area': '94102', 'distance_miles': 2.9},
            {'census_block_group': '060730004001', 'zip_area': '94109', 'distance_miles': 3.7},
            {'census_block_group': '060730004002', 'zip_area': '94133', 'distance_miles': 6.1},
        ]

        # Assign visitor counts (closer = more visitors)
        for origin in origins:
            # Inverse distance decay
            distance_factor = 1 / (origin['distance_miles'] ** 1.5)
            origin['visitor_count'] = int(np.random.poisson(100 * distance_factor))
            origin['percentage'] = 0  # Will calculate after

        df = pd.DataFrame(origins)
        total_visitors = df['visitor_count'].sum()
        df['percentage'] = (df['visitor_count'] / total_visitors * 100).round(1)

        return df.sort_values('visitor_count', ascending=False)

    def _generate_sample_cross_shopping(self, top_n: int) -> pd.DataFrame:
        """Generate sample cross-shopping data"""
        brands = [
            {'brand_name': 'Starbucks', 'co_visit_percentage': 35.2},
            {'brand_name': 'Target', 'co_visit_percentage': 28.7},
            {'brand_name': 'Whole Foods', 'co_visit_percentage': 24.3},
            {'brand_name': 'CVS Pharmacy', 'co_visit_percentage': 21.8},
            {'brand_name': "McDonald's", 'co_visit_percentage': 18.9},
            {'brand_name': 'Walmart', 'co_visit_percentage': 16.4},
            {'brand_name': 'Home Depot', 'co_visit_percentage': 14.2},
            {'brand_name': "Trader Joe's", 'co_visit_percentage': 12.7},
            {'brand_name': 'Costco', 'co_visit_percentage': 11.3},
            {'brand_name': 'Safeway', 'co_visit_percentage': 9.8},
        ]

        return pd.DataFrame(brands[:top_n])


class CensusClient:
    """
    Client for US Census Bureau API
    Provides demographic data by geography
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Census client

        Args:
            api_key: Census API key (get free from https://api.census.gov/data/key_signup.html)
        """
        self.api_key = api_key
        self.base_url = "https://api.census.gov/data"

    def get_demographics(
        self,
        geography: str = "tract",
        state: str = "06",  # California
        county: str = "073",  # San Diego County
        variables: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get demographic data for a geography

        Args:
            geography: 'tract', 'block group', 'county', 'zip'
            state: State FIPS code
            county: County FIPS code
            variables: List of ACS variables (if None, uses defaults)

        Returns:
            DataFrame with demographic data
        """
        if variables is None:
            # Common useful variables
            variables = [
                'B01003_001E',  # Total population
                'B19013_001E',  # Median household income
                'B25077_001E',  # Median home value
                'B01002_001E',  # Median age
                'B23025_005E',  # Employed population
            ]

        if not self.api_key:
            print("⚠️  No Census API key provided. Using sample data.")
            return self._generate_sample_demographics()

        # Build API request
        var_string = ','.join(['NAME'] + variables)
        url = f"{self.base_url}/2021/acs/acs5"

        params = {
            'get': var_string,
            'for': f'{geography}:*',
            'in': f'state:{state} county:{county}',
            'key': self.api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])

            # Rename columns to friendly names
            column_mapping = {
                'B01003_001E': 'population',
                'B19013_001E': 'median_income',
                'B25077_001E': 'median_home_value',
                'B01002_001E': 'median_age',
                'B23025_005E': 'employed_count',
            }

            df = df.rename(columns=column_mapping)

            # Convert to numeric
            for col in column_mapping.values():
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            return df

        except Exception as e:
            print(f"❌ Error fetching Census data: {e}")
            return self._generate_sample_demographics()

    def _generate_sample_demographics(self) -> pd.DataFrame:
        """Generate sample demographic data"""
        import numpy as np

        data = []
        for i in range(20):
            tract_id = f'060730{i+1:04d}'
            data.append({
                'NAME': f'Census Tract {i+1}, San Diego County, California',
                'tract': tract_id,
                'population': np.random.randint(2000, 8000),
                'median_income': np.random.randint(40000, 120000),
                'median_home_value': np.random.randint(300000, 900000),
                'median_age': np.random.uniform(28, 45),
                'employed_count': np.random.randint(1000, 4000),
            })

        return pd.DataFrame(data)


class GooglePlacesClient:
    """
    Client for Google Places API
    Provides Popular Times and basic business info
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Google Places client

        Args:
            api_key: Google Cloud API key with Places API enabled
        """
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"

    def get_popular_times(self, place_id: str) -> Dict:
        """
        Get popular times data (hourly foot traffic patterns)

        Note: Popular Times is not officially in the API.
        You'll need to use a service like SerpAPI or web scraping.

        Args:
            place_id: Google Place ID

        Returns:
            Dict with popular times by day of week and hour
        """
        # This would require SerpAPI or similar
        print("⚠️  Popular Times requires SerpAPI subscription or web scraping")
        return self._generate_sample_popular_times()

    def _generate_sample_popular_times(self) -> Dict:
        """Generate sample popular times data"""
        import numpy as np

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        popular_times = {}

        for day_idx, day in enumerate(days):
            hourly_data = []

            # Different patterns for weekday vs weekend
            is_weekend = day_idx >= 5

            for hour in range(6, 23):  # 6 AM to 10 PM
                # Peak hours: lunch (12-1pm) and evening (5-7pm) on weekdays
                # Afternoon peak on weekends
                if is_weekend:
                    peak_hours = [12, 13, 14, 15]
                else:
                    peak_hours = [12, 17, 18]

                if hour in peak_hours:
                    busyness = np.random.randint(70, 100)
                elif hour < 11 or hour > 19:
                    busyness = np.random.randint(20, 40)
                else:
                    busyness = np.random.randint(40, 70)

                hourly_data.append({
                    'hour': hour,
                    'busyness_percent': busyness
                })

            popular_times[day] = hourly_data

        return popular_times


class MemberDataCollector:
    """
    Helper class for collecting and aggregating member-contributed data
    """

    def __init__(self, data_dir: str = "member_data"):
        """
        Initialize member data collector

        Args:
            data_dir: Directory to store member uploads
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def ingest_pos_data(
        self,
        member_id: str,
        csv_file: str
    ) -> pd.DataFrame:
        """
        Ingest Point of Sale data from a member

        Expected columns: timestamp, transaction_id, card_last4, zip_code (optional)

        Args:
            member_id: Unique member identifier
            csv_file: Path to CSV file

        Returns:
            Processed DataFrame
        """
        df = pd.read_csv(csv_file)

        # Validate required columns
        required = ['timestamp', 'transaction_id']
        if not all(col in df.columns for col in required):
            raise ValueError(f"CSV must contain columns: {required}")

        # Parse timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.day_name()

        # Add member ID
        df['member_id'] = member_id

        # Anonymize
        df = df.drop(columns=['transaction_id', 'card_last4'], errors='ignore')

        # Save processed data
        output_file = self.data_dir / f"{member_id}_pos_processed.parquet"
        df.to_parquet(output_file)

        return df

    def aggregate_member_traffic(self) -> pd.DataFrame:
        """
        Aggregate foot traffic across all members

        Returns:
            DataFrame with aggregated daily traffic by member
        """
        all_files = list(self.data_dir.glob("*_pos_processed.parquet"))

        if not all_files:
            print("⚠️  No member data found")
            return pd.DataFrame()

        dfs = [pd.read_parquet(f) for f in all_files]
        combined = pd.concat(dfs, ignore_index=True)

        # Aggregate by member and date
        aggregated = combined.groupby(['member_id', 'date']).agg({
            'timestamp': 'count'  # Count transactions as proxy for foot traffic
        }).rename(columns={'timestamp': 'transaction_count'}).reset_index()

        return aggregated


def create_sample_dataset():
    """
    Create a sample dataset for demonstration purposes
    """
    print("📦 Creating sample location analytics dataset...")

    # Initialize clients (without API keys for demo)
    sg = SafeGraphClient()
    census = CensusClient()
    google = GooglePlacesClient()

    # Generate sample data
    foot_traffic = sg.get_foot_traffic(
        placekey="zzw-222@5vg-7gq-qzz",
        start_date="2024-01-01",
        end_date="2024-12-31"
    )

    visitor_origins = sg.get_visitor_origins(
        placekey="zzw-222@5vg-7gq-qzz",
        date="2024-11-01"
    )

    cross_shopping = sg.get_cross_shopping(
        placekey="zzw-222@5vg-7gq-qzz",
        date="2024-11-01",
        top_n=10
    )

    demographics = census.get_demographics()

    popular_times = google.get_popular_times(
        place_id="ChIJexample"
    )

    # Save to files
    foot_traffic.to_csv('sample_foot_traffic.csv', index=False)
    visitor_origins.to_csv('sample_visitor_origins.csv', index=False)
    cross_shopping.to_csv('sample_cross_shopping.csv', index=False)
    demographics.to_csv('sample_demographics.csv', index=False)

    with open('sample_popular_times.json', 'w') as f:
        json.dump(popular_times, f, indent=2)

    print("✅ Sample dataset created successfully!")
    print(f"   - Foot traffic: {len(foot_traffic)} days")
    print(f"   - Visitor origins: {len(visitor_origins)} locations")
    print(f"   - Cross-shopping: {len(cross_shopping)} brands")
    print(f"   - Demographics: {len(demographics)} census tracts")

    return {
        'foot_traffic': foot_traffic,
        'visitor_origins': visitor_origins,
        'cross_shopping': cross_shopping,
        'demographics': demographics,
        'popular_times': popular_times
    }


if __name__ == "__main__":
    # Demo: Create sample dataset
    data = create_sample_dataset()

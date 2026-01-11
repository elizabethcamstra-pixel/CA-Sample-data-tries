# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

## Step 2: Generate Sample Data

```bash
# Create sample dataset for demonstration
python3 data_sources.py
```

This creates:
- `sample_foot_traffic.csv` - 365 days of sample foot traffic
- `sample_visitor_origins.csv` - Where visitors come from
- `sample_cross_shopping.csv` - Co-visited brands
- `sample_demographics.csv` - Census demographics
- `sample_popular_times.json` - Hourly traffic patterns

## Step 3: Launch Dashboard

```bash
# Start the analytics dashboard
streamlit run location_analytics_dashboard.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## Step 4: Explore Features

Navigate through the 5 tabs:
1. **Overview** - Key metrics and insights
2. **Foot Traffic** - Daily trends and patterns
3. **Visitor Origins** - Interactive map of where customers come from
4. **Cross-Shopping** - Brands also visited by your customers
5. **Demographics** - Income, age, and population data

## Next Steps

### To Use Real Data:

1. **Get API Keys** (all free):
   - SafeGraph: https://www.safegraph.com/ ($99-499/month)
   - Census Bureau: https://api.census.gov/data/key_signup.html (FREE)

2. **Configure Keys**:
   ```bash
   cp config.example.py config.py
   # Edit config.py and add your API keys
   ```

3. **Update data_sources.py**:
   ```python
   from config import SAFEGRAPH_API_KEY, CENSUS_API_KEY

   sg = SafeGraphClient(api_key=SAFEGRAPH_API_KEY)
   census = CensusClient(api_key=CENSUS_API_KEY)
   ```

### To Collect Member Data:

1. Read `MEMBER_DATA_TOOLKIT.md`
2. Share `member_data_template.csv` with members
3. Collect monthly POS exports
4. Run aggregation:
   ```python
   from data_sources import MemberDataCollector

   collector = MemberDataCollector()
   data = collector.aggregate_member_traffic()
   ```

## Troubleshooting

**Issue: "ModuleNotFoundError"**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: Dashboard won't start**
```bash
# Solution: Check Streamlit installation
pip install --upgrade streamlit
streamlit run location_analytics_dashboard.py
```

**Issue: "No module named 'config'"**
```bash
# Solution: Config is optional for sample data
# Only needed when using real API keys
```

## Help & Resources

- **Full Guide**: See `README.md`
- **Implementation Details**: See `PLACER_ALTERNATIVE_GUIDE.md`
- **Member Toolkit**: See `MEMBER_DATA_TOOLKIT.md`

## What You're Building

A location analytics platform that provides:
- 📊 Foot traffic analysis
- 🗺️ Customer origin mapping
- 🛒 Cross-shopping insights
- 📈 Demographic overlays

**Cost:** $100-500/month (vs $5,000-15,000/month for Placer.ai)
**Savings:** 90-97% cost reduction
**Value:** 70-80% of Placer.ai's functionality

---

**Questions?** See README.md or contact your chamber administrator.

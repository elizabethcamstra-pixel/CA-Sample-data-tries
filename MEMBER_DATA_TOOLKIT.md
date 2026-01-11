# 📊 Member Data Collection Toolkit

## Overview

This guide helps chamber members contribute their own data to improve the accuracy of location analytics for their business.

**Benefits of Contributing Data:**
- ✅ More accurate foot traffic counts for YOUR business
- ✅ Better insights about YOUR specific customers
- ✅ Stronger data for YOUR grant applications
- ✅ FREE participation in chamber analytics program

**Privacy Guarantee:**
- All data is aggregated and anonymized
- Individual customer information is never shared
- You control what data you share
- You can opt out at any time

## What Data Can You Contribute?

### Option 1: Point of Sale (POS) Data
**What:** Transaction timestamps from your POS system
**Why:** Provides exact foot traffic counts
**Accuracy:** 95-100%

### Option 2: WiFi Analytics
**What:** Device counts from your guest WiFi
**Why:** Tracks visitors who don't make purchases
**Accuracy:** 80-90%

### Option 3: Customer Surveys
**What:** ZIP codes and shopping patterns from customers
**Why:** Shows where customers come from
**Accuracy:** 70-80%

### Option 4: Traffic Counter
**What:** Physical device counting people entering store
**Why:** Simple, accurate foot traffic
**Accuracy:** 90-95%

## How to Contribute

### Method 1: POS Data Export (Recommended)

**Step 1:** Export transaction data from your POS system

Most POS systems (Square, Clover, Shopify, Toast, etc.) allow CSV exports.

**Required fields:**
- `timestamp` - Date and time of transaction
- `transaction_id` - Unique ID for each transaction

**Optional fields:**
- `card_last4` - Last 4 digits of card (for cross-shopping analysis)
- `zip_code` - Customer ZIP code (from billing address)

**Step 2:** Clean the data

Remove any personally identifiable information:
- ❌ Customer names
- ❌ Full credit card numbers
- ❌ Email addresses
- ❌ Phone numbers
- ✅ Keep: timestamps, transaction IDs, last 4 of card, ZIP codes

**Step 3:** Use the template

See `member_data_template.csv` for the correct format.

Example:
```csv
timestamp,transaction_id,card_last4,zip_code
2024-01-15 09:23:15,TXN001,1234,92101
2024-01-15 10:45:32,TXN002,5678,92103
```

**Step 4:** Submit the file

- Email to: [chamber-data@chamber.org]
- Or upload at: [https://chamber-portal.org/upload]
- Or provide via secure file share

### Method 2: WiFi Analytics

**Option A: Using UniFi (Ubiquiti)**

If you have UniFi access points:

1. Log into UniFi Controller
2. Go to Insights → WiFi
3. Export visitor counts by hour/day
4. Send CSV to chamber

**Option B: Using Third-Party WiFi Analytics**

Services like:
- Purple WiFi
- Aislelabs
- Cloud4Wi
- Skyfii

These provide:
- Foot traffic counts
- Dwell time
- Repeat visitor rates
- Heat maps

**Cost:** $50-200/month

**Step 1:** Sign up for service
**Step 2:** Install their WiFi system
**Step 3:** Export monthly reports
**Step 4:** Share with chamber

### Method 3: Customer Surveys

**Step 1:** Create a simple survey

Questions to ask:
1. What is your ZIP code?
2. How far did you travel to get here?
3. What other businesses did you visit today?
4. How often do you visit our business?

**Step 2:** Implement survey

Options:
- QR code at checkout → Google Forms
- Email survey after purchase
- Paper form at register
- SMS survey

**Step 3:** Incentivize responses

Offer:
- 10% off next purchase
- Entry into monthly drawing
- Free small item
- Loyalty points

**Step 4:** Export and share

Export survey results as CSV monthly and send to chamber.

### Method 4: Physical Traffic Counter

**Option A: Manual Counter**

- Cost: $20-50
- Accuracy: 90%+
- Method: Clicker counter at entrance
- Time: 5 seconds per customer

**Option B: Electronic Counter**

Products:
- **Sensormatic** - $200-500
- **DILAX** - $300-800
- **V-Count** - $400-1000

Features:
- Automatic counting
- In/out tracking
- Hourly reports
- WiFi/cloud export

**Step 1:** Purchase and install
**Step 2:** Export daily/weekly counts
**Step 3:** Send CSV to chamber

## Data Format Requirements

### POS Data Format

**File name:** `memberID_pos_YYYYMM.csv`

**Columns:**
```
timestamp,transaction_id,card_last4,zip_code
2024-01-15 09:23:15,TXN001,1234,92101
```

- `timestamp`: YYYY-MM-DD HH:MM:SS format
- `transaction_id`: Any unique identifier
- `card_last4`: Last 4 digits only (optional)
- `zip_code`: 5-digit ZIP code (optional)

### WiFi Analytics Format

**File name:** `memberID_wifi_YYYYMM.csv`

**Columns:**
```
date,hour,device_count,new_devices,returning_devices
2024-01-15,09,23,15,8
```

### Survey Data Format

**File name:** `memberID_survey_YYYYMM.csv`

**Columns:**
```
date,zip_code,distance_miles,other_businesses_visited,visit_frequency
2024-01-15,92101,2.3,"Target,Starbucks",Weekly
```

### Traffic Counter Format

**File name:** `memberID_counter_YYYYMM.csv`

**Columns:**
```
date,hour,entry_count,exit_count
2024-01-15,09,34,32
```

## Frequency of Submission

**Recommended:** Monthly

Submit data by the 5th of each month for the previous month.

Example:
- January data → Submit by February 5th
- February data → Submit by March 5th

## Data Security

**How we protect your data:**

1. **Encryption:** All uploads use SSL/TLS encryption
2. **Anonymization:** Personal information is removed immediately
3. **Aggregation:** Individual business data is combined with others
4. **Access Control:** Only authorized chamber staff can view raw data
5. **Minimum Threshold:** We never publish data representing fewer than 10 customers

**What we do with your data:**

✅ Create aggregated reports for the chamber
✅ Generate insights for YOUR business
✅ Support grant applications for members
✅ Benchmark against regional averages

**What we DON'T do:**

❌ Sell your data to third parties
❌ Share individual business data publicly
❌ Use data for purposes other than analytics
❌ Keep unnecessary customer information

## Legal Agreement

By submitting data, you agree that:

1. You own the data or have permission to share it
2. You have obtained any necessary customer consents
3. The data has been anonymized appropriately
4. You understand how the data will be used

**Data Sharing Agreement:** [Link to legal document]

## Getting Started Checklist

- [ ] Decide which data method(s) to use
- [ ] Sign data sharing agreement
- [ ] Set up data export process
- [ ] Test with one month of data
- [ ] Schedule recurring monthly exports
- [ ] Review your analytics dashboard
- [ ] Use insights for business decisions

## Support

**Need help?**

**Technical Support:**
- Email: tech-support@chamber.org
- Phone: (555) 123-4567
- Hours: Mon-Fri 9am-5pm

**Training:**
- Monthly webinar: "How to Export POS Data"
- One-on-one setup assistance available
- Video tutorials: [Link]

**FAQ:**

**Q: Is this required?**
A: No, it's completely voluntary. But members who contribute get more accurate insights.

**Q: How much time does this take?**
A: Initial setup: 30-60 minutes. Monthly submission: 5-10 minutes.

**Q: What if I don't have a POS system?**
A: Use WiFi analytics, surveys, or a simple traffic counter.

**Q: Can I see my raw data?**
A: Yes, you always have access to your own data through the member portal.

**Q: What if I have multiple locations?**
A: Submit separate files for each location with different member IDs.

**Q: Can I stop sharing data?**
A: Yes, you can opt out at any time. Just email us.

## Example Success Stories

**Example 1: Grant Application**

> "Thanks to the foot traffic data from the chamber, we were able to demonstrate 30% year-over-year growth in our business. This helped us secure a $50,000 SBA loan for expansion."
>
> — Sarah M., Retail Store Owner

**Example 2: Partnership**

> "The cross-shopping analysis showed that 40% of my customers also visit the coffee shop two doors down. We created a joint loyalty program and both saw a 15% increase in sales."
>
> — Mike T., Restaurant Owner

**Example 3: Marketing ROI**

> "By knowing which ZIP codes our customers come from, we targeted our Facebook ads more effectively and cut our customer acquisition cost by 35%."
>
> — Jennifer L., Boutique Owner

## Monthly Submission Checklist

Use this checklist each month:

- [ ] Export last month's transaction data from POS
- [ ] Remove any personal information (names, emails, etc.)
- [ ] Verify data format matches template
- [ ] Save as: `memberID_pos_YYYYMM.csv`
- [ ] Upload to chamber portal or email
- [ ] Verify submission confirmation
- [ ] Review your updated analytics dashboard
- [ ] Note any insights for business planning

## Resources

**POS Export Guides:**
- [Square: How to export transaction data]
- [Clover: How to export reports]
- [Shopify: How to export order data]
- [Toast: How to export transaction data]

**WiFi Analytics Providers:**
- Purple WiFi: https://www.purplewifi.com
- Aislelabs: https://www.aislelabs.com
- Cloud4Wi: https://www.cloud4wi.com

**Traffic Counter Options:**
- Amazon: Search "people counter"
- Sensormatic: https://www.sensormatic.com
- V-Count: https://www.v-count.com

**Survey Tools:**
- Google Forms: https://forms.google.com (Free)
- SurveyMonkey: https://www.surveymonkey.com (Free tier)
- Typeform: https://www.typeform.com (Free tier)

## Contact

Questions about data submission?

**Chamber of Commerce**
[Your Address]
[Your Phone]
[Your Email]

**Office Hours:**
Monday-Friday, 9am-5pm

**Online Portal:**
[https://chamber-portal.org]

---

**Thank you for contributing to our chamber's location analytics program!**

*Together, we're making data-driven decision making accessible to all our members.*

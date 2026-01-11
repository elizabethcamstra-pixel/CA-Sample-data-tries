"""
Location Analytics Dashboard - Placer.ai Alternative
Chamber of Commerce Edition
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
from data_sources import SafeGraphClient, CensusClient, GooglePlacesClient, create_sample_dataset
from datetime import datetime, timedelta
import json
from pathlib import Path


# Page config
st.set_page_config(
    page_title="Chamber Location Analytics",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_sample_data():
    """Load or create sample data"""
    # Check if sample files exist
    if Path('sample_foot_traffic.csv').exists():
        foot_traffic = pd.read_csv('sample_foot_traffic.csv')
        visitor_origins = pd.read_csv('sample_visitor_origins.csv')
        cross_shopping = pd.read_csv('sample_cross_shopping.csv')
        demographics = pd.read_csv('sample_demographics.csv')

        with open('sample_popular_times.json', 'r') as f:
            popular_times = json.load(f)

        return {
            'foot_traffic': foot_traffic,
            'visitor_origins': visitor_origins,
            'cross_shopping': cross_shopping,
            'demographics': demographics,
            'popular_times': popular_times
        }
    else:
        # Create sample data
        return create_sample_dataset()


def create_map(visitor_origins_df, center_lat=32.7157, center_lon=-117.1611):
    """Create an interactive map showing visitor origins"""

    # Create base map centered on business location
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles='OpenStreetMap'
    )

    # Add business location marker
    folium.Marker(
        [center_lat, center_lon],
        popup="Your Business",
        tooltip="Your Business Location",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

    # Add heat map circles for visitor origins
    # (In real implementation, would use actual lat/lon from census block groups)
    import numpy as np

    for idx, row in visitor_origins_df.iterrows():
        # Sample coordinates around the center (replace with real geocoding)
        offset_lat = np.random.uniform(-0.1, 0.1)
        offset_lon = np.random.uniform(-0.1, 0.1)

        lat = center_lat + offset_lat
        lon = center_lon + offset_lon

        folium.Circle(
            location=[lat, lon],
            radius=row['visitor_count'] * 10,  # Scale by visitor count
            popup=f"ZIP {row['zip_area']}: {row['visitor_count']} visitors ({row['percentage']}%)",
            tooltip=f"{row['zip_area']}: {row['percentage']}%",
            color='blue',
            fill=True,
            fillColor='blue',
            fillOpacity=0.4
        ).add_to(m)

    return m


def main():
    # Header
    st.markdown('<div class="main-header">📍 Chamber Location Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Affordable Alternative to Placer.ai</div>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("🎛️ Dashboard Controls")

    # Business selector
    business_name = st.sidebar.selectbox(
        "Select Business",
        ["Sample Business - Downtown", "Member Store A", "Member Store B", "Member Store C"]
    )

    # Date range
    st.sidebar.subheader("Date Range")
    date_option = st.sidebar.radio(
        "Select Period",
        ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "Custom"]
    )

    if date_option == "Custom":
        start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=90))
        end_date = st.sidebar.date_input("End Date", datetime.now())
    else:
        end_date = datetime.now()
        if date_option == "Last 30 Days":
            start_date = end_date - timedelta(days=30)
        elif date_option == "Last 90 Days":
            start_date = end_date - timedelta(days=90)
        elif date_option == "Last 6 Months":
            start_date = end_date - timedelta(days=180)
        else:  # Last Year
            start_date = end_date - timedelta(days=365)

    # Data source info
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Data Sources")

    use_safegraph = st.sidebar.checkbox("SafeGraph Patterns", value=True, help="Foot traffic & visitor origins")
    use_census = st.sidebar.checkbox("US Census Data", value=True, help="Demographics")
    use_google = st.sidebar.checkbox("Google Popular Times", value=False, help="Hourly busyness")
    use_member_data = st.sidebar.checkbox("Member Contributed", value=False, help="POS & WiFi data")

    # Load data
    with st.spinner("Loading data..."):
        data = load_sample_data()

    # Filter foot traffic data by date range
    foot_traffic_df = pd.DataFrame(data['foot_traffic'])
    foot_traffic_df['date'] = pd.to_datetime(foot_traffic_df['date'])
    mask = (foot_traffic_df['date'] >= pd.to_datetime(start_date)) & (foot_traffic_df['date'] <= pd.to_datetime(end_date))
    foot_traffic_df = foot_traffic_df.loc[mask]

    # Main dashboard
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "👥 Foot Traffic",
        "🗺️ Visitor Origins",
        "🛒 Cross-Shopping",
        "📈 Demographics"
    ])

    # TAB 1: OVERVIEW
    with tab1:
        st.header("Business Performance Overview")

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        total_visits = foot_traffic_df['raw_visit_counts'].sum()
        total_visitors = foot_traffic_df['raw_visitor_counts'].sum()
        avg_daily_visits = foot_traffic_df['raw_visit_counts'].mean()

        # Calculate period-over-period change
        mid_point = len(foot_traffic_df) // 2
        first_half_avg = foot_traffic_df.iloc[:mid_point]['raw_visit_counts'].mean()
        second_half_avg = foot_traffic_df.iloc[mid_point:]['raw_visit_counts'].mean()
        pct_change = ((second_half_avg - first_half_avg) / first_half_avg * 100) if first_half_avg > 0 else 0

        with col1:
            st.metric(
                label="Total Visits",
                value=f"{total_visits:,}",
                delta=f"{pct_change:+.1f}% vs prev period"
            )

        with col2:
            st.metric(
                label="Unique Visitors",
                value=f"{total_visitors:,}",
                delta=None
            )

        with col3:
            st.metric(
                label="Avg Daily Visits",
                value=f"{avg_daily_visits:.0f}",
                delta=None
            )

        with col4:
            repeat_rate = (1 - total_visitors / total_visits) * 100
            st.metric(
                label="Repeat Visit Rate",
                value=f"{repeat_rate:.1f}%",
                delta=None
            )

        st.markdown("---")

        # Quick insights
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top Visitor Origins")
            origins_top5 = data['visitor_origins'].head(5)

            fig = px.bar(
                origins_top5,
                x='zip_area',
                y='visitor_count',
                text='percentage',
                labels={'zip_area': 'ZIP Code', 'visitor_count': 'Visitors'},
                color='visitor_count',
                color_continuous_scale='Blues'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Top Cross-Shopping Destinations")
            cross_shop_top5 = data['cross_shopping'].head(5)

            fig = px.bar(
                cross_shop_top5,
                x='brand_name',
                y='co_visit_percentage',
                text='co_visit_percentage',
                labels={'brand_name': 'Brand', 'co_visit_percentage': '% of Customers'},
                color='co_visit_percentage',
                color_continuous_scale='Greens'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)

        # Info box
        st.markdown("""
        <div class="info-box">
        <strong>💡 How to use these insights:</strong>
        <ul>
            <li><strong>Foot Traffic:</strong> Track your busiest days/times to optimize staffing</li>
            <li><strong>Visitor Origins:</strong> Understand your trade area for targeted marketing</li>
            <li><strong>Cross-Shopping:</strong> Identify partnership opportunities with co-visited brands</li>
            <li><strong>Demographics:</strong> Tailor products/services to your customer base</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # TAB 2: FOOT TRAFFIC ANALYSIS
    with tab2:
        st.header("Foot Traffic Analysis")

        # Time series chart
        st.subheader("Daily Foot Traffic Trend")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=foot_traffic_df['date'],
            y=foot_traffic_df['raw_visit_counts'],
            mode='lines',
            name='Total Visits',
            line=dict(color='#1f77b4', width=2),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))

        fig.add_trace(go.Scatter(
            x=foot_traffic_df['date'],
            y=foot_traffic_df['raw_visitor_counts'],
            mode='lines',
            name='Unique Visitors',
            line=dict(color='#ff7f0e', width=2)
        ))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Count",
            hovermode='x unified',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Day of week analysis
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Traffic by Day of Week")

            dow_avg = foot_traffic_df.groupby('day_of_week')['raw_visit_counts'].mean().reset_index()

            # Ensure correct day order
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_avg['day_of_week'] = pd.Categorical(dow_avg['day_of_week'], categories=day_order, ordered=True)
            dow_avg = dow_avg.sort_values('day_of_week')

            fig = px.bar(
                dow_avg,
                x='day_of_week',
                y='raw_visit_counts',
                labels={'day_of_week': 'Day', 'raw_visit_counts': 'Avg Visits'},
                color='raw_visit_counts',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Hourly Traffic Pattern")

            if use_google:
                # Use popular times data
                popular_times = data['popular_times']

                # Average across all days
                all_hours = []
                for day, hours in popular_times.items():
                    for hour_data in hours:
                        all_hours.append(hour_data)

                hourly_df = pd.DataFrame(all_hours)
                hourly_avg = hourly_df.groupby('hour')['busyness_percent'].mean().reset_index()

                fig = px.line(
                    hourly_avg,
                    x='hour',
                    y='busyness_percent',
                    labels={'hour': 'Hour of Day', 'busyness_percent': 'Busyness %'},
                    markers=True
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Enable 'Google Popular Times' in sidebar to see hourly patterns")

        # Weekly heatmap
        st.subheader("Weekly Traffic Heatmap")

        # Create week number and day of week columns
        foot_traffic_df['week'] = foot_traffic_df['date'].dt.isocalendar().week
        foot_traffic_df['dow_num'] = foot_traffic_df['date'].dt.dayofweek

        # Pivot for heatmap
        heatmap_data = foot_traffic_df.pivot_table(
            index='dow_num',
            columns='week',
            values='raw_visit_counts',
            aggfunc='mean'
        )

        fig = px.imshow(
            heatmap_data,
            labels=dict(x="Week Number", y="Day of Week", color="Avg Visits"),
            y=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            color_continuous_scale='YlOrRd',
            aspect='auto'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    # TAB 3: VISITOR ORIGINS
    with tab3:
        st.header("Visitor Origin Analysis")

        st.subheader("Where Your Customers Come From")

        col1, col2 = st.columns([2, 1])

        with col1:
            # Interactive map
            visitor_map = create_map(data['visitor_origins'])
            st_folium(visitor_map, width=700, height=500)

        with col2:
            st.markdown("### Top Origin Areas")

            origins_df = data['visitor_origins'].head(10)

            for idx, row in origins_df.iterrows():
                st.markdown(f"""
                <div class="metric-card">
                    <strong>ZIP {row['zip_area']}</strong><br>
                    {row['visitor_count']} visitors ({row['percentage']}%)<br>
                    <small>{row['distance_miles']:.1f} miles away</small>
                </div>
                """, unsafe_allow_html=True)

        # Trade area insights
        st.markdown("---")
        st.subheader("Trade Area Insights")

        col1, col2, col3 = st.columns(3)

        origins_df = data['visitor_origins']

        with col1:
            st.metric(
                "Primary Trade Area",
                "< 3 miles",
                f"{origins_df[origins_df['distance_miles'] < 3]['percentage'].sum():.1f}% of visitors"
            )

        with col2:
            st.metric(
                "Secondary Trade Area",
                "3-5 miles",
                f"{origins_df[(origins_df['distance_miles'] >= 3) & (origins_df['distance_miles'] < 5)]['percentage'].sum():.1f}% of visitors"
            )

        with col3:
            avg_distance = (origins_df['distance_miles'] * origins_df['visitor_count']).sum() / origins_df['visitor_count'].sum()
            st.metric(
                "Avg Distance Traveled",
                f"{avg_distance:.1f} miles"
            )

    # TAB 4: CROSS-SHOPPING ANALYSIS
    with tab4:
        st.header("Cross-Shopping Analysis")

        st.subheader("Brands Also Visited by Your Customers")

        cross_shop_df = data['cross_shopping']

        # Horizontal bar chart
        fig = px.bar(
            cross_shop_df.sort_values('co_visit_percentage', ascending=True),
            x='co_visit_percentage',
            y='brand_name',
            orientation='h',
            text='co_visit_percentage',
            labels={'co_visit_percentage': '% of Your Customers', 'brand_name': 'Brand'},
            color='co_visit_percentage',
            color_continuous_scale='Teal'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Insights
        st.markdown("---")
        st.subheader("🎯 Partnership Opportunities")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Complementary Businesses")
            top_partners = cross_shop_df.head(3)

            for idx, row in top_partners.iterrows():
                st.markdown(f"""
                <div class="info-box">
                    <strong>{row['brand_name']}</strong><br>
                    {row['co_visit_percentage']:.1f}% of your customers also visit this location<br>
                    <small>💡 Consider: Co-marketing campaigns, shared promotions, loyalty partnerships</small>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("### Market Positioning")

            st.markdown(f"""
            <div class="metric-card">
                <strong>Your Customer Profile:</strong><br><br>
                Your customers are also shopping at:
                <ul>
                    <li>{cross_shop_df.iloc[0]['brand_name']} ({cross_shop_df.iloc[0]['co_visit_percentage']:.0f}%)</li>
                    <li>{cross_shop_df.iloc[1]['brand_name']} ({cross_shop_df.iloc[1]['co_visit_percentage']:.0f}%)</li>
                    <li>{cross_shop_df.iloc[2]['brand_name']} ({cross_shop_df.iloc[2]['co_visit_percentage']:.0f}%)</li>
                </ul>
                <br>
                <strong>💡 Insight:</strong> This suggests your customers value convenience
                and are likely shopping for everyday needs in the same trip.
            </div>
            """, unsafe_allow_html=True)

    # TAB 5: DEMOGRAPHICS
    with tab5:
        st.header("Customer Demographics")

        if use_census:
            demo_df = data['demographics']

            st.subheader("Trade Area Demographics")

            # Key demographic metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                avg_income = demo_df['median_income'].mean()
                st.metric("Avg Median Income", f"${avg_income:,.0f}")

            with col2:
                avg_age = demo_df['median_age'].mean()
                st.metric("Avg Median Age", f"{avg_age:.1f} years")

            with col3:
                total_pop = demo_df['population'].sum()
                st.metric("Total Trade Area Pop", f"{total_pop:,.0f}")

            with col4:
                avg_home_value = demo_df['median_home_value'].mean()
                st.metric("Avg Home Value", f"${avg_home_value:,.0f}")

            # Charts
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Income Distribution")

                fig = px.histogram(
                    demo_df,
                    x='median_income',
                    nbins=20,
                    labels={'median_income': 'Median Household Income'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig.update_layout(showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("Age Distribution")

                fig = px.histogram(
                    demo_df,
                    x='median_age',
                    nbins=20,
                    labels={'median_age': 'Median Age'},
                    color_discrete_sequence=['#ff7f0e']
                )
                fig.update_layout(showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)

            # Detailed table
            st.subheader("Census Tract Details")

            display_df = demo_df[[
                'NAME', 'population', 'median_income', 'median_age', 'median_home_value'
            ]].copy()

            display_df.columns = ['Census Tract', 'Population', 'Median Income', 'Median Age', 'Median Home Value']

            st.dataframe(
                display_df.style.format({
                    'Population': '{:,.0f}',
                    'Median Income': '${:,.0f}',
                    'Median Age': '{:.1f}',
                    'Median Home Value': '${:,.0f}'
                }),
                use_container_width=True
            )

        else:
            st.info("Enable 'US Census Data' in sidebar to see demographics")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <strong>📍 Chamber Location Analytics Dashboard</strong><br>
        Powered by SafeGraph, US Census Bureau, and Member Data<br>
        <small>Cost-effective alternative to Placer.ai | Built for Chambers of Commerce</small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

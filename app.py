# app.py
import math
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(page_title="Joins, CVR & Financials (2024–2025)", layout="wide")

# =========================
# Data (ported from your React file)
# =========================
monthly_data = [
    {"date":"2024-01-01","joins_total":7745.0,"joins_online":7152.0,"joins_phone":593.0,"trial_cancel_pct_total":0.21123305358295674,"trial_conversion_rate":0.7887669464170433,"active_total":1466725.0,"active_phone":138868.0,"gmv_total":1131941.04,"claim_amount":123266.14,"claims_to_gmv":0.10889802175562077,"net_members":874.0,"claims_phone":14126.73},
    {"date":"2024-02-01","joins_total":7169.0,"joins_online":6468.0,"joins_phone":701.0,"trial_cancel_pct_total":0.23057609150509137,"trial_conversion_rate":0.7694236297977409,"active_total":1385888.0,"active_phone":130532.0,"gmv_total":1033025.76,"claim_amount":110917.59,"claims_to_gmv":0.10737245846975335,"net_members":844.0,"claims_phone":10310.61},
    {"date":"2024-03-01","joins_total":7771.0,"joins_online":7062.0,"joins_phone":709.0,"trial_cancel_pct_total":0.21953416893642983,"trial_conversion_rate":0.7804658386300347,"active_total":1478854.0,"active_phone":137554.0,"gmv_total":1211336.85,"claim_amount":128548.31,"claims_to_gmv":0.10612600721297262,"net_members":965.0,"claims_phone":13556.69},
    {"date":"2024-04-01","joins_total":10334.0,"joins_online":9429.0,"joins_phone":905.0,"trial_cancel_pct_total":0.22217960131565705,"trial_conversion_rate":0.7778213640816723,"active_total":1452543.0,"active_phone":133531.0,"gmv_total":1282364.63,"claim_amount":141069.55,"claims_to_gmv":0.11000184001291532,"net_members":1302.0,"claims_phone":14505.19},
    {"date":"2024-05-01","joins_total":14554.0,"joins_online":13666.0,"joins_phone":888.0,"trial_cancel_pct_total":0.23938436168750996,"trial_conversion_rate":0.7606159131515724,"active_total":1653547.0,"active_phone":131590.0,"gmv_total":1394269.5,"claim_amount":156647.27,"claims_to_gmv":0.11235295272282786,"net_members":1789.0,"claims_phone":14694.49},
    {"date":"2024-06-01","joins_total":12692.0,"joins_online":12153.0,"joins_phone":539.0,"trial_cancel_pct_total":0.26851402458209833,"trial_conversion_rate":0.7286473378518762,"active_total":1587107.0,"active_phone":128628.0,"gmv_total":1148398.61,"claim_amount":129423.03,"claims_to_gmv":0.11270394568123778,"net_members":1642.0,"claims_phone":9346.92},
    {"date":"2024-07-01","joins_total":9876.0,"joins_online":9398.0,"joins_phone":478.0,"trial_cancel_pct_total":0.2584925192066316,"trial_conversion_rate":0.7370382737926286,"active_total":1816145.0,"active_phone":140165.0,"gmv_total":1270073.87,"claim_amount":137060.77,"claims_to_gmv":0.10791692337760695,"net_members":1398.0,"claims_phone":10394.89},
    {"date":"2024-08-01","joins_total":11094.0,"joins_online":10492.0,"joins_phone":602.0,"trial_cancel_pct_total":0.2345411930854516,"trial_conversion_rate":0.7655138813776818,"active_total":2060399.0,"active_phone":143610.0,"gmv_total":1466066.66,"claim_amount":161870.02,"claims_to_gmv":0.11041113261240167,"net_members":1821.0,"claims_phone":12508.46},
    {"date":"2024-09-01","joins_total":12013.0,"joins_online":11295.0,"joins_phone":718.0,"trial_cancel_pct_total":0.21285049529676067,"trial_conversion_rate":0.7869807714975447,"active_total":1988208.0,"active_phone":137659.0,"gmv_total":1439107.8,"claim_amount":156094.83,"claims_to_gmv":0.10846878675236639,"net_members":2202.0,"claims_phone":13034.64},
    {"date":"2024-10-01","joins_total":12964.0,"joins_online":12873.0,"joins_phone":91.0,"trial_cancel_pct_total":0.1919160752850972,"trial_conversion_rate":0.8084696073674784,"active_total":2056908.0,"active_phone":141788.0,"gmv_total":1379048.13,"claim_amount":145535.78,"claims_to_gmv":0.10552304116246772,"net_members":2752.0,"claims_phone":13718.89},
    {"date":"2024-11-01","joins_total":18487.0,"joins_online":17302.0,"joins_phone":1185.0,"trial_cancel_pct_total":0.19131671304376345,"trial_conversion_rate":0.8084251586591664,"active_total":2183029.0,"active_phone":146842.0,"gmv_total":1723824.74,"claim_amount":187733.4,"claims_to_gmv":0.10889852147521854,"net_members":3963.0,"claims_phone":16434.52},
    {"date":"2024-12-01","joins_total":13141.0,"joins_online":8997.0,"joins_phone":4144.0,"trial_cancel_pct_total":0.189939882200745,"trial_conversion_rate":0.8098936157062635,"active_total":2455376.0,"active_phone":161896.0,"gmv_total":1522046.25,"claim_amount":159269.7,"claims_to_gmv":0.10463969847689829,"net_members":2898.0,"claims_phone":15249.38},
    {"date":"2025-01-01","joins_total":8855.0,"joins_online":8119.0,"joins_phone":736.0,"trial_cancel_pct_total":0.21050254093732354,"trial_conversion_rate":0.7894974590626764,"active_total":920852.0,"active_phone":60111.0,"gmv_total":1281202.26,"claim_amount":130833.61,"claims_to_gmv":0.10212339200073639,"net_members":2149.0,"claims_phone":10988.28},
    {"date":"2025-02-01","joins_total":10504.0,"joins_online":6860.0,"joins_phone":3644.0,"trial_cancel_pct_total":0.22934120335110434,"trial_conversion_rate":0.7706597530415719,"active_total":912764.0,"active_phone":59599.0,"gmv_total":1013317.74,"claim_amount":107605.77,"claims_to_gmv":0.10619879357490775,"net_members":2690.0,"claims_phone":11176.35},
    {"date":"2025-03-01","joins_total":13592.0,"joins_online":7734.0,"joins_phone":5858.0,"trial_cancel_pct_total":0.2227781047675106,"trial_conversion_rate":0.7346233078281342,"active_total":1018598.0,"active_phone":61939.0,"gmv_total":1369951.94,"claim_amount":148014.65,"claims_to_gmv":0.10804391744691358,"net_members":3720.0,"claims_phone":13993.75},
    {"date":"2025-04-01","joins_total":17768.0,"joins_online":13279.0,"joins_phone":4489.0,"trial_cancel_pct_total":0.30395317244484466,"trial_conversion_rate":0.8120225123827104,"active_total":1022575.0,"active_phone":62456.0,"gmv_total":1496028.17,"claim_amount":167435.28,"claims_to_gmv":0.11191965984001364,"net_members":5399.0,"claims_phone":12892.15},
    {"date":"2025-05-01","joins_total":14209.0,"joins_online":13285.0,"joins_phone":924.0,"trial_cancel_pct_total":0.1936804842046586,"trial_conversion_rate":0.7970293471750292,"active_total":1072984.0,"active_phone":64535.0,"gmv_total":2885906.58,"claim_amount":301888.81,"claims_to_gmv":0.10462531713611304,"net_members":4940.0,"claims_phone":22650.61},
    {"date":"2025-06-01","joins_total":11582.0,"joins_online":10863.0,"joins_phone":719.0,"trial_cancel_pct_total":0.20755465342876878,"trial_conversion_rate":0.7974443090989468,"active_total":1190084.0,"active_phone":72078.0,"gmv_total":1539569.14,"claim_amount":162909.77,"claims_to_gmv":0.105819975131355,"net_members":4421.0,"claims_phone":12135.84},
    {"date":"2025-07-01","joins_total":10957.0,"joins_online":10060.0,"joins_phone":897.0,"trial_cancel_pct_total":0.23181491174701142,"trial_conversion_rate":0.7942863926253533,"active_total":1365127.0,"active_phone":80828.0,"gmv_total":1666496.14,"claim_amount":172954.31,"claims_to_gmv":0.10377686224277741,"net_members":4594.0,"claims_phone":16123.87},
    {"date":"2025-08-01","joins_total":13227.0,"joins_online":12346.0,"joins_phone":881.0,"trial_cancel_pct_total":0.18084346489786087,"trial_conversion_rate":0.7850684170324348,"active_total":1278217.0,"active_phone":75236.0,"gmv_total":1760092.42,"claim_amount":186930.84,"claims_to_gmv":0.10620838601746653,"net_members":6319.0,"claims_phone":15570.79},
    {"date":"2025-09-01","joins_total":14431.0,"joins_online":13487.0,"joins_phone":944.0,"trial_cancel_pct_total":0.1672802994941452,"trial_conversion_rate":0.7935698012615203,"active_total":1217756.0,"active_phone":70835.0,"gmv_total":1709932.73,"claim_amount":183183.99,"claims_to_gmv":0.10712782008663247,"net_members":8260.0,"claims_phone":15061.27},
    {"date":"2025-10-01","joins_total":14114.0,"joins_online":12873.0,"joins_phone":1241.0,"trial_cancel_pct_total":0.1769162526569341,"trial_conversion_rate":0.7999858299552212,"active_total":1360591.0,"active_phone":77002.0,"gmv_total":2321424.68,"claim_amount":247867.23,"claims_to_gmv":0.10677713357313231,"net_members":9635.0,"claims_phone":21721.95},
    {"date":"2025-11-01","joins_total":17980.0,"joins_online":16323.0,"joins_phone":1657.0,"trial_cancel_pct_total":0.15444938820912125,"trial_conversion_rate":0.8317575083426029,"active_total":1104788.0,"active_phone":65456.0,"gmv_total":2319018.39,"claim_amount":258933.28,"claims_to_gmv":0.11165982188823046,"net_members":14901.0,"claims_phone":20301.26},
    {"date":"2025-12-01","joins_total":5646.0,"joins_online":5170.0,"joins_phone":476.0,"trial_cancel_pct_total":0.09794544810485299,"trial_conversion_rate":0.902054551895147,"active_total":926874.0,"active_phone":62919.0,"gmv_total":1158699.84,"claim_amount":116420.08,"claims_to_gmv":0.10047475280569643,"net_members":5093.0,"claims_phone":10398.03},
]

# =========================
# Helpers
# =========================
def fmt_int(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    return f"{int(round(float(x))):,}"

def fmt_money(x, digits=0):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    return f"${float(x):,.{digits}f}"

def fmt_pct(x, digits=1):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    return f"{float(x)*100:.{digits}f}%"

def safe_div(a, b):
    a = float(a) if a is not None else np.nan
    b = float(b) if b is not None else np.nan
    if not np.isfinite(a) or not np.isfinite(b) or b == 0:
        return np.nan
    return a / b

def ym_label(dt: pd.Timestamp) -> str:
    return dt.strftime("%b %Y")

def summarize(df: pd.DataFrame) -> dict:
    gmv = df["gmv_total"].sum()
    claims = df["claim_amount"].sum()
    claims_phone = df["claims_phone"].sum()
    return {
        "joins": df["joins_total"].sum(),
        "gmv": gmv,
        "claims": claims,
        "claimsPhone": claims_phone,
        "activeAvg": df["active_total"].mean(),
        "trialCancelAvg": df["trial_cancel_pct_total"].mean(),
        "trialConvAvg": df["trial_conversion_rate"].mean(),
        "claimsToGmvAvg": df["claims_to_gmv"].mean(),
        "phoneClaimsShare": safe_div(claims_phone, claims),
        "netMembers": df["net_members"].sum(),
    }

# =========================
# Build DataFrame + light tests (ported from your JS assertions)
# =========================
df = pd.DataFrame(monthly_data)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)
df["month_label"] = df["date"].dt.strftime("%b %Y")

assert len(df) == 24, "Expected 24 months (Jan 2024–Dec 2025)"
assert df["date"].notna().all(), "All rows must have a valid date"
assert (df["claim_amount"].fillna(0) >= df["claims_phone"].fillna(0)).all(), "claim_amount must be >= claims_phone"
joins_sum_ok = (
    (df["joins_total"].fillna(0) == 0)
    | ((df["joins_online"].fillna(0) + df["joins_phone"].fillna(0) - df["joins_total"].fillna(0)).abs() < 1e-6)
).all()
assert joins_sum_ok, "joins_online + joins_phone should equal joins_total"
assert np.isfinite(df["joins_total"].sum()) and df["joins_total"].sum() > 0, "Join total sum must be finite and > 0"

# =========================
# Header + controls
# =========================
st.title("Joins, CVR & Financials (2024–2025)")
st.caption("External Context removed · Channel Mix replaced with Claims by Placement · Opportunities + Recommendations added.")

c1, c2, c3 = st.columns([1.2, 1, 1])
with c1:
    year = st.selectbox("Year", ["All", "2024", "2025"], index=0)
with c2:
    claims_view = st.radio("Claims by Placement view", ["Amount", "Share"], horizontal=True, index=0)
with c3:
    st.download_button(
        "Download data (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="monthly_data_2024_2025.csv",
        mime="text/csv",
        use_container_width=True,
    )

# Filtered
if year == "All":
    fdf = df.copy()
else:
    fdf = df[df["date"].dt.year == int(year)].copy()

# Claims by placement (online = total - phone)
claims_df = fdf.copy()
claims_df["claims_total"] = claims_df["claim_amount"].astype(float)
claims_df["claims_phone_calc"] = claims_df["claims_phone"].astype(float)
claims_df["claims_online_calc"] = claims_df["claims_total"] - claims_df["claims_phone_calc"]
claims_df["phone_share"] = claims_df.apply(lambda r: safe_div(r["claims_phone_calc"], r["claims_total"]), axis=1)
claims_df["online_share"] = claims_df.apply(lambda r: safe_div(r["claims_online_calc"], r["claims_total"]), axis=1)
claims_df[["phone_share", "online_share"]] = claims_df[["phone_share", "online_share"]].fillna(0)

# KPIs
phone_claims_per_active = (fdf["claims_phone"] / fdf["active_phone"]).replace([np.inf, -np.inf], np.nan).dropna()
kpis = {
    "joins": fdf["joins_total"].sum(),
    "gmv": fdf["gmv_total"].sum(),
    "claims": fdf["claim_amount"].sum(),
    "netMembers": fdf["net_members"].sum(),
    "activeAvg": fdf["active_total"].mean(),
    "trialCancelAvg": fdf["trial_cancel_pct_total"].mean(),
    "trialConvAvg": fdf["trial_conversion_rate"].mean(),
    "claimsToGmvAvg": fdf["claims_to_gmv"].mean(),
    "phoneClaimsShareAvg": safe_div(fdf["claims_phone"].sum(), fdf["claim_amount"].sum()),
    "phoneClaimsPerActiveAvg": float(phone_claims_per_active.mean()) if len(phone_claims_per_active) else np.nan,
}

# Top months
def top_n(df_, key, n=5, asc=False):
    return df_.sort_values(key, ascending=asc).head(n)

top_joins = top_n(fdf, "joins_total", 5, asc=False)
top_trial_cancel = top_n(fdf, "trial_cancel_pct_total", 5, asc=False)
top_claims_to_gmv = top_n(fdf, "claims_to_gmv", 5, asc=False)

# Analysis (full 2024 vs 2025, like your JS)
y2024 = df[df["date"].dt.year == 2024]
y2025 = df[df["date"].dt.year == 2025]
s2024 = summarize(y2024)
s2025 = summarize(y2025)

worst_claims_to_gmv = df.sort_values("claims_to_gmv", ascending=False).iloc[0]
best_claims_to_gmv = df.sort_values("claims_to_gmv", ascending=True).iloc[0]
max_gmv = df.sort_values("gmv_total", ascending=False).iloc[0]
max_claims = df.sort_values("claim_amount", ascending=False).iloc[0]

deltas = {
    "claimsToGmvAvg": s2025["claimsToGmvAvg"] - s2024["claimsToGmvAvg"],
    "trialCancelAvg": s2025["trialCancelAvg"] - s2024["trialCancelAvg"],
    "trialConvAvg": s2025["trialConvAvg"] - s2024["trialConvAvg"],
    "phoneClaimsShare": s2025["phoneClaimsShare"] - s2024["phoneClaimsShare"],
}

# =========================
# KPI row
# =========================
st.subheader("KPIs")

r1 = st.columns(4)
r1[0].metric("Total Joins", fmt_int(kpis["joins"]), "Sum of monthly joins")
r1[1].metric("Total GMV", fmt_money(kpis["gmv"]), "Sum of Total GMV")
r1[2].metric("Total Claim Amount", fmt_money(kpis["claims"]), "Sum of Claim Amount")
r1[3].metric("Net Members", fmt_int(kpis["netMembers"]), "Sum of Net Members")

r2 = st.columns(4)
r2[0].metric("Avg Active Members", fmt_int(kpis["activeAvg"]), "Mean monthly active_total")
r2[1].metric("Avg Trial Cancel %", fmt_pct(kpis["trialCancelAvg"], 1), "Trial cancels / signups")
r2[2].metric("Avg Trial→Billable Rate", fmt_pct(kpis["trialConvAvg"], 1), "Converted / signups")
r2[3].metric("Claims as % of GMV", fmt_pct(kpis["claimsToGmvAvg"], 1), "claim_amount / gmv_total")

# =========================
# Chart 1: Joins vs Net Members
# =========================
st.subheader("Joins vs Net Members")

fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(
    go.Bar(
        x=fdf["month_label"],
        y=fdf["joins_total"],
        name="Joins (Total)",
        hovertemplate="%{x}<br>Joins: %{y:,.0f}<extra></extra>",
    ),
    secondary_y=False,
)
fig1.add_trace(
    go.Scatter(
        x=fdf["month_label"],
        y=fdf["net_members"],
        mode="lines",
        name="Net Members",
        hovertemplate="%{x}<br>Net Members: %{y:,.0f}<extra></extra>",
    ),
    secondary_y=True,
)
fig1.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h"))
fig1.update_yaxes(title_text="Joins", secondary_y=False)
fig1.update_yaxes(title_text="Net Members", secondary_y=True)
st.plotly_chart(fig1, use_container_width=True)

# =========================
# Chart 2: GMV, Claims, and Claims/GMV
# =========================
st.subheader("GMV, Claims, and Claims / GMV")

fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(
    go.Bar(
        x=fdf["month_label"],
        y=fdf["gmv_total"],
        name="GMV (Total)",
        hovertemplate="%{x}<br>GMV: $%{y:,.0f}<extra></extra>",
    ),
    secondary_y=False,
)
fig2.add_trace(
    go.Scatter(
        x=fdf["month_label"],
        y=fdf["claim_amount"],
        mode="lines",
        name="Claim Amount",
        hovertemplate="%{x}<br>Claims: $%{y:,.0f}<extra></extra>",
    ),
    secondary_y=False,
)
fig2.add_trace(
    go.Scatter(
        x=fdf["month_label"],
        y=fdf["claims_to_gmv"],
        mode="lines",
        name="Claims / GMV",
        hovertemplate="%{x}<br>Claims/GMV: %{y:.2%}<extra></extra>",
    ),
    secondary_y=True,
)
fig2.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h"))
fig2.update_yaxes(title_text="Dollars", secondary_y=False)
fig2.update_yaxes(title_text="Percent", tickformat=".0%", secondary_y=True)
st.plotly_chart(fig2, use_container_width=True)

# =========================
# Claims by Placement
# =========================
st.subheader("Claims by Placement (Online vs Phone)")
st.caption('Based on the workbook claims-by-channel table. "Online" = total claims - phone claims.')

if claims_view == "Amount":
    fig3 = go.Figure()
    fig3.add_trace(
        go.Bar(
            x=claims_df["month_label"],
            y=claims_df["claims_online_calc"],
            name="Online Claims",
            hovertemplate="%{x}<br>Online: $%{y:,.0f}<extra></extra>",
        )
    )
    fig3.add_trace(
        go.Bar(
            x=claims_df["month_label"],
            y=claims_df["claims_phone_calc"],
            name="Phone Claims",
            hovertemplate="%{x}<br>Phone: $%{y:,.0f}<extra></extra>",
        )
    )
    fig3.add_trace(
        go.Scatter(
            x=claims_df["month_label"],
            y=claims_df["claims_total"],
            mode="lines",
            name="Total Claims",
            hovertemplate="%{x}<br>Total: $%{y:,.0f}<extra></extra>",
        )
    )
    fig3.update_layout(barmode="stack", height=380, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h"))
    st.plotly_chart(fig3, use_container_width=True)
else:
    fig3 = go.Figure()
    fig3.add_trace(
        go.Scatter(
            x=claims_df["month_label"],
            y=claims_df["online_share"],
            mode="lines",
            stackgroup="one",
            name="Online Share",
            hovertemplate="%{x}<br>Online Share: %{y:.1%}<extra></extra>",
        )
    )
    fig3.add_trace(
        go.Scatter(
            x=claims_df["month_label"],
            y=claims_df["phone_share"],
            mode="lines",
            stackgroup="one",
            name="Phone Share",
            hovertemplate="%{x}<br>Phone Share: %{y:.1%}<extra></extra>",
        )
    )
    fig3.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h"))
    fig3.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig3, use_container_width=True)

st.caption(
    f"Avg phone share of claims: **{fmt_pct(kpis['phoneClaimsShareAvg'], 1)}** · "
    f"Phone claims per phone active (avg): **{fmt_money(kpis['phoneClaimsPerActiveAvg'], 2) if np.isfinite(kpis['phoneClaimsPerActiveAvg']) else '—'}**"
)

# =========================
# Top months tables
# =========================
st.subheader("Top months")

t1, t2, t3 = st.columns(3)

with t1:
    st.markdown("**Top 5 months by Joins**")
    tmp = top_joins[["month_label", "joins_total"]].copy()
    tmp["joins_total"] = tmp["joins_total"].map(lambda v: f"{v:,.0f}")
    st.dataframe(tmp, hide_index=True, use_container_width=True)

with t2:
    st.markdown("**Top 5 months by Trial Cancel %**")
    tmp = top_trial_cancel[["month_label", "trial_cancel_pct_total"]].copy()
    tmp["trial_cancel_pct_total"] = tmp["trial_cancel_pct_total"].map(lambda v: f"{v:.1%}")
    st.dataframe(tmp, hide_index=True, use_container_width=True)

with t3:
    st.markdown("**Top 5 months by Claims / GMV**")
    tmp = top_claims_to_gmv[["month_label", "claims_to_gmv"]].copy()
    tmp["claims_to_gmv"] = tmp["claims_to_gmv"].map(lambda v: f"{v:.1%}")
    st.dataframe(tmp, hide_index=True, use_container_width=True)

# =========================
# Opportunities, Analysis & Recommendations
# =========================
st.subheader("Opportunities, Analysis & Recommendations")
st.caption("Computed from your workbook (2024 vs 2025 full-year summaries + best/worst months).")

a1, a2, a3, a4 = st.columns(4)
a1.metric("2025 vs 2024: Claims / GMV (avg)", fmt_pct(deltas["claimsToGmvAvg"], 2), "Delta of monthly avg claims_to_gmv")
a2.metric("2025 vs 2024: Trial Cancel % (avg)", fmt_pct(deltas["trialCancelAvg"], 2), "Delta of monthly avg trial_cancel_pct_total")
a3.metric("2025 vs 2024: Trial→Billable (avg)", fmt_pct(deltas["trialConvAvg"], 2), "Delta of monthly avg trial_conversion_rate")
a4.metric("2025 vs 2024: Phone share of claims", fmt_pct(deltas["phoneClaimsShare"], 2), "Delta of total phone_claims / total claims")

left, right = st.columns(2)

with left:
    st.markdown("**Where to look first**")
    st.markdown(
        f"""
- Highest Claims/GMV month: **{ym_label(worst_claims_to_gmv['date'])}** at **{worst_claims_to_gmv['claims_to_gmv']:.2%}**.
- Lowest Claims/GMV month: **{ym_label(best_claims_to_gmv['date'])}** at **{best_claims_to_gmv['claims_to_gmv']:.2%}**.
- Peak GMV month: **{ym_label(max_gmv['date'])}** (**{fmt_money(max_gmv['gmv_total'])}**).
- Peak Claims month: **{ym_label(max_claims['date'])}** (**{fmt_money(max_claims['claim_amount'])}**).
        """.strip()
    )

with right:
    st.markdown("**Recommendations (data-driven)**")
    st.markdown(
        f"""
1. **Investigate claim drivers in the worst Claims/GMV month**: break down claim reasons, retailer/vendor cohorts, and claim amounts (P50/P90) for that month vs baseline.
2. **Reduce phone-claim load if it’s disproportionately high**: phone claims are **{kpis['phoneClaimsShareAvg']:.1%}** of all claims in the selected period—evaluate triage rules, self-serve flows, and agent tooling.
3. **Tie trial cancel and conversion to acquisition and onboarding steps**: identify onboarding changes that coincide with cancel spikes and test improvements in the first 72 hours.
4. **Capacity planning for peak GMV/claims**: use the peak months above to set staffing + vendor targets; aim to hold Claims/GMV closer to the best-month benchmark.
        """.strip()
    )

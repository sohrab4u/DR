import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path






st.set_page_config(page_title="Facility Analytics Dashboard", page_icon="📊", layout="wide")






DEFAULT_FILE = "Count_of_Records_by__1774868240147.xlsx"






st.markdown("""
<style>
:root {
    --bg: #f7f9fc;
    --card: #ffffff;
    --text: #0f172a;
    --muted: #64748b;
    --primary: #2563eb;
    --primary2: #1d4ed8;
    --accent: #f59e0b;
    --border: #e2e8f0;
}
.stApp {
    background: linear-gradient(180deg, #f8fbff 0%, #f1f5f9 100%);
    color: var(--text);
}
.block-container {
    padding-top: 0.8rem;
    padding-bottom: 1.8rem;
    max-width: 1450px;
}
.dashboard-hero {
    background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #3b82f6 100%);
    border-radius: 24px;
    padding: 24px 26px;
    color: white;
    margin-bottom: 1rem;
    box-shadow: 0 14px 32px rgba(37, 99, 235, 0.18);
}
.dashboard-hero h1 {
    margin: 0;
    font-size: 2rem;
    font-weight: 700;
}
.dashboard-hero p {
    margin: 8px 0 0 0;
    color: #dbeafe;
    font-size: 0.98rem;
}
[data-testid="stMetric"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid #dbeafe;
    padding: 14px 16px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f172a;
    margin: 1rem 0 0.55rem 0;
}
.chart-card, .table-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 12px 14px 6px 14px;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
}
.sidebar-note {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border: 1px solid #93c5fd;
    border-radius: 14px;
    padding: 10px 12px;
    color: #1e3a8a;
    font-size: 0.9rem;
    margin-top: 8px;
    margin-bottom: 12px;
    font-weight: 500;
}
.sidebar-section {
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-radius: 16px;
    padding: 12px 12px 8px 12px;
    margin-bottom: 12px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
}
.sidebar-section-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 8px;
}
div[data-baseweb="select"] > div {
    border-radius: 12px !important;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background: #eff6ff;
    border-radius: 12px;
    padding: 10px 16px;
    border: 1px solid #dbeafe;
}
.stTabs [aria-selected="true"] {
    background: #dbeafe !important;
    color: #1d4ed8 !important;
}


/* Sidebar enhancement */
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
    border-right: 1px solid #cbd5e1;
    padding-top: 0.8rem;
    padding-left: 0.7rem;
    padding-right: 0.7rem;
}
[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
    width: 320px;
}
[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
    width: 320px;
    margin-left: -320px;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #0f172a;
}
[data-testid="stSidebar"] .stFileUploader,
[data-testid="stSidebar"] .stMultiSelect,
[data-testid="stSidebar"] .stDateInput {
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-radius: 14px;
    padding: 6px;
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.06);
}
[data-testid="stSidebar"] label {
    color: #0f172a !important;
    font-weight: 600;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #334155;
}
</style>
""", unsafe_allow_html=True)







def resolve_input_file(uploaded_file):
    if uploaded_file is not None:
        return uploaded_file






    local_file = Path(DEFAULT_FILE)
    if local_file.exists():
        return str(local_file)






    app_folder_file = Path(__file__).parent / DEFAULT_FILE
    if app_folder_file.exists():
        return str(app_folder_file)






    return None







def parse_pivot_excel(source):
    raw = pd.read_excel(source, sheet_name=0, header=None)
    rows = raw.where(pd.notnull(raw), None).values.tolist()






    if not rows or len(rows) < 8:
        return pd.DataFrame()






    max_cols = max(len(r) for r in rows)
    rows = [list(r) + [None] * (max_cols - len(r)) for r in rows]






    month_row = rows[4]
    category_row = rows[5]






    header_pairs = []
    current_month = None
    for col in range(1, max_cols):
        month_val = month_row[col]
        category_val = category_row[col]






        if month_val is not None and str(month_val).strip() != "":
            current_month = str(month_val).strip()






        if current_month and category_val is not None and str(category_val).strip() != "":
            header_pairs.append((col, current_month, str(category_val).strip()))






    state = None
    pending_district = None
    records = []






    for row in rows[7:]:
        first_val = row[0]
        first_text = str(first_val).strip() if first_val is not None else ""
        numeric_values = [x for x in row[1:] if isinstance(x, (int, float)) and not pd.isna(x)]






        if not first_text and not numeric_values:
            continue






        if first_text and not numeric_values:
            state = first_text
            pending_district = None
            continue






        if first_text and numeric_values:
            if pending_district is None:
                pending_district = first_text
                continue






            district = pending_district
            facility = first_text






            for col, month, category in header_pairs:
                if col >= len(row):
                    continue
                value = row[col]
                if value is None or str(value).strip() == "":
                    continue
                try:
                    count = float(value)
                except Exception:
                    continue






                records.append({
                    "State": state,
                    "District": district,
                    "Facility": facility,
                    "Month": month,
                    "Referral Category": category,
                    "Count": count
                })






            pending_district = None






    df = pd.DataFrame(records)
    if df.empty:
        return df






    df["Month Date"] = pd.to_datetime(df["Month"], format="%b %Y", errors="coerce")
    df["Month Name"] = df["Month Date"].dt.strftime("%b %Y")
    df["Year"] = df["Month Date"].dt.year
    df["Count"] = pd.to_numeric(df["Count"], errors="coerce").fillna(0)
    df["Referral Category"] = df["Referral Category"].astype(str)






    return df.sort_values(["Month Date", "District", "Facility", "Referral Category"]).reset_index(drop=True)







@st.cache_data(show_spinner=False)
def load_data(uploaded_file):
    source = resolve_input_file(uploaded_file)
    if source is None:
        raise FileNotFoundError(
            "Please upload the Excel file from the sidebar, or keep the default Excel file in the app folder."
        )
    return parse_pivot_excel(source)







st.markdown("""
<div class="dashboard-hero">
    <h1>📊 Facility-wise Referral Analytics Dashboard</h1>
    <p>Upload Excel, auto-detect headers, transform the pivot layout, and analyze referral counts by state, district, facility, month, and category.</p>
</div>
""", unsafe_allow_html=True)






with st.sidebar:
    st.header("Upload and Filters")
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Data Source</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])
    st.markdown('<div class="sidebar-note">Upload the latest pivot export. The dashboard will automatically read month headers, referral categories, and facility-wise values.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)






try:
    df = load_data(uploaded_file)
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()
except Exception as e:
    st.error(f"Error while reading Excel: {e}")
    st.stop()






if df.empty:
    st.warning("No analyzable data found in the uploaded Excel.")
    st.stop()






with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Geography Filters</div>', unsafe_allow_html=True)



    state_options = sorted(df["State"].dropna().unique().tolist())
    selected_states = st.multiselect("State", state_options, default=state_options)



    district_options = sorted(df[df["State"].isin(selected_states)]["District"].dropna().unique().tolist())
    selected_districts = st.multiselect("District", district_options, default=district_options)



    facility_options = sorted(df[df["District"].isin(selected_districts)]["Facility"].dropna().unique().tolist())
    selected_facilities = st.multiselect("Facility", facility_options, default=facility_options)



    st.markdown('</div>', unsafe_allow_html=True)



    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Category and Period</div>', unsafe_allow_html=True)



    category_options = sorted(df["Referral Category"].dropna().unique().tolist())
    selected_categories = st.multiselect("Referral Category", category_options, default=category_options)



    min_date = df["Month Date"].min().date()
    max_date = df["Month Date"].max().date()
    st.markdown("##### Month Range")
    date_col1, date_col2 = st.columns(2)
    with date_col1:
        start_date_input = st.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
    with date_col2:
        end_date_input = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)



    st.markdown('</div>', unsafe_allow_html=True)






filtered_df = df[
    df["State"].isin(selected_states) &
    df["District"].isin(selected_districts) &
    df["Facility"].isin(selected_facilities) &
    df["Referral Category"].isin(selected_categories)
].copy()






start_date = pd.to_datetime(start_date_input)
end_date = pd.to_datetime(end_date_input)





if start_date > end_date:
    st.warning("Start Date cannot be greater than End Date.")
    st.stop()





filtered_df = filtered_df[(filtered_df["Month Date"] >= start_date) & (filtered_df["Month Date"] <= end_date)]






if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()






col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", f"{int(filtered_df['Count'].sum()):,}")
col2.metric("Facilities", int(filtered_df["Facility"].nunique()))
col3.metric("Districts", int(filtered_df["District"].nunique()))
col4.metric("Months", int(filtered_df["Month Name"].nunique()))






monthly_df = (
    filtered_df.groupby(["Month Date", "Referral Category"], as_index=False)["Count"]
    .sum()
    .sort_values(["Month Date", "Referral Category"])
)




facility_df = (
    filtered_df.groupby("Facility", as_index=False)["Count"]
    .sum()
    .sort_values(["Count", "Facility"], ascending=[False, True])
)




district_df = filtered_df.groupby("District", as_index=False)["Count"].sum().sort_values(["Count", "District"], ascending=[False, True])
category_df = filtered_df.groupby("Referral Category", as_index=False)["Count"].sum().sort_values("Count", ascending=False)






month_order = filtered_df[["Month", "Month Date"]].drop_duplicates().sort_values("Month Date")["Month"].tolist()
pivot_df = filtered_df.pivot_table(index="Facility", columns="Month", values="Count", aggfunc="sum", fill_value=0)
pivot_df = pivot_df.reindex(columns=month_order)
pivot_df["Total"] = pivot_df.sum(axis=1)
pivot_df = pivot_df.sort_values("Total", ascending=False)






row1_col1, row1_col2 = st.columns([1.2, 1], gap="large")
with row1_col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig1 = px.line(
        monthly_df,
        x="Month Date",
        y="Count",
        color="Referral Category",
        markers=True,
        title="Monthly Referral Trend",
        color_discrete_sequence=["#2563eb", "#f59e0b"]
    )
    fig1.update_traces(
        mode="lines+markers",
        line=dict(width=3),
        marker=dict(size=9, line=dict(width=2, color="white")),
        hovertemplate=None
    )
    fig1.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Referral Count",
        legend_title="Category",
        height=440,
        margin=dict(l=10, r=10, t=65, b=10),
        hovermode="x unified",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            type="date",
            tickformat="%b %Y",
            showgrid=False
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.18)",
            zeroline=False
        )
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)






with row1_col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    top_facility_df = facility_df.head(10).sort_values(["Count", "Facility"], ascending=[True, True])
    fig2 = px.bar(
        top_facility_df,
        x="Count",
        y="Facility",
        orientation="h",
        color="Count",
        color_continuous_scale=[(0.0, "#bfdbfe"), (0.5, "#60a5fa"), (1.0, "#1d4ed8")],
        text="Count",
        title="Top Facilities by Volume"
    )
    fig2.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        marker_line_color="rgba(255,255,255,0.85)",
        marker_line_width=1.2,
        hovertemplate="<b>%{y}</b><br>Count: %{x:,.0f}<extra></extra>"
    )
    fig2.update_layout(
        template="plotly_white",
        xaxis_title="Referral Count",
        yaxis_title="Facility",
        height=440,
        margin=dict(l=10, r=30, t=65, b=10),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        coloraxis_showscale=False,
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.18)",
            zeroline=False
        ),
        yaxis=dict(
            categoryorder="total ascending",
            showgrid=False
        )
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)






row2_col1, row2_col2 = st.columns(2, gap="large")
with row2_col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig3 = px.pie(
        category_df,
        names="Referral Category",
        values="Count",
        hole=0.55,
        title="Referral Category Contribution",
        color_discrete_sequence=["#2563eb", "#f59e0b", "#10b981", "#ef4444"]
    )
    fig3.update_layout(height=430, margin=dict(l=10, r=10, t=60, b=10))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)






with row2_col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig4 = px.bar(
        district_df.head(10),
        x="District",
        y="Count",
        color="Count",
        color_continuous_scale="Viridis",
        title="Top Districts by Volume"
    )
    fig4.update_layout(
        template="plotly_white",
        xaxis_tickangle=-30,
        height=430,
        margin=dict(l=10, r=10, t=60, b=10)
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)






tab1, tab2 = st.tabs(["Facility Matrix", "Detailed Data"])




with tab1:
    st.markdown('<div class="section-title">Facility x Month Matrix (Descending by Total)</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.dataframe(pivot_df.style.format('{:,.0f}'), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)




with tab2:
    st.markdown('<div class="section-title">Detailed Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.dataframe(
        filtered_df.sort_values(["Facility", "Month Date", "Referral Category"], ascending=[True, True, True]),
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)






csv_data = filtered_df.sort_values(["Facility", "Month Date", "Referral Category"]).to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered CSV",
    data=csv_data,
    file_name="facility_analysis.csv",
    mime="text/csv"
)
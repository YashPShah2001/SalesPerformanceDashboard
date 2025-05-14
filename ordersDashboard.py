import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('cleanOrders.csv')

# Defining the title, layout and sidebar state
st.set_page_config(
    page_title="Sales Performance Dashboard - USA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Defining my sidebar to provide filters based on region cascading with state and further on city for whole dashboard.
st.sidebar.header("Filter Data by Location")
st.sidebar.markdown("Advanced feature 1,2: Cascading filters, Conneted visuals")

regions = sorted(df["region"].dropna().unique())
selected_region = st.sidebar.selectbox("Select Region", ["All"]+ regions)

if selected_region == "All":
    states = sorted(df["state"].dropna().unique())
else:
    states = sorted(df[df["region"] == selected_region]["state"].dropna().unique())
selected_state = st.sidebar.selectbox("Select State",["All"]+ states)

if selected_state == 'All':
    cities = sorted(df["city"].dropna().unique())
else:
    cities = sorted(df[df['state'] == selected_state]['city'].dropna().unique())
selected_city = st.sidebar.selectbox("Select City",['All']+cities)

# Applying region/state/city filters on the dataframe and generating filtered df which is used further for analysing.
filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]
if selected_state != "All":
    filtered_df = filtered_df[filtered_df["state"] == selected_state]
if selected_city != 'All':
    filtered_df = filtered_df[filtered_df['city'] == selected_city]

# Defining a reusable method to calculate the KPI's from df for the year passed.
def calc_metrics(df, year):
    data = df[df["year"] == year]
    return {
        "sales": data["sale_price"].sum(),
        "profit": data["profit"].sum(),
        "orders": data["order_id"].nunique()
    }

metrics_2023 = calc_metrics(filtered_df, 2023)
metrics_2022 = calc_metrics(filtered_df, 2022)

# A reusabale method to calculate percentage change from prev data.
def percent_change(new, old):
    if old == 0:
        return "N/A"
    return f"{((new - old) / old) * 100:.2f}%"

# Now starting to define my dashboard as we have filtered our data based on 
st.title("Sales Performance Dashboard - USA (FY 2022-2023)")

# Subheader Update with respect to selected filters
region_display = selected_region if selected_region != "All" else "All Regions"
state_display = selected_state if selected_state != "All" else "All States"
city_display = selected_city if selected_city !="All" else "All Cities"
st.markdown(f"**Currently viewing data for:** `{region_display}` → `{state_display}` → `{city_display}`")

st.subheader("Summary metrics")
col1, col2, col3 = st.columns(3)

col1.metric(
    label="💰 Total Sales (FY23)",
    value=f"${metrics_2023['sales']:,.2f}",
    delta=percent_change(metrics_2023['sales'], metrics_2022['sales']),
    border=True
)

col2.metric(
    "📈 Total Profit (FY23)",
    f"${metrics_2023['profit']:,.2f}",
    percent_change(metrics_2023['profit'], metrics_2022['profit']),
    border=True
)

col3.metric(
    "🧾 Total Orders (FY23)",
    f"{metrics_2023['orders']:,}",
    percent_change(metrics_2023['orders'], metrics_2022['orders']),
    border=True
)

st.divider()
#-----------------------------------------------------------------------------------------

# Group by Year & Month
monthly_summary = (
    filtered_df.groupby(["year", "month"], as_index=False)
    .agg({"sale_price": "sum", "profit": "sum"})
    .sort_values(["year", "month"])
)
monthly_summary["month"] = monthly_summary["month"].astype(int)
monthly_summary["year"] = monthly_summary["year"].astype(str)

# Sales Line Chart across the months
sales_fig = px.line(
    monthly_summary,
    x="month",
    y="sale_price",
    color="year",
    markers=True,
    labels={"month": "Month", "sale_price": "Sales ($)", "year": "Year"},
    title="Monthly Sales: 2022 vs 2023"
)
sales_fig.update_layout(legend_title_text="Year")

# Profit grouped bar across months
profit_fig = px.bar(
    monthly_summary,
    x="month",
    y="profit",
    color="year",
    barmode="group",
    labels={"month": "Month", "profit": "Profit ($)", "year": "Year"},
    title="Monthly Profit: 2022 vs 2023",
    text_auto=".2s"
)
profit_fig.update_xaxes(tickmode="linear", tick0=1, dtick=1)

# Columns based grid to display Charts Side-by-Side
st.markdown("### Monthly Sales & Profit Trends")
col1, col2 = st.columns(2)
col1.plotly_chart(sales_fig, use_container_width=True)
col2.plotly_chart(profit_fig, use_container_width=True)


st.divider()
#------------------------------------------------------------------------------

# Section to analyse sales & profit across different business dimensions
st.subheader("Comparative Analysis: Profit & Sales by Business Dimensions")
st.markdown("Advanced feature 3,4,5: Conditional content, Dynamic configurations, Connected visuals")
col1,col2,col3,col4 = st.columns(4)
with col1:

    # Radio button to select analysis type
    analysis_metric = st.radio(
        "Choose metric to analyse:",
        options=["Profit", "Sales"],
        horizontal=True,
        index=0
    )
with col2:
    # Radio button to select year
    selected_year = st.radio(
        "Choose year to analyse:",
        options=['2022','2023'],
        horizontal=True,
        index=0
    )

# Filtering data for this section based on year selected.
year_filtered_df = filtered_df[filtered_df["year"] == int(selected_year)]

# Map selection to actual column name based on metrics selected
metric_col = "profit" if analysis_metric == "Profit" else "sale_price"

# Define chart titles based on metrics selected
title_suffix = "Profit ($)" if analysis_metric == "Profit" else "Sales ($)"

col1,col2 = st.columns(2)

with col1:
    # Segment vs Profit/Sales on bar plot
    seg_fig = px.bar(
        year_filtered_df.groupby("segment")[metric_col].sum().reset_index(),
        x="segment", y=metric_col,
        title=f"Segment-wise {title_suffix} - {selected_year}",
        text_auto=".2s"
    )
    st.plotly_chart(seg_fig, use_container_width=True)

with col2:
    # Category vs Profit/Sales distribution using pie
    cat_fig = px.pie(
        year_filtered_df,
        names="category",
        values=metric_col,
        hole=0.4,
        title=f"Category-wise {title_suffix} Distribution - {selected_year}"
    )
    cat_fig.update_traces(textinfo='percent+label')
    st.plotly_chart(cat_fig, use_container_width=True)

# -----------------------------------------------------------------------------------

# To format columns based on relativeness. This is to make the input field not consume whole width of screen.
col1,col2 = st.columns([1,5])
with col1:
    # Let user select number of top/bottom products to display
    num_products = st.number_input(
            "Select number of products to display (Max 50)",
            min_value=1,
            max_value=50,
            value=10,
            step=1
    )
# Filtering top performed products based on metrics selected amnd number of products selected.
top_products = (
            year_filtered_df.groupby("product_id")[metric_col].sum()
            .sort_values(ascending=False)
            .head(num_products)
            .reset_index()
        )
# Filtering worst performed products based on metrics selected amnd number of products selected.
bottom_products = (
            year_filtered_df.groupby("product_id")[metric_col].sum()
            .sort_values(ascending=True)
            .head(num_products)
            .reset_index()
        )

# Utilizing columns to show both graphs side by side.
col1, col2 = st.columns(2)
with col1:
    top_fig = px.bar(
        top_products,
        x=metric_col,
        y="product_id",
        title=f"Top {num_products} Products by {title_suffix} - {selected_year}",
        text_auto=".2s"
    )
    st.plotly_chart(top_fig, use_container_width=True)

with col2:
    bottom_fig = px.bar(
        bottom_products,
        x=metric_col,
        y="product_id",
        title=f"Bottom {num_products} Products by {title_suffix} - {selected_year}",
        text_auto=".2s"
    )
    st.plotly_chart(bottom_fig, use_container_width=True)

# Columns to show the tabular data insights for the top and worst performers
col1,col2= st.columns(2)
with col1:
    with st.expander("Tabular product insights"):
        st.dataframe(top_products,use_container_width=True)
with col2:
    with st.expander("Tabular product insights"):
        st.dataframe(bottom_products,use_container_width=True)

st.divider()
#------------------------------------------------------------------------------
# An expandable section to optionally view the dataset for further insight generation.
with st.expander("View Dataset"):
    st.markdown("Use the filters below to narrow down the data view.")

    # Adding filter widgets for dataframe table
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        segment_filter = st.selectbox(
            "Segment",
            options=["All"] + sorted(filtered_df["segment"].dropna().unique().tolist())
        )

    with col2:
        category_filter = st.selectbox(
            "Category",
            options=["All"] + sorted(filtered_df["category"].dropna().unique().tolist())
        )

    with col3:
        sub_category_filter = st.selectbox(
            "Sub-Category",
            options=["All"] + sorted(filtered_df["sub_category"].dropna().unique().tolist())
        )

    with col4:
        product_id_filter = st.text_input("Search Product ID")

    # Applying the filters selected on the filters.
    table_df = filtered_df.copy()

    if segment_filter != "All":
        table_df = table_df[table_df["segment"] == segment_filter]
    if category_filter != "All":
        table_df = table_df[table_df["category"] == category_filter]
    if sub_category_filter != "All":
        table_df = table_df[table_df["sub_category"] == sub_category_filter]
    if product_id_filter:
        table_df = table_df[table_df["product_id"].str.contains(product_id_filter, case=False, na=False)]

    # Droping unwanted columns to show in the dashboard dataframe.
    table_df = table_df.drop(columns=["region", "state", "city" , "country" , "postal_code", "year", "month"], errors="ignore")

    # Display the filtered and clean table with sorting
    st.dataframe(table_df, use_container_width=True)

import pandas as pd
import streamlit as st
import plotly.express as px
from prophet import Prophet

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Urban_Grocers.csv.xlsx")  # replace with Excel if needed
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()
    df["Revenue"] = df["Units_Sold"] * df["Price_per_Unit"]
    df["Profit"] = df["Revenue"] * 0.14  # assume 14% margin
    return df

df = load_data()

# -----------------------------
# KPI Section
# -----------------------------
st.title("📊 Urban Grocers Case Study Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{df['Revenue'].sum():,.0f}")
col2.metric("Total Units Sold", f"{df['Units_Sold'].sum():,}")
col3.metric("Avg Price per Unit", f"₹{df['Price_per_Unit'].mean():.2f}")
promo_sales = df[df["Promotion"] == 1]["Units_Sold"].sum()
promo_pct = (promo_sales / df["Units_Sold"].sum()) * 100
col4.metric("% Sales via Promotion", f"{promo_pct:.1f}%")

st.markdown("---")

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("🔎 Explore Analysis")
plot_type = st.sidebar.radio(
    "Select Analysis",
    [
        "Overall Demand Trends",
        "Revenue Trends",
        "Category Performance",
        "Top Selling Items per Category",
        "Store Analysis",
        "Promotion Impact",
        "Holiday Effect",
        "Weather Impact",
        "Mode of Purchase",
        "Profitability",
        "Milk Demand Forecast"
    ]
)

# -----------------------------
# Plots
# -----------------------------
if plot_type == "Overall Demand Trends":
    monthly_sales = df.groupby("Month")["Units_Sold"].sum().reset_index()
    fig = px.line(monthly_sales, x="Month", y="Units_Sold", markers=True,
                  title="Overall Monthly Units Sold")
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Revenue Trends":
    monthly_revenue = df.groupby("Month")["Revenue"].sum().reset_index()
    fig = px.line(monthly_revenue, x="Month", y="Revenue", markers=True,
                  title="Overall Monthly Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Category Performance":
    cat_df = df.groupby("Food_Category")[["Units_Sold", "Revenue"]].sum().reset_index()
    fig = px.bar(cat_df, x="Food_Category", y=["Units_Sold", "Revenue"],
                 barmode="group", title="Category-wise Performance")
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Top Selling Items per Category":
    top_items = df.groupby("Food_Category")["Units_Sold"].nlargest(5).reset_index()
    st.write("🚀 Top Selling Items per Category")
    st.dataframe(top_items)

elif plot_type == "Store Analysis":
    store_df = df.groupby("Store_ID")[["Units_Sold", "Revenue"]].sum().reset_index()
    fig = px.bar(store_df, x="Store_ID", y=["Units_Sold", "Revenue"],
                 barmode="group", title="Store-wise Sales & Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Promotion Impact":
    promo_df = df.groupby("Promotion")[["Units_Sold", "Revenue"]].mean().reset_index()
    promo_df["Promotion"] = promo_df["Promotion"].map({0: "No Promotion", 1: "Promotion"})
    fig = px.bar(promo_df, x="Promotion", y=["Units_Sold", "Revenue"],
                 barmode="group", title="Impact of Promotion on Sales & Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Holiday Effect":
    holiday_df = df.groupby("Holiday_Weekend")[["Units_Sold", "Revenue"]].mean().reset_index()
    holiday_df["Holiday_Weekend"] = holiday_df["Holiday_Weekend"].map({0: "Non-Holiday", 1: "Holiday"})
    fig = px.bar(holiday_df, x="Holiday_Weekend", y=["Units_Sold", "Revenue"],
                 barmode="group", title="Holiday vs Non-Holiday Sales")
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Weather Impact":
    weather_df = df.groupby("Weather")[["Units_Sold", "Revenue"]].mean().reset_index()
    fig = px.bar(weather_df, x="Weather", y=["Units_Sold", "Revenue"],
                 barmode="group", title="Weather Impact on Sales")
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Mode of Purchase":
    mode_df = df["Mode_Purchase"].value_counts().reset_index()
    mode_df.columns = ["Mode", "Count"]
    fig = px.pie(mode_df, names="Mode", values="Count", title="Mode of Purchase Distribution")
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Profitability":
    profit_df = df.groupby("Food_Category")[["Profit"]].sum().reset_index()
    fig = px.bar(profit_df, x="Food_Category", y="Profit",
                 title="Profit Contribution by Category", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Milk Demand Forecast":
    milk_df = df[df["Food_Category"] == "Milk"].groupby("Month")["Units_Sold"].sum().reset_index()
    milk_df = milk_df.rename(columns={"Month": "ds", "Units_Sold": "y"})
    if len(milk_df) > 2:
        m = Prophet()
        m.fit(milk_df)
        future = m.make_future_dataframe(periods=4, freq="M")
        forecast = m.predict(future)
        fig = px.line(forecast, x="ds", y="yhat", title="Milk Demand Forecast (Next 4 Months)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Not enough data for forecasting.")

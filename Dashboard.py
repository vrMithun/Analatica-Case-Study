import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Urban_Grocers.csv.xlsx")
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()
    df["Revenue"] = df["Units_Sold"] * df["Price_per_Unit"]
    df["Profit"] = df["Revenue"] * 0.14
    return df

df = load_data()

# -----------------------------
# KPI Section
# -----------------------------
st.title("📊 Urban Grocers Case Study Dashboard")

col1, col2, col3, col4 = st.columns(4)

total_revenue = f"₹{df['Revenue'].sum():,.2f}"
total_units = f"{df['Units_Sold'].sum():,}"
avg_price = f"₹{df['Price_per_Unit'].mean():.2f}"
promo_sales = df[df["Promotion"] == 1]["Units_Sold"].sum()
promo_pct = (promo_sales / df["Units_Sold"].sum()) * 100

col1.write("**Total Revenue**")
col1.write(total_revenue)

col2.write("**Total Units Sold**")
col2.write(total_units)

col3.write("**Avg Price/Unit**")
col3.write(avg_price)

col4.write("**Sales via Promotion**")
col4.write(f"{promo_pct:.1f}%")


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
        "Top Selling Categories",
        "Store Analysis",
        "Promotion Impact",
        "Promotion vs. Price",
        "Holiday Effect",
        "Weather Impact",
        "Mode of Purchase",
        "Profitability",
        "Food Category Demand Forecast",
        "Investment Status"
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
    metric = st.radio("Choose Metric", ["Units_Sold", "Revenue"], horizontal=True)
    cat_df = df.groupby("Food_Category")[[metric]].sum().reset_index()
    fig = px.bar(cat_df, x="Food_Category", y=metric,
                 title=f"Category-wise {metric}", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Top Selling Categories":
    top_n = st.slider("Select Top N Categories", 3, 10, 5)
    metric = st.radio("Choose Metric", ["Units_Sold", "Revenue"], horizontal=True)
    cat_sales = df.groupby("Food_Category")[[metric]].sum().reset_index()
    top_cats = cat_sales.sort_values(by=metric, ascending=False).head(top_n)
    fig = px.bar(top_cats, x="Food_Category", y=metric,
                 title=f"Top {top_n} Categories by {metric}", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    fig2 = px.pie(top_cats, names="Food_Category", values=metric,
                  title=f"Share of Top {top_n} Categories")
    st.plotly_chart(fig2, use_container_width=True)

elif plot_type == "Store Analysis":
    store_df = df.groupby("Store_ID")[["Units_Sold", "Revenue"]].sum().reset_index()
    fig = px.bar(store_df, x="Store_ID", y="Revenue", text_auto=True,
                 title="Store-wise Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Promotion Impact":
    promotion_view = st.radio(
        "Select Impact View",
        ["Overall Impact", "Impact by Category"],
        horizontal=True
    )
    
    if promotion_view == "Overall Impact":
        promo_df = df.groupby("Promotion")[["Units_Sold", "Revenue"]].mean().reset_index()
        promo_df["Promotion"] = promo_df["Promotion"].map({0: "No Promotion", 1: "Promotion"})
        fig = px.bar(promo_df, x="Promotion", y=["Units_Sold", "Revenue"],
                     barmode="group", title="Overall Impact of Promotion on Sales & Revenue")
        st.plotly_chart(fig, use_container_width=True)
        
    elif promotion_view == "Impact by Category":
        promo_impact_df = df.pivot_table(index='Food_Category', columns='Promotion', values='Units_Sold', aggfunc='mean')
        promo_impact_df.columns = ['No Promotion', 'Promotion']
        promo_impact_df['Percentage_Change'] = (
            (promo_impact_df['Promotion'] - promo_impact_df['No Promotion']) / promo_impact_df['No Promotion']
        ) * 100
        fig = px.bar(promo_impact_df.reset_index(), x='Food_Category', y='Percentage_Change', title='Promotion Impact by Food Category')
        fig.update_yaxes(title='Percentage Change in Sales')
        st.plotly_chart(fig, use_container_width=True)

elif plot_type == "Promotion vs. Price":
    promo_price_df = df.groupby(['Food_Category', 'Promotion'])['Price_per_Unit'].mean().reset_index()
    promo_price_df["Promotion"] = promo_price_df["Promotion"].map({0: "No Promotion", 1: "Promotion"})
    
    fig = px.bar(
        promo_price_df, 
        x="Food_Category", 
        y="Price_per_Unit", 
        color="Promotion", 
        barmode="group",
        title="Average Price per Unit: Promotion vs. No Promotion",
        labels={
            "Price_per_Unit": "Average Price per Unit",
            "Food_Category": "Food Category"
        }
    )
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

elif plot_type == "Food Category Demand Forecast":
    st.subheader("📈 Food Category Demand Forecast")
    
    # Select Food Category
    food_categories = df['Food_Category'].unique()
    selected_cat = st.selectbox("Select Food Category for Forecast", food_categories)
    
    # Aggregate daily sales
    cat_df = df[df['Food_Category'] == selected_cat][['Date', 'Units_Sold']].groupby('Date').sum().reset_index()
    cat_df = cat_df.rename(columns={'Date': 'ds', 'Units_Sold': 'y'})
    
    if len(cat_df) > 2:
        # Step 1: Fill missing Dec 21–31, 2024
        model_dec = Prophet(daily_seasonality=True, yearly_seasonality=True, weekly_seasonality=True)
        model_dec.fit(cat_df)
        future_dec = model_dec.make_future_dataframe(periods=11, freq='D')
        forecast_dec = model_dec.predict(future_dec)
        dec_missing = forecast_dec.set_index('ds').loc['2024-12-21':'2024-12-31', ['yhat']].rename(columns={'yhat':'y'})
        filled_cat_data = pd.concat([cat_df.set_index('ds'), dec_missing]).reset_index()

        # Step 2: Retrain on completed dataset
        model_final = Prophet(daily_seasonality=True, yearly_seasonality=True, weekly_seasonality=True)
        model_final.fit(filled_cat_data.rename(columns={'index':'ds'}))

        # Step 3: Forecast next 3 months (Jan–Mar 2025)
        future_q1 = model_final.make_future_dataframe(periods=90, freq='D')
        forecast_q1 = model_final.predict(future_q1)
        forecast_future = forecast_q1[(forecast_q1['ds'] > '2024-12-31') & (forecast_q1['ds'] <= '2025-03-31')]

        # Aggregate to monthly totals
        forecast_monthly = forecast_future.set_index('ds').resample('M').sum()
        # Format index for readability
        forecast_monthly.index = forecast_monthly.index.strftime('%b %Y')

        # Plot
        fig = go.Figure()
        # Historical monthly sales
        hist_monthly = filled_cat_data.set_index('ds').resample('M').sum()
        hist_monthly.index = hist_monthly.index.strftime('%b %Y')  # keep full history readable
        fig.add_trace(go.Scatter(
            x=hist_monthly.index, y=hist_monthly['y'], mode='markers', name='Historical Sales'
        ))
        # Forecast line
        fig.add_trace(go.Scatter(
            x=forecast_monthly.index, y=forecast_monthly['yhat'], mode='lines', name='Forecasted Sales'
        ))
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_monthly.index, y=forecast_monthly['yhat_lower'], fill=None, mode='lines',
            line_color='rgba(0,0,0,0)', showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=forecast_monthly.index, y=forecast_monthly['yhat_upper'], fill='tonexty', mode='lines',
            line_color='rgba(0,0,255,0.2)', name='Confidence Interval'
        ))

        fig.update_layout(
            title=f"{selected_cat} Demand Forecast (Jan–Mar 2025)",
            yaxis_title='Units Sold',
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

        # Table: Forecast values with thresholds
        forecast_table = forecast_monthly[['yhat', 'yhat_lower', 'yhat_upper']].copy()
        forecast_table = forecast_table.rename(columns={
            'yhat': 'Forecast',
            'yhat_lower': 'Min Threshold',
            'yhat_upper': 'Max Threshold'
        })
        forecast_table.index.name = 'Month'
        st.markdown("### Forecast Table with Min/Max Thresholds")
        st.dataframe(forecast_table.style.format("{:.0f}"))
        
    else:
        st.warning("⚠️ Not enough data for forecasting.")



elif plot_type == "Investment Status":
    total_revenue = df['Revenue'].sum()
    total_profit = df['Profit'].sum()
    initial_investment = 200_000_000
    shortfall = initial_investment - total_profit

    st.header("Investment Status")
    st.markdown("---")
    
    st.subheader(f"Total Profit: ₹{total_profit:,.2f}")
    st.subheader(f"Initial Investment: ₹{initial_investment:,.2f}")
    st.subheader(f"Remaining Shortfall: ₹{shortfall:,.2f}")
    st.warning("⚠️ The company has a significant shortfall and has not yet recovered its initial investment.")

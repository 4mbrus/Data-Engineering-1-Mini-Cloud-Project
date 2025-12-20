import streamlit as st
import pandas as pd
import numpy as np
import datetime
import altair as alt
import os

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Media Monitor Dashboard",
    page_icon="📰",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. Data Loading & Processing
# -----------------------------------------------------------------------------
@st.cache_data
def load_and_process_data(topics_file, economy_file):
    """Loads all data at once to ensure consistency."""
    data = {}
    
    # --- A. Load Topic Data ---
    try:
        df_topics = pd.read_csv(topics_file)
        
        # Clean and Organize
        df_topics['date_obj'] = pd.to_datetime(df_topics['month_year'])
        # Sort chronologically
        df_topics = df_topics.sort_values('date_obj', ascending=True) 
        
        # Get list of unique months for the slider/selector (Text format)
        unique_months = df_topics['month_year'].unique().tolist()
        # Sort them just in case
        unique_months.sort(key=lambda date: datetime.datetime.strptime(date, "%Y-%m"))
        
        data['topics_df'] = df_topics
        data['available_months'] = unique_months
        
    except Exception as e:
        st.error(f"Error loading topics file: {e}")
        data['topics_df'] = pd.DataFrame()
        data['available_months'] = []

    # --- B. Load Economy Data  ---
    try:
        df_eco = pd.read_csv(economy_file)
        df_eco['date_obj'] = pd.to_datetime(df_eco['month_year'])
        
        # Sort descending for the rolling chart (Newest first)
        df_eco = df_eco.sort_values('date_obj', ascending=False).head(12)
        
        # Melt for Altair (Wide -> Long)
        df_eco_long = df_eco.melt(
            id_vars=['month_year', 'date_obj'], 
            value_vars=['cnn_sentiment', 'fox_sentiment'],
            var_name='SourceRaw', 
            value_name='Negative Articles'
        )
        source_map = {'cnn_sentiment': 'CNN', 'fox_sentiment': 'FOX'}
        df_eco_long['Source'] = df_eco_long['SourceRaw'].map(source_map)
        df_eco_long['MonthLabel'] = df_eco_long['date_obj'].dt.strftime("%b %Y")
        
        data['economy_df'] = df_eco_long
        
    except Exception as e:
        # If file missing, return empty but don't crash
        data['economy_df'] = pd.DataFrame()

    return data

def get_topics_for_month(df, month_str, source):
    """Filters the big dataframe for a specific month and news source."""
    if df.empty:
        return pd.DataFrame()

    # Filter
    mask = (df['month_year'] == month_str) & (df['news_site'] == source)
    row = df[mask]
    
    if row.empty:
        return pd.DataFrame()

    # The columns that contain our topic counts
    topic_cols = [
        'topic_inflation_sum', 'topic_taxes_sum', 'topic_stocks_sum', 
        'topic_jobs_sum', 'topic_housing_sum', 'topic_energy_sum', 'topic_crypto_sum'
    ]
    
    # Extract values and clean up names (remove "topic_" and "_sum")
    clean_data = []
    for col in topic_cols:
        val = row.iloc[0][col]
        # Handle NaN/None values (treat as 0)
        if pd.isna(val):
            val = 0
            
        topic_name = col.replace('topic_', '').replace('_sum', '').capitalize()
        clean_data.append({"Topic": topic_name, "Percentage": int(val)})
        
    return pd.DataFrame(clean_data).sort_values("Percentage", ascending=False)

# -----------------------------------------------------------------------------
# 3. Chart Helper (UPDATED: White Text Inside Horizontal Bars)
# -----------------------------------------------------------------------------
def make_topic_chart(df, color_hex):
    if df.empty:
        return alt.Chart(pd.DataFrame({'A':[]})).mark_text().encode(text=alt.value("No data"))

    base = alt.Chart(df).encode(
        x=alt.X('Percentage', axis=None), 
        y=alt.Y('Topic', sort=None, axis=alt.Axis(title=None, labelFontSize=12)), 
    )
    
    # Bars
    bars = base.mark_bar(color=color_hex, cornerRadiusEnd=4).encode(tooltip=['Topic', 'Percentage'])
    
    # Text (Inside the bar, aligned right, white)
    text = base.mark_text(
        align='right',      # Anchor text at the end of the bar
        baseline='middle', 
        dx=-5,              # Move text 5px LEFT (inside)
        color='white'       # White text
    ).encode(text='Percentage')
    
    return (bars + text).configure_view(strokeWidth=0).properties(height=300)

# -----------------------------------------------------------------------------
# 4. Main Application Logic
# -----------------------------------------------------------------------------

# --- Files (Ensure these match your filenames on EC2) ---
TOPICS_FILE = "https://business-news-sentiments.s3.eu-west-1.amazonaws.com/news_sentiments_monthly/topic_breakdown/monthly_topic_breakdown.csv"  
ECONOMY_FILE = "https://business-news-sentiments.s3.eu-west-1.amazonaws.com/news_sentiments_monthly/sentiment/monthly_combined_sentiments.csv"


# Load Data
data_store = load_and_process_data(TOPICS_FILE, ECONOMY_FILE)
available_months = data_store['available_months']

# --- Session State for Month Navigation ---
if 'month_index' not in st.session_state:
    # Default to the last month (latest)
    st.session_state.month_index = len(available_months) - 1

def prev_month():
    if st.session_state.month_index > 0:
        st.session_state.month_index -= 1

def next_month():
    if st.session_state.month_index < len(available_months) - 1:
        st.session_state.month_index += 1

# If we have data, get the current selected month string
if available_months:
    current_month_str = available_months[st.session_state.month_index]
else:
    current_month_str = "No Data"

# -----------------------------------------------------------------------------
# 5. Layout
# -----------------------------------------------------------------------------
st.title("📰 Media Monitor: Economy")

# --- Month Selector (Top of page) ---
col_nav1, col_nav2, col_nav3 = st.columns([1, 6, 1])
with col_nav1:
    st.button("⬅️ Prev", on_click=prev_month, use_container_width=True)
with col_nav3:
    st.button("Next ➡️", on_click=next_month, use_container_width=True)
with col_nav2:
    st.markdown(f"<h3 style='text-align: center; margin-top: 0;'>📅 Viewing Data: {current_month_str}</h3>", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2, gap="large")

# --- LEFT COLUMN: CNN ---
with col1:
    st.markdown('<img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/CNN.svg" height="100">', unsafe_allow_html=True)
    st.subheader(f"Topic Focus (% of artcles - {current_month_str})")
    
    # Get Data for this specific month
    cnn_topics = get_topics_for_month(data_store['topics_df'], current_month_str, "CNN")
    st.altair_chart(make_topic_chart(cnn_topics, "#CC0000"), width="stretch")

# --- RIGHT COLUMN: FOX NEWS ---
with col2:
    st.markdown('<img src="https://upload.wikimedia.org/wikipedia/commons/6/67/Fox_News_Channel_logo.svg" height="100">', unsafe_allow_html=True)
    st.subheader(f"Topic Focus (% of artcles - {current_month_str})")
    
    # Get Data for this specific month
    fox_topics = get_topics_for_month(data_store['topics_df'], current_month_str, "FOX")
    st.altair_chart(make_topic_chart(fox_topics, "#003366"), width="stretch")

# -----------------------------------------------------------------------------
# 6. Bottom Section: Economy Sentiment (Rolling 12 Months)
# -----------------------------------------------------------------------------
st.markdown("---")
st.header("📉 Percentage of Articles With Negative Economic Sentiment (Rolling 12 Months)")

with st.container():
    economy_df = data_store['economy_df']
    
    if not economy_df.empty:
        # Define the colors
        color_scale = alt.Scale(domain=['CNN', 'FOX'], range=['#CC0000', '#003366'])

        # 1. Base Chart (Encodes X, Y, AND Color here so both bars and text use it)
        base = alt.Chart(economy_df).encode(
            x=alt.X('MonthLabel', sort=alt.EncodingSortField(field="date_obj", order='ascending'), title=None),
            xOffset='Source', 
            y=alt.Y('Negative Articles', title="Article Count"),
            color=alt.Color('Source', scale=color_scale), # <--- Color defined here applies to text too
            tooltip=['MonthLabel', 'Source', 'Negative Articles']
        )
        
        # 2. Bars
        bars = base.mark_bar()
        
        # 3. Text (OUTSIDE Top, Matches Bar Color)
        text = base.mark_text(
            align='center',
            baseline='bottom',  # Sits on top of the value
            dy=-5,              # Nudge UP 5px (Negative = Outside/Up)
            fontSize=12,
            fontWeight='bold'
        ).encode(
            text='Negative Articles'
        )
        
        final_chart = (bars + text).properties(
            height=400
        ).interactive()
        
        st.altair_chart(final_chart, width="stretch")
        
    else:
        st.warning(f"Could not load economy data. Ensure '{ECONOMY_FILE}' is uploaded.")
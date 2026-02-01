import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Crime Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/crime_data.csv")

# Try loading data safely
try:
    data = load_data()
except:
    data = None

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Dataset Overview", "Data Analysis", "Screenshots", "About Research"]
)

# -------------------------------
# Home Page
# -------------------------------
if page == "Home":

    st.title("📊 Crime Data Analysis Dashboard")
    st.subheader("Exploratory Analysis of Crime Patterns in Mpumalanga")

    st.markdown("""
    ### Welcome
    This dashboard showcases my research on **crime analysis and hotspot identification**
    using data visualization and statistical analysis.

    It is based on recorded crime data containing:
    - Police stations
    - Crime categories
    - Geographic coordinates
    - Yearly crime counts
    """)

    st.image("assets/cover.jpeg", caption="Crime Analysis Overview", use_container_width=True)

# -------------------------------
# Dataset Overview
# -------------------------------
elif page == "Dataset Overview":

    st.title("📁 Dataset Overview")

    if data is not None:

        st.write("### Sample Records")
        st.dataframe(data.head(50))

        st.write("### Dataset Shape")
        st.write(f"Rows: {data.shape[0]}")
        st.write(f"Columns: {data.shape[1]}")

        st.write("### Column Names")
        st.write(list(data.columns))

        st.write("### Missing Values")
        st.dataframe(data.isnull().sum())

        st.write("### Basic Statistics")
        st.dataframe(data.describe())

    else:
        st.warning("Dataset not found. Please add crime_data.csv in the data folder.")

# -------------------------------
# Data Analysis Page
# -------------------------------
elif page == "Data Analysis":

    st.title("📈 Data Analysis & Trends")

    if data is not None:

        # ---------------------------
        # Crime by Police Station
        # ---------------------------
        st.subheader("🏢 Crime by Police Station")

        station_counts = data.groupby("station")["crime_count"].sum().sort_values(ascending=False).head(15)

        fig1, ax1 = plt.subplots()
        station_counts.plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Total Crime Count")
        ax1.set_title("Top 15 Police Stations by Crime Volume")
        st.pyplot(fig1)

        # ---------------------------
        # Crime by Category (Separated & Clear)
        # ---------------------------
        st.subheader("📂 Crime by Category (Clear View)")

        category_counts = data.groupby("category")["crime_count"].sum().sort_values(ascending=False)

        # Show only top 8 categories to avoid congestion
        top_categories = category_counts.head(8)
        others = category_counts.iloc[8:].sum()

        if others > 0:
            top_categories["Others"] = others

        fig2, ax2 = plt.subplots(figsize=(7, 7))

        wedges, texts, autotexts = ax2.pie(
            top_categories,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.8
        )

        ax2.set_title("Crime Distribution by Category (Top Categories)")

        # Add legend on the side
        ax2.legend(
            wedges,
            top_categories.index,
            title="Categories",
            loc="center left",
            bbox_to_anchor=(1, 0.5)
        )

        st.pyplot(fig2)

        # ---------------------------
        # Crime Trend Over Time
        # ---------------------------
        st.subheader("📅 Crime Trend Over Years")

        yearly_trend = data.groupby("year")["crime_count"].sum()

        fig3, ax3 = plt.subplots()
        yearly_trend.plot(marker="o", ax=ax3)
        ax3.set_xlabel("Year")
        ax3.set_ylabel("Total Crimes")
        ax3.set_title("Yearly Crime Trend")
        st.pyplot(fig3)

        # ---------------------------
        # All Stations Locations
        # ---------------------------
        st.subheader("📍 All Police Stations Map")

        # Get unique station locations
        station_locations = data.groupby(
            ["station", "location_x", "location_y"]
        )["crime_count"].sum().reset_index()

        st.dataframe(station_locations)

        # ---------------------------
        # Interactive Map (All Stations)
        # ---------------------------
        st.subheader("🗺️ Police Stations Map")

        st.map(
            station_locations.rename(
                columns={
                    "location_y": "lat",
                    "location_x": "lon"
                }
            )
        )

        # ---------------------------
        # Top Hotspot Locations
        # ---------------------------
        st.subheader("🔥 Top Crime Hotspots")

        hotspot_data = data.groupby([
            "location_x",
            "location_y"
        ])["crime_count"].sum().reset_index()

        hotspot_data = hotspot_data.sort_values("crime_count", ascending=False).head(20)

        st.dataframe(hotspot_data)

        # ---------------------------
        # Hotspot Map
        # ---------------------------
        st.subheader("🚨 Hotspot Map")

        st.map(
            hotspot_data.rename(
                columns={
                    "location_y": "lat",
                    "location_x": "lon"
                }
            )
        )

    else:
        st.warning("No data available for analysis.")

# -------------------------------
# Screenshots Page
# -------------------------------
elif page == "Screenshots":

    st.title("🖼️ Research Screenshots")

    st.markdown("""
    This section presents screenshots of
    model comparison of models developed during research.
    """)

    screenshot_folder = "screenshots"

    if os.path.exists(screenshot_folder):

        images = os.listdir(screenshot_folder)

        if len(images) > 0:
            for img in images:
                st.image(
                    os.path.join(screenshot_folder, img),
                    caption=img,
                    use_container_width=True
                )
        else:
            st.info("No screenshots found in the folder.")

    else:
        st.warning("Please create a 'screenshots' folder and add your images.")

# -------------------------------
# About Research Page
# -------------------------------
elif page == "About Research":

    st.title("📚 About This Research")

    st.markdown("""
    ### Title
    **Predicting Crime Hotspots in Mpumalanga, South Africa Using Data Analysis Techniques**

    ### Dataset Columns
    - station
    - category
    - location_x (longitude)
    - location_y (latitude)
    - year
    - crime_count

    ### Objectives
    - Explore spatial and temporal crime patterns
    - Identify high-risk areas
    - Support crime prevention strategies
    - Present findings visually

    ### Methodology
    1. Data Collection
    2. Data Cleaning
    3. Exploratory Data Analysis (EDA)
    4. Visualization
    5. Interpretation of Results
    6. Dashboard Development

    ### Tools Used
    - Python
    - Pandas & NumPy
    - Matplotlib
    - Streamlit

    ### Author
    Honour's Student in Data Science & AI
    TUMI Magwagwa
    """)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("© 2026 | Crime Data Analysis Dashboard")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #fff9f0;
            color: #333333;
        }
        h1, h2, h3 {
            color: #a10000;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stSelectbox, .stButtton{
            display:inline-block;
            vertical-align:middle;
        }
        .stColumns{
            display:flex;
            justify-content:space-between;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>🎬 Netflix Data Visualization Dashboard</h1>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📂 Upload Your Netflix CSV File")

# 📁 File Upload
uploaded_file = st.file_uploader("Upload your file here", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')

    st.markdown("### 👀 Data Preview")
    st.dataframe(df.head())
    
    st.markdown("### shape of the DataFrame")
    st.write(f"The dataset contains **{df.shape[0]} rows** and **{df.shape[1]} columns**.")
   
    st.markdown("### summary statistics")
    st.dataframe(df.describe())

    # 🎯 Chart Options
    st.markdown("---")
    st.markdown("### 📊 Choose Your Visualization")

    chart_options = {
        "Top 10 Genres": "genres",
        "Movies vs TV Shows Over the Years": "trend",
        "Top 10 Countries": "countries",
        "Content Added Per Year": "yearly",
        "Top 10 Directors": "directors",
        "Distribution of Movie Durations (1990s)": "duration_90s",
        "Netflix Releases Over the Years (Line Plot)": "release_line",
        "Count of Movies vs TV Shows (Bar Chart)": "count_type",
        "Top 10 Genres of Movies Released in 2000": "genres_2000"
    }

    # with st.container():
    #     col1, col2 = st.columns([3, 1])
    #     with col1:
    #         selected_chart = st.selectbox("Choose a chart:", list(chart_options.keys()))
    #     with col2:
    #         generate = st.button("Generate Chart")
    
    selected_chart = st.selectbox("Choose a chart:", list(chart_options.keys()))
    generate = st.button("Generate Chart")

    if generate:
        st.markdown("---")
        st.markdown(f"### 📈 {selected_chart}")
        fig, ax = plt.subplots(figsize=(10, 6))

        if chart_options[selected_chart] == "genres":
            top_genres = df['genre'].value_counts().head(10)
            sns.barplot(x=top_genres.values, y=top_genres.index, palette='viridis', ax=ax)
            ax.set_xlabel("Count")

        elif chart_options[selected_chart] == "trend":
            content_trend = df.groupby(['release_year', 'type']).size().reset_index(name='count')
            sns.lineplot(data=content_trend, x='release_year', y='count', hue='type', marker='o', ax=ax)
            ax.set_xlabel("Release Year")
            ax.set_ylabel("Number of Releases")

        elif chart_options[selected_chart] == "countries":
            top_countries = df['country'].value_counts().head(10)
            sns.barplot(x=top_countries.values, y=top_countries.index, palette='magma', ax=ax)
            ax.set_title("Top 10 Countries with Most Netflix Content")
            ax.set_xlabel("Count")

        elif chart_options[selected_chart] == "yearly":
            sns.countplot(data=df, x='year_added', order=df['year_added'].value_counts().sort_index().index, ax=ax)
            plt.xticks(rotation=45)

        elif chart_options[selected_chart] == "directors":
            top_directors = df['director'].dropna().str.split(', ').explode().value_counts().head(10)
            sns.barplot(x=top_directors.values, y=top_directors.index, palette='mako', ax=ax)
            ax.set_xlabel("Number of Titles")

        elif chart_options[selected_chart] == "duration_90s":
            subset = df[(df['type'] == 'Movie') & (df['release_year'].between(1990, 1999))]
            sns.histplot(data=subset, x='duration', bins=20, kde=True, ax=ax)
            ax.set_xlabel("Duration (minutes)")

        elif chart_options[selected_chart] == "release_line":
            counts = df['release_year'].value_counts().sort_index()
            counts.plot(kind='line', marker='o', ax=ax)
            ax.set_xlabel("Year")
            ax.set_ylabel("Number of Titles")
            ax.grid(True)

        elif chart_options[selected_chart] == "count_type":
            df['type'].value_counts().plot(kind='bar', color=['salmon', 'skyblue'], ax=ax)
            ax.set_xlabel("Type")
            ax.set_ylabel("Number of Titles")

        elif chart_options[selected_chart] == "genres_2000":
            movies_2000 = df[(df['type'] == 'Movie') & (df['release_year'] == 2000)]
            genres_2000 = movies_2000['genre'].str.split(', ').explode()
            top_genres_2000 = genres_2000.value_counts().head(10)
            sns.barplot(x=top_genres_2000.values, y=top_genres_2000.index, palette='Set2', ax=ax)
            ax.set_xlabel("Number of Movies")
            ax.set_ylabel("Genre")

        st.pyplot(fig)

else:
    st.markdown("Please upload a Netflix dataset (CSV) to get started.")

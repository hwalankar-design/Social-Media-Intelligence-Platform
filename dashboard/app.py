
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Social Media Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# 2. DASHBOARD TITLE
# --------------------------------

st.title("📊 Social Media Intelligence Platform")

st.write(
    "Analyze social media posts, sentiment, trending topics, "
    "misinformation signals, and influencer engagement."
)

# --------------------------------
# 3. SIDEBAR NAVIGATION
# --------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Dashboard Section",
    [
        "Overview",
        "Sentiment Analysis",
        "Trending Topics",
        "Misinformation Screening",
        "Influencer Analysis"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Social Media Intelligence Platform\n\n"
    "Data Science Project - 2026"
)

# --------------------------------
# 4. LOAD PROJECT DATASETS
# --------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

sentiment_data = pd.read_csv(
    BASE_DIR / "data" / "sentiment_results.csv"
)

topic_data = pd.read_csv(
    BASE_DIR / "data" / "topic_results.csv"
)

misinformation_data = pd.read_csv(
    BASE_DIR / "data" / "misinformation_results.csv"
)

influencer_data = pd.read_csv(
    BASE_DIR / "data" / "influencer_results.csv"
)

cleaned_data = pd.read_csv(
    BASE_DIR / "data" / "cleaned_posts.csv"
)

# --------------------------------
# 5. SIDEBAR DOWNLOAD OPTIONS
# --------------------------------

st.sidebar.success(f"Currently viewing: {page}")

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Download Data")

st.sidebar.download_button(
    label="Download Social Media Dataset",
    data=cleaned_data.to_csv(index=False).encode("utf-8"),
    file_name="social_media_dataset.csv",
    mime="text/csv",
    key="dataset_download"
)

st.sidebar.download_button(
    label="Download Influencer Report",
    data=influencer_data.to_csv(index=False).encode("utf-8"),
    file_name="influencer_report.csv",
    mime="text/csv",
    key="influencer_download"
)

# --------------------------------
# 6. OVERVIEW PAGE
# --------------------------------

if page == "Overview":

    st.header("📈 Overall Statistics")

    total_posts = len(sentiment_data)

    total_influencers = len(influencer_data)

    total_engagement = (
        sentiment_data["likes"].sum()
        + sentiment_data["comments"].sum()
        + sentiment_data["shares"].sum()
    )

    positive_posts = (
        sentiment_data["sentiment"] == "Positive"
    ).sum()

    negative_posts = (
        sentiment_data["sentiment"] == "Negative"
    ).sum()

    neutral_posts = (
        sentiment_data["sentiment"] == "Neutral"
    ).sum()

    # Six dashboard metric cards
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("Total Posts", total_posts)

    with col2:
        st.metric("Total Influencers", total_influencers)

    with col3:
        st.metric("Positive Posts", int(positive_posts))

    with col4:
        st.metric("Negative Posts", int(negative_posts))

    with col5:
        st.metric("Neutral Posts", int(neutral_posts))

    with col6:
        st.metric("Total Engagement", int(total_engagement))

    # Posts by Username
    st.subheader("📝 Posts by Username")

    user_posts = (
        sentiment_data["username"]
        .value_counts()
        .reset_index()
    )

    user_posts.columns = ["username", "post_count"]

    user_chart = px.bar(
        user_posts,
        x="username",
        y="post_count",
        title="Number of Posts by Each User",
        labels={
            "username": "Username",
            "post_count": "Number of Posts"
        }
    )

    st.plotly_chart(
        user_chart,
        use_container_width=True,
        key="posts_by_username_chart"
    )

    # Sentiment Overview
    st.subheader("😊 Sentiment Overview")

    sentiment_counts = sentiment_data["sentiment"].value_counts()

    sentiment_chart = px.pie(
        names=sentiment_counts.index,
        values=sentiment_counts.values,
        title="Sentiment Distribution",
        hole=0.4
    )

    st.plotly_chart(
        sentiment_chart,
        use_container_width=True,
        key="overview_sentiment_chart"
    )

    # Top Influencers
    st.subheader("🌟 Top Influencers")

    overview_influencer_chart = px.bar(
        influencer_data.head(5),
        x="username",
        y="engagement_score",
        title="Top Influencers by Engagement"
    )

    st.plotly_chart(
        overview_influencer_chart,
        use_container_width=True,
        key="overview_influencer_chart"
    )

    # Recent Posts
    st.subheader("📋 Recent Social Media Posts")

    st.dataframe(
        sentiment_data[
            ["post_id", "username", "post_text", "sentiment"]
        ],
        use_container_width=True
    )

# --------------------------------
# 7. SENTIMENT ANALYSIS PAGE
# --------------------------------

elif page == "Sentiment Analysis":

    st.header("😊 Sentiment Analysis")

    sentiment_counts = sentiment_data["sentiment"].value_counts()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Positive Posts",
            int(sentiment_counts.get("Positive", 0))
        )

    with col2:
        st.metric(
            "Negative Posts",
            int(sentiment_counts.get("Negative", 0))
        )

    with col3:
        st.metric(
            "Neutral Posts",
            int(sentiment_counts.get("Neutral", 0))
        )

    st.subheader("📊 Sentiment Distribution")

    sentiment_chart = px.pie(
        names=sentiment_counts.index,
        values=sentiment_counts.values,
        title="Social Media Sentiment Distribution",
        hole=0.4
    )

    st.plotly_chart(
        sentiment_chart,
        use_container_width=True,
        key="sentiment_page_chart"
    )

    st.subheader("Sentiment Results")

    st.download_button(
        label="📥 Download Sentiment Report",
        data=sentiment_data.to_csv(index=False).encode("utf-8"),
        file_name="sentiment_report.csv",
        mime="text/csv",
        key="sentiment_download"
    )

    # Search and Date Filter
    st.subheader("🔍 Search and Filter Posts")

    start_date = st.date_input(
        "📅 Filter posts from",
        value=None
    )

    search_text = st.text_input(
        "Search by username or post content"
    )

    filtered_data = sentiment_data.copy()

    filtered_data["date"] = pd.to_datetime(
        filtered_data["date"],
        errors="coerce"
    )

    if search_text:
        filtered_data = filtered_data[
            filtered_data["username"].astype(str).str.contains(
                search_text,
                case=False,
                na=False
            )
            |
            filtered_data["post_text"].astype(str).str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    if start_date is not None:
        filtered_data = filtered_data[
            filtered_data["date"].dt.date >= start_date
        ]

    st.write(f"Matching posts: {len(filtered_data)}")

    st.dataframe(
        filtered_data,
        use_container_width=True
    )

# --------------------------------
# 8. TRENDING TOPICS PAGE
# --------------------------------

elif page == "Trending Topics":

    st.header("🔥 Trending Topics")

    st.write(
        "Explore frequently mentioned words in social media posts."
    )

    topic_chart = px.bar(
        topic_data.head(10),
        x="topic",
        y="frequency",
        title="Most Discussed Topics",
        labels={
            "topic": "Topics",
            "frequency": "Number of Mentions"
        }
    )

    st.plotly_chart(
        topic_chart,
        use_container_width=True,
        key="trending_topics_chart"
    )

    st.subheader("Topic Results")

    st.dataframe(
        topic_data,
        use_container_width=True
    )

# --------------------------------
# 9. MISINFORMATION SCREENING PAGE
# --------------------------------

elif page == "Misinformation Screening":

    st.header("⚠️ Misinformation Screening")

    flagged_count = (
        misinformation_data["misinformation_status"]
        == "Flagged for Review"
    ).sum()

    review_count = (
        misinformation_data["misinformation_status"]
        == "No Keyword Flag Found"
    ).sum()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Flagged for Review",
            int(flagged_count)
        )

    with col2:
        st.metric(
            "No Keyword Flag Found",
            int(review_count)
        )

    st.subheader("Screening Results")

    st.dataframe(
        misinformation_data,
        use_container_width=True
    )

    st.warning(
        "Important: This is a basic keyword-based screening system. "
        "A flagged post is not necessarily misinformation, and "
        "an unflagged post is not necessarily true."
    )

# --------------------------------
# 10. INFLUENCER ANALYSIS PAGE
# --------------------------------

elif page == "Influencer Analysis":

    st.header("🌟 Influencer Analysis")

    st.write(
        "Analyze users based on likes, comments, and shares."
    )

    influencer_chart = px.bar(
        influencer_data.head(10),
        x="username",
        y="engagement_score",
        title="Top Influencers by Engagement",
        labels={
            "username": "Username",
            "engagement_score": "Engagement Score"
        }
    )

    st.plotly_chart(
        influencer_chart,
        use_container_width=True,
        key="influencer_analysis_chart"
    )

    st.subheader("📊 Engagement Comparison")

    engagement_chart = px.bar(
        influencer_data,
        x="username",
        y="engagement_score",
        title="User Engagement Comparison",
        labels={
            "username": "Username",
            "engagement_score": "Total Engagement"
        }
    )

    st.plotly_chart(
        engagement_chart,
        use_container_width=True,
        key="engagement_comparison_chart"
    )

    st.subheader("Influencer Ranking Table")

    st.dataframe(
        influencer_data,
        use_container_width=True
    )

    st.info(
        "Influencer ranking is based on engagement scores "
        "in the available dataset."
    )

# --------------------------------
# 11. FOOTER
# --------------------------------

st.markdown("---")

st.caption(
    "Social Media Intelligence Platform | "
    "Data Science Project | 2026"
)

# --------------------------------
# 12. CUSTOM CSS
# --------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F4F7FB;
    }

    [data-testid="stSidebar"] {
        background-color: #E8EEF8;
    }

    h1 {
        color: #173B65;
    }

    h2, h3 {
        color: #24527A;
    }
    </style>
    """,
    unsafe_allow_html=True
)

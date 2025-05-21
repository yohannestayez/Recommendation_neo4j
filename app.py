import streamlit as st
import pandas as pd
import sys
sys.path.append('.')
from Recommenders.content_based import ContentBasedFiltering
from Recommenders.collaborative import CollaborativeFiltering
from Recommenders.Hybrid import Recommender

# Streamlit app configuration
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Title and description
st.title("🎬 Movie Recommendation System")
st.markdown("""
    Enter a user ID and select a recommendation type to get personalized movie recommendations.
    Choose between Content-Based, Collaborative, or Hybrid filtering.
""")

# Initialize recommenders
content_recommender = ContentBasedFiltering()
collab_recommender = CollaborativeFiltering()
hybrid_recommender = Recommender()

# Input section
col1, col2 = st.columns([2, 3])
with col1:
    user_id = st.text_input("Enter User ID", value="", help="Enter a valid user ID (e.g., 21)")
with col2:
    rec_type = st.selectbox(
        "Select Recommendation Type",
        ["Hybrid", "Content-Based", "Collaborative"],
        help="Choose the type of recommendation algorithm"
    )

# Button to trigger recommendations
if st.button("Get Recommendations"):
    try:
        # Select the appropriate recommender
        if rec_type == "Content-Based":
            recommendations = content_recommender.recommend_movies(user_id)
        elif rec_type == "Collaborative":
            recommendations = collab_recommender.recommend_movies(user_id)
        else:  # Hybrid
            recommendations = hybrid_recommender.recommend_movies(user_id)

        # Handle results
        if isinstance(recommendations, str):
            st.error(recommendations)
        else:
            # Convert recommendations to DataFrame
            df = pd.DataFrame(
                recommendations,
                columns=["Title", "Genres", "Avg Rating", "Votes", "Popularity", "Year", "Relevance Score"]
            )
            # Format Genres as comma-separated string
            df["Genres"] = df["Genres"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
            # Format numerical columns
            df["Avg Rating"] = df["Avg Rating"].map("{:.1f}".format)
            df["Popularity"] = df["Popularity"].map("{:.1f}".format)
            df["Relevance Score"] = df["Relevance Score"].map("{:.2f}".format)
            df["Year"] = df["Year"].fillna("N/A")
            # Display table
            st.subheader(f"{rec_type} Recommendations")
            st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")

# Cleanup
st.markdown("---")
st.write("Click the button below to close the database connection.")
if st.button("Close Connection"):
    content_recommender.close()
    collab_recommender.close()
    hybrid_recommender.close()
    st.success("Database connection closed.")
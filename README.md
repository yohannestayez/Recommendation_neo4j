# Movie Recommendation System

This project is a movie recommendation system that leverages a Neo4j graph database. It provides a user-friendly web interface built with Streamlit.

## Features

*   **Multiple Recommendation Algorithms:** Users can choose from three different recommendation approaches:
    *   **Content-Based Filtering:** Recommends movies based on the similarity of their genres to movies the user has liked.
    *   **Collaborative Filtering:** Recommends movies based on what users with similar tastes have liked.
    *   **Hybrid Approach:** Combines the strengths of both content-based and collaborative filtering to provide more robust and personalized recommendations. The hybrid model currently weights collaborative filtering results higher.
*   **Neo4j Backend:** Utilizes a Neo4j graph database to store movie, user, and rating data, enabling efficient querying for recommendation generation.
*   **Streamlit Web Interface:** Offers an interactive UI where users can input their User ID and select a recommendation type to receive a list of suggested movies. The results display movie details like title, genres, average rating, vote count, popularity, release year, and a relevance score.
*   **Database Connection Management:** Includes functionality to connect to and close the Neo4j database connection.
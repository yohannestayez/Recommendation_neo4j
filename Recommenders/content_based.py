import sys
sys.path.append('.')
from utils.db_connector import DB_CONNECTOR

class ContentBasedFiltering:
    def __init__(self):
        self.driver = DB_CONNECTOR

    def close(self):
        self.driver.close()

    def recommend_movies(self, user_id):
        query = """
        MATCH (u:User {id: $userId})-[r:RATED]->(m:Movie)
        WHERE r.rating >= 4.0
        WITH u, COLLECT(DISTINCT m.genres) AS allGenres
        WITH u, apoc.coll.flatten(allGenres) AS userGenres
        WITH u, userGenres, 
             [g IN userGenres | [g, SIZE([x IN userGenres WHERE x = g])]] AS genreCounts
        WITH u, apoc.map.fromPairs(genreCounts) AS genreWeights
        MATCH (k:Movie)
        WHERE NOT (u)-[:RATED]->(k) 
        AND k.vote_count >= 50
        WITH k, genreWeights, 
             SIZE([g IN k.genres WHERE g IN KEYS(genreWeights)]) AS matchingGenres,
             REDUCE(score = 0.0, g IN k.genres | score + COALESCE(genreWeights[g], 0)) AS genreScore
        WHERE matchingGenres > 0
        RETURN k.title AS Title, k.genres AS Genres, k.vote_average AS VoteAverage, 
               k.vote_count AS VoteCount, k.popularity AS Popularity, 
               k.release_year AS ReleaseYear, genreScore AS RelevanceScore
        ORDER BY genreScore DESC, k.vote_average DESC, k.popularity DESC, k.release_year DESC
        LIMIT 10;
        """
        try:
            result = self.driver.query(query, userId=user_id)
            recommendations = [
                (
                    record["Title"],
                    record["Genres"],
                    record["VoteAverage"],
                    record["VoteCount"],
                    record["Popularity"],
                    record["ReleaseYear"],
                    record["RelevanceScore"]
                ) for record in result
            ]
            if not recommendations:
                return "No recommendations found for this user."
            return recommendations
        except Exception as e:
            return f"Error fetching recommendations: {str(e)}"

if __name__ == "__main__":
    cbf = ContentBasedFiltering()
    try:
        user_id = str(input("Enter the user id: ").strip())  # Ensure user_id is a string
        recommendations = cbf.recommend_movies(user_id)
        if isinstance(recommendations, str):
            print(recommendations)
        else:
            print("Content-Based Recommendations:")
            for title, genres, vote_avg, vote_cnt, popularity, year, score in recommendations:
                print(
                    f"Movie: {title}, Genres: {', '.join(genres)}, "
                    f"Avg Rating: {vote_avg:.1f}, Votes: {vote_cnt}, "
                    f"Popularity: {popularity:.1f}, Year: {year or 'N/A'}, "
                    f"Relevance Score: {score:.1f}"
                )
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        cbf.close()
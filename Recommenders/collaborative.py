import sys
sys.path.append('.')
from utils.db_connector import DB_CONNECTOR

class CollaborativeFiltering:
    def __init__(self):
        self.driver = DB_CONNECTOR

    def close(self):
        self.driver.close()

    def recommend_movies(self, user_id):
        query = """
        MATCH (u1:User {id: $userId})-[x:RATED]->(m:Movie)
        WHERE x.rating >= 3.5
        MATCH (u2:User)-[y:RATED]->(m)
        WHERE u1 <> u2 AND y.rating >= 3.5
        WITH u1, m, COLLECT(DISTINCT u2) AS similarUsers
        UNWIND similarUsers AS u2
        MATCH (u2)-[z:RATED]->(rec:Movie)
        WHERE NOT (u1)-[:RATED]->(rec) AND z.rating >= 3.5
        WITH rec, COUNT(DISTINCT u2) AS similarUserCount
        WHERE similarUserCount >= 2 AND rec.vote_count >= 50
        RETURN rec.title AS Title, rec.genres AS Genres, rec.vote_average AS VoteAverage,
               rec.vote_count AS VoteCount, rec.popularity AS Popularity,
               rec.release_year AS ReleaseYear, similarUserCount AS RelevanceScore
        ORDER BY similarUserCount DESC, rec.vote_average DESC, rec.popularity DESC, rec.release_year DESC
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
    cf = CollaborativeFiltering()
    try:
        user_id = str(input("Enter the user id: ").strip())  # Ensure user_id is a string
        recommendations = cf.recommend_movies(user_id)
        if isinstance(recommendations, str):
            print(recommendations)
        else:
            print("Collaborative Filtering Recommendations:")
            for title, genres, vote_avg, vote_cnt, popularity, year, score in recommendations:
                print(
                    f"Movie: {title}, Genres: {', '.join(genres)}, "
                    f"Avg Rating: {vote_avg:.1f}, Votes: {vote_cnt}, "
                    f"Popularity: {popularity:.1f}, Year: {year or 'N/A'}, "
                    f"Relevance Score: {score}"
                )
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        cf.close()
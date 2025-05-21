import sys
sys.path.append('.')
from Recommenders.content_based import ContentBasedFiltering
from Recommenders.collaborative import CollaborativeFiltering

class Recommender:
    def __init__(self):
        self.content_based = ContentBasedFiltering()
        self.collaborative = CollaborativeFiltering()

    def close(self):
        self.content_based.close()
        self.collaborative.close()

    def recommend_movies(self, user_id):
        try:
            # Get recommendations from both recommenders
            content_results = self.content_based.recommend_movies(user_id)
            collab_results = self.collaborative.recommend_movies(user_id)

            # Handle cases where one or both return errors or no results
            if isinstance(content_results, str) and isinstance(collab_results, str):
                return "No recommendations found from either content-based or collaborative filtering."
            elif isinstance(content_results, str):
                if isinstance(collab_results, list):
                    return collab_results  # Return collaborative results if content-based fails
                return content_results
            elif isinstance(collab_results, str):
                if isinstance(content_results, list):
                    return content_results  # Return content-based results if collaborative fails
                return collab_results

            # Normalize scores within each result set
            recommendations = {}

            # Normalize content-based scores
            if content_results:
                content_scores = [res[6] for res in content_results]
                content_max = max(content_scores, default=1.0)
                content_min = min(content_scores, default=0.0)
                content_range = content_max - content_min if content_max != content_min else 1.0

                for title, genres, vote_avg, vote_cnt, popularity, year, score in content_results:
                    # Normalize content score to [0, 1]
                    normalized_score = (score - content_min) / content_range if content_range != 0 else 0.5
                    recommendations[title] = {
                        'genres': genres,
                        'vote_average': vote_avg,
                        'vote_count': vote_cnt,
                        'popularity': popularity,
                        'release_year': year,
                        'content_score': normalized_score,
                        'collab_score': 0.0,
                        'combined_score': normalized_score  # Initial score
                    }

            # Normalize collaborative scores
            if collab_results:
                collab_scores = [res[6] for res in collab_results]
                collab_max = max(collab_scores, default=1.0)
                collab_min = min(collab_scores, default=0.0)
                collab_range = collab_max - collab_min if collab_max != collab_min else 1.0

                for title, genres, vote_avg, vote_cnt, popularity, year, score in collab_results:
                    # Normalize collab score to [0, 1]
                    normalized_score = (score - collab_min) / collab_range if collab_range != 0 else 0.5
                    if title in recommendations:
                        # Movie in both lists: combine normalized scores (e.g., average)
                        recommendations[title]['collab_score'] = normalized_score
                        recommendations[title]['combined_score'] = (
                            0.25 * recommendations[title]['content_score'] + 0.75* normalized_score
                        )
                    else:
                        # Movie only in collaborative results
                        recommendations[title] = {
                            'genres': genres,
                            'vote_average': vote_avg,
                            'vote_count': vote_cnt,
                            'popularity': popularity,
                            'release_year': year,
                            'content_score': 0.0,
                            'collab_score': normalized_score,
                            'combined_score': normalized_score
                        }

            # Convert to list of tuples for output
            combined_recommendations = [
                (
                    title,
                    data['genres'],
                    data['vote_average'],
                    data['vote_count'],
                    data['popularity'],
                    data['release_year'],
                    data['combined_score']
                )
                for title, data in recommendations.items()
            ]

            # Sort by combined score, vote_average, popularity, release_year
            combined_recommendations.sort(
                key=lambda x: (x[6], x[2], x[4], x[5] if x[5] is not None else 0),
                reverse=True
            )

            # Limit to 10 recommendations
            combined_recommendations = combined_recommendations[:10]

            if not combined_recommendations:
                return "No recommendations found after combining results."
            return combined_recommendations

        except Exception as e:
            return f"Error fetching recommendations: {str(e)}"

if __name__ == "__main__":
    recommender = Recommender()
    try:
        user_id = str(input("Enter the user id: ").strip())  # Ensure user_id is a string
        recommendations = recommender.recommend_movies(user_id)
        if isinstance(recommendations, str):
            print(recommendations)
        else:
            print("Hybrid Recommendations:")
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
        recommender.close()
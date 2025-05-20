import sys
sys.path.append('.')

from db_connector import DB_CONNECTOR

def load_movies(connector):
    """
    Load movies into Neo4j as Movie nodes.
    """ 
    query = """
    LOAD CSV WITH HEADERS FROM 'file:///movies_cleaned.csv' AS row
    MERGE (m:Movie {id: row.id})
    SET m.title = row.title,
        m.genres = split(row.genres, ','), 
        m.release_year = toInteger(row.release_year),
        m.popularity = toFloat(row.popularity),
        m.vote_average = toFloat(row.vote_average),
        m.vote_count = toInteger(row.vote_count);
    """
    connector.query(query)
    print("Movies data loaded into Neo4j.")

def load_users_and_ratings(connector):
    """
    Load users and RATED relationships into Neo4j.
    """
    query = """
    LOAD CSV WITH HEADERS FROM 'file:///ratings_cleaned.csv' AS row
    MERGE (u:User {id: row.userId})
    WITH u, row
    MATCH (m:Movie {id: row.movieId})
    CREATE (u)-[:RATED {rating: toFloat(row.rating)}]->(m);
    """
    connector.query(query)
    print("Ratings data and user nodes loaded into Neo4j.")

def main():
    try:
        load_movies(DB_CONNECTOR)
        load_users_and_ratings(DB_CONNECTOR)
    finally:
        DB_CONNECTOR.close()
        print("Connection to Neo4j closed.")

if __name__ == "__main__":
    main()
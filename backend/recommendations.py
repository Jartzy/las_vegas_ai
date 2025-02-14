import psycopg2
from database import get_db_connection

def get_personalized_recommendations(user_id):
    """Fetches AI-driven recommendations based on user preferences."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch user's most clicked categories
    query = """
        SELECT r.id, r.name, r.category, COUNT(ui.id) as interactions
        FROM recommendations r
        LEFT JOIN user_interactions ui ON r.id = ui.recommendation_id
        WHERE ui.user_id = %s
        GROUP BY r.id, r.name, r.category
        ORDER BY interactions DESC, r.rating DESC
        LIMIT 10;
    """
    cur.execute(query, (user_id,))
    recommendations = cur.fetchall()

    cur.close()
    conn.close()

    return recommendations

# Example usage:
# get_personalized_recommendations("user123")
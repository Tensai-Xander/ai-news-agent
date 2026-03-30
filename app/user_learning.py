import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def get_user_preferences():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # score par interest
    cur.execute("""
        SELECT interest,
               SUM(CASE WHEN action='like' THEN 1 ELSE -1 END) as score
        FROM feedback
        GROUP BY interest
    """)

    interest_scores = {row[0]: row[1] for row in cur.fetchall()}

    # score features
    cur.execute("""
        SELECT
            SUM(CASE WHEN has_code AND action='like' THEN 1 ELSE 0 END) -
            SUM(CASE WHEN has_code AND action='dislike' THEN 1 ELSE 0 END),
            SUM(CASE WHEN is_deep_dive AND action='like' THEN 1 ELSE 0 END) -
            SUM(CASE WHEN is_deep_dive AND action='dislike' THEN 1 ELSE 0 END),
            SUM(CASE WHEN is_tutorial AND action='like' THEN 1 ELSE 0 END) -
            SUM(CASE WHEN is_tutorial AND action='dislike' THEN 1 ELSE 0 END)
        FROM feedback
    """)

    row = cur.fetchone()

    conn.close()

    return {
        "interest_scores": interest_scores,
        "feature_scores": {
            "has_code": row[0] or 0,
            "is_deep_dive": row[1] or 0,
            "is_tutorial": row[2] or 0,
        }
    }
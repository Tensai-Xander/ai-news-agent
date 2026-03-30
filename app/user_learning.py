import psycopg2
import os
from app.config import DECAY_DAYS

DATABASE_URL = os.getenv("DATABASE_URL")

def get_user_preferences():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    DAY_IN_SEC = 86400

    # score par interest
    cur.execute(f"""
        SELECT interest,
            SUM(
                CASE 
                    WHEN action='like' THEN 1 
                    ELSE -1 
                END * EXP(-EXTRACT(EPOCH FROM (NOW() - created_at)) / {DAY_IN_SEC} / {DECAY_DAYS})
            ) as score
        FROM feedback
        GROUP BY interest
    """)

    interest_scores = {row[0]: row[1] for row in cur.fetchall()}

    # score features
    cur.execute(f"""
    SELECT
        SUM(
            (CASE WHEN has_code AND action='like' THEN 1 ELSE 0 END -
             CASE WHEN has_code AND action='dislike' THEN 1 ELSE 0 END)
            * EXP(-EXTRACT(EPOCH FROM (NOW() - created_at)) / {DAY_IN_SEC} / {DECAY_DAYS})
        ),
        SUM(
            (CASE WHEN is_deep_dive AND action='like' THEN 1 ELSE 0 END -
             CASE WHEN is_deep_dive AND action='dislike' THEN 1 ELSE 0 END)
            * EXP(-EXTRACT(EPOCH FROM (NOW() - created_at)) / {DAY_IN_SEC} / {DECAY_DAYS})
        ),
        SUM(
            (CASE WHEN is_tutorial AND action='like' THEN 1 ELSE 0 END -
             CASE WHEN is_tutorial AND action='dislike' THEN 1 ELSE 0 END)
            * EXP(-EXTRACT(EPOCH FROM (NOW() - created_at)) / {DAY_IN_SEC} / {DECAY_DAYS})
        )
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
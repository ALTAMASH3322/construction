# In routes/reviews.py

import pymysql.cursors
import logging
from flask import Blueprint, request, jsonify
from app import getConnection

review_bp = Blueprint('reviews', __name__)


# --- ENDPOINT 1: Submit a new review ---

@review_bp.route("/submit_review", methods=["POST"])
def submit_review():
    """
    Submits a new review and automatically updates the average rating of the target.
    Prevents a user from submitting a duplicate review for the same target.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        reviewer_user_id = data.get("reviewer_user_id")
        target_type = data.get("review_target_type")
        target_id = data.get("review_target_id")
        rating = data.get("rating")
        comment = data.get("comment")

        # ... (Your existing validation for required fields and rating range is still here and correct) ...
        if not all([reviewer_user_id, target_type, target_id, rating]):
            return jsonify(error="... are required"), 400
        if target_type not in ['user', 'agent', 'property']:
            return jsonify(error="Invalid review_target_type..."), 400
        try:
            rating = int(rating)
            if not 1 <= rating <= 5: raise ValueError
        except (ValueError, TypeError):
            return jsonify(error="Rating must be an integer between 1 and 5."), 400

        con = getConnection()
        cursor = con.cursor()

        # 1. Try to insert the new review
        try:
            query_insert = "INSERT INTO reviews (reviewer_user_id, review_target_type, review_target_id, rating, comment) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query_insert, (reviewer_user_id, target_type, target_id, rating, comment))
        
        # --- THIS IS THE NEW LOGIC ---
        except pymysql.err.IntegrityError as e:
            # Check if the error is specifically a 'Duplicate entry' error
            if 'Duplicate entry' in str(e):
                logging.warning(f"User {reviewer_user_id} attempted to submit a duplicate review for {target_type} ID {target_id}.")
                return jsonify(error="You have already submitted a review for this item."), 409 # 409 Conflict
            else:
                # If it's a different integrity error (e.g., foreign key), re-raise it
                raise e
        # --------------------------------

        # 2. If insert was successful, recalculate and update the average rating
        avg_query = """
            UPDATE {table_name}
            SET 
                review_count = (SELECT COUNT(*) FROM reviews WHERE review_target_type = %s AND review_target_id = %s),
                average_rating = (SELECT AVG(rating) FROM reviews WHERE review_target_type = %s AND review_target_id = %s)
            WHERE {id_column} = %s;
        """
        
        if target_type == 'user':
            table_name, id_column = 'users', 'user_id'
        elif target_type == 'agent':
            table_name, id_column = 'agents', 'agent_id'
        elif target_type == 'property':
            table_name, id_column = 'properties', 'property_id'
        else: # Should not happen due to validation above
            raise ValueError("Invalid target type for update.")
        
        formatted_query = avg_query.format(table_name=table_name, id_column=id_column)
        cursor.execute(formatted_query, (target_type, target_id, target_type, target_id, target_id))

        con.commit()
        
        return jsonify(message="Review submitted successfully."), 201

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /submit_review: {e}", exc_info=True)
        return jsonify(error="please check all the details before Submitting"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


# --- ENDPOINT 2: Get all reviews for a target ---

@review_bp.route("/get_reviews", methods=["POST"])
def get_reviews():
    """
    Fetches all reviews for a specific target (user, agent, or property).
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        target_type = data.get("review_target_type")
        target_id = data.get("review_target_id")

        print(data)

        if not all([target_type, target_id]):
            return jsonify(error="review_target_type and review_target_id are required"), 400
            
        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        
        # Join with the users table to get the reviewer's name
        query = """
            SELECT 
                r.rating,
                r.comment,
                DATE_FORMAT(r.created_at, '%%Y-%%m-%%d') AS review_date,
                u.name AS reviewer_name
            FROM reviews r
            JOIN users u ON r.reviewer_user_id = u.user_id
            WHERE r.review_target_type = %s AND r.review_target_id = %s
            ORDER BY r.created_at DESC;
        """
        
        cursor.execute(query, (target_type, target_id))
        reviews = cursor.fetchall()
        print(reviews)
        
        return jsonify(reviews=reviews), 200

    except Exception as e:
        logging.error(f"Error in /get_reviews: {e}", exc_info=True)
        return jsonify(error="please check all the details before Submitting"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()
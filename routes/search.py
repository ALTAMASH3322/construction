import pymysql.cursors
import logging
import json
from flask import Blueprint, request, jsonify
from app import getConnection

search_bp = Blueprint('search', __name__)


# --- ENDPOINT 1: Save a New Search ---

@search_bp.route("/save_search", methods=["POST"])
def save_search():
    """
    Saves a set of search filters for a user with a given name.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        search_name = data.get("search_name")
        search_params = data.get("search_params")

        print(data)

        if not all([user_id, search_name, search_params]):
            return jsonify(error="user_id, search_name, and search_params are required"), 400

        if not isinstance(search_params, dict):
            return jsonify(error="search_params must be a valid JSON object"), 400

        con = getConnection()
        cursor = con.cursor()

        # Convert the Python dictionary to a JSON string for the database
        params_as_string = json.dumps(search_params)

        query = "INSERT INTO saved_searches (user_id, search_name, search_params) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, search_name, params_as_string))
        search_id = cursor.lastrowid
        
        con.commit()

        return jsonify(message="Search saved successfully.", search_id=search_id), 201

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /save_search: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


# --- ENDPOINT 2: Get All of a User's Saved Searches ---

@search_bp.route("/my_saved_searches", methods=["POST"])
def get_saved_searches():
    """
    Fetches all saved searches for a specific user.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify(error="user_id is required"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        query = "SELECT search_id, search_name, search_params, created_at FROM saved_searches WHERE user_id = %s ORDER BY created_at DESC"
        cursor.execute(query, (user_id,))
        searches = cursor.fetchall()
        
        # The database returns search_params as a string, so we convert it back to an object
        for search in searches:
            if search['search_params']:
                search['search_params'] = json.loads(search['search_params'])

        return jsonify(saved_searches=searches), 200

    except Exception as e:
        logging.error(f"Error in /my_saved_searches: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


# --- ENDPOINT 3: Delete a Saved Search ---

@search_bp.route("/delete_saved_search", methods=["POST"])
def delete_saved_search():
    """
    Deletes a specific saved search belonging to a user.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        search_id = data.get("search_id")

        print(data)
        if not all([user_id, search_id]):
            return jsonify(error="user_id and search_id are required"), 400

        con = getConnection()
        cursor = con.cursor()


        # The WHERE clause includes user_id for security, ensuring a user can only delete their own searches.
        query = "DELETE FROM saved_searches WHERE search_id = %s AND user_id = %s"
        cursor.execute(query, (search_id, user_id))

        if cursor.rowcount > 0:
            con.commit()
            return jsonify(message="Saved search deleted successfully."), 200
        else:
            return jsonify(error="Saved search not found or you do not have permission to delete it."), 404

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /delete_saved_search: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()
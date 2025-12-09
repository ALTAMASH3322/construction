from flask import Blueprint, request, jsonify
from app import getConnection
import pymysql.cursors  # <--- FIX 1: Add this import for the dictionary cursor
import logging

from datetime import datetime

# It's good practice to have your Blueprint and logging setup
buyer_bp = Blueprint('buyer', __name__)
logging.basicConfig(level=logging.INFO)

@buyer_bp.route("/buyer_dashboard", methods=["POST"])
def dashboard():
    """
    Provides dashboard statistics for a specific buyer (user).
    Expects a JSON body with a "user_id".
    """
    con = None
    cursor = None

    try:
        # 1. Get and validate the user_id from the request body
        data = request.get_json()
        if not data or "user_id" not in data:
            return jsonify(error="user_id is required in the JSON body"), 400

        try:
            userId = data.get("user_id")
        except (ValueError, TypeError):
            return jsonify(error="user_id must be a valid integer"), 400

        logging.info(f"Received buyer dashboard request for user_id: {userId}")

        # 2. Connect to the database and prepare the query
        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        query = """
            SELECT
                (SELECT COUNT(*) FROM appointments WHERE user_id = %s) AS total_appointments,
                (SELECT COUNT(*) FROM favorites WHERE user_id = %s) AS favorite_properties,
                (SELECT COUNT(*) FROM conversations WHERE user_id = %s) AS active_chats,
                (SELECT COUNT(*) FROM appointments WHERE user_id = %s AND appointment_date >= CURDATE()) AS upcoming_visits;
        """

        # 3. Execute the query, passing the userId for each placeholder
        cursor.execute(query, (userId, userId, userId, userId))
        
        # This query always returns exactly one row, so use fetchone()
        result = cursor.fetchone()
        
        logging.info(f"Query result for user_id {userId}: {result}")

        # 4. Return the successful JSON response
        return jsonify(message="Buyer dashboard data retrieved successfully", dashboard=result), 200

    except Exception as e:
        logging.error(f"An error occurred in /buyer_dashboard: {e}", exc_info=True)
        return jsonify(error="please check all the details before Submitting"), 500

    finally:
        # 5. Ensure the connection is always closed
        if cursor:
            cursor.close()
        if con:
            con.close()
            logging.info("Database connection closed.")







@buyer_bp.route("/request_appointment", methods=["POST"])
def request_appointment():
    """
    Allows a user to request an appointment for a property on a specific date.
    - NEW: Checks if the user already has an active appointment for this property.
    - Checks the agent's daily booking limit before creating a 'pending' record.
    """
    con = None
    cursor = None
    
    try:
        # 1. Get and validate input from the user
        data = request.get_json()
        user_id = data.get("user_id")
        property_id = data.get("property_id")
        appointment_date = data.get("appointment_date")
        user_notes = data.get("user_notes")

        print(data)

        if not all([user_id, property_id, appointment_date]):
            return jsonify(error="user_id, property_id, and appointment_date are required"), 400

        # ... (date format validation remains the same) ...
        try:
            datetime.strptime(appointment_date, '%Y-%m-%d')
        except ValueError:
            return jsonify(error="Invalid date format. Please use YYYY-MM-DD."), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # 2. (*** NEW STEP ***) Check for existing active appointments for this user/property
        query_duplicate_check = """
            SELECT COUNT(*) AS active_count 
            FROM appointments 
            WHERE user_id = %s 
              AND property_id = %s 
              AND status IN ('pending', 'confirmed');
        """
        cursor.execute(query_duplicate_check, (user_id, property_id))
        active_appointments = cursor.fetchone()

        if active_appointments and active_appointments['active_count'] > 0:
            logging.warning(f"User {user_id} tried to book a duplicate appointment for property {property_id}.")
            return jsonify(error="You already have an active (pending or confirmed) appointment for this property."), 409 # 409 Conflict

        # 3. Get agent details and count their confirmed appointments for that day (existing logic)
        query_check_limit = """
            SELECT 
                p.agent_id, 
                ag.daily_booking_limit,
                (SELECT COUNT(*) FROM appointments 
                 WHERE agent_id = p.agent_id 
                   AND appointment_date = %s 
                   AND status = 'confirmed') AS confirmed_today
            FROM properties p
            JOIN agents ag ON p.agent_id = ag.agent_id
            WHERE p.property_id = %s;
        """
        cursor.execute(query_check_limit, (appointment_date, property_id))
        agent_info = cursor.fetchone()

        if not agent_info:
            return jsonify(error="Property or associated agent not found"), 404

        # 4. Enforce the agent's daily booking limit (existing logic)
        if agent_info['confirmed_today'] >= agent_info['daily_booking_limit']:
            logging.warning(f"Booking rejected for agent {agent_info['agent_id']} on {appointment_date}. Limit reached.")
            return jsonify(error="This agent is fully booked for the selected date. Please choose another day."), 409

        # 5. If all checks pass, create the PENDING appointment (existing logic)
        agent_id = agent_info['agent_id']
        query_insert = """
            INSERT INTO appointments 
                (user_id, property_id, agent_id, appointment_date, status, user_notes, appointment_time)
            VALUES (%s, %s, %s, %s, 'pending', %s, NULL);
        """
        cursor.execute(query_insert, (user_id, property_id, agent_id, appointment_date, user_notes))
        
        appointment_id = cursor.lastrowid
        con.commit()

        logging.info(f"Pending appointment created with ID {appointment_id} for agent {agent_id}")
        return jsonify(message="Appointment requested successfully. Awaiting agent confirmation.", appointment_id=appointment_id), 201

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /request_appointment: {e}", exc_info=True)
        return jsonify(error="please check all the details before Submitting"), 500

    finally:
        if cursor: cursor.close()
        if con: con.close()




@buyer_bp.route("/my_appointments", methods=["POST"])
def get_my_appointments():
    """
    Fetches a list of all appointments for a specific user,
    including property and agent details.
    """
    con = None
    cursor = None

    try:
        # 1. Get and validate the user_id
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify(error="user_id is required"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # 2. Query to join appointments with properties, agents, and users (for agent's name)
        query = """
            SELECT
                a.appointment_id,
                DATE_FORMAT(a.appointment_date, '%%Y-%%m-%%d') AS appointment_date,
                TIME_FORMAT(a.appointment_time, '%%H:%%i') AS appointment_time,
                a.status,
                a.user_notes,
                a.agent_notes,
                p.property_id,
                p.title AS property_title,
                p.address AS property_address,
                u.name AS agent_name
            FROM
                appointments a
            LEFT JOIN
                properties p ON a.property_id = p.property_id
            LEFT JOIN
                agents ag ON a.agent_id = ag.agent_id
            LEFT JOIN
                users u ON ag.user_id = u.user_id
            WHERE
                a.user_id = %s
            ORDER BY
                a.appointment_date DESC, a.appointment_time ASC;
        """
        
        cursor.execute(query, (user_id,))
        appointments = cursor.fetchall()
        print(appointments)
        
        return jsonify(appointments=appointments), 200

    except Exception as e:
        logging.error(f"Error in /my_appointments: {e}", exc_info=True)
        return jsonify(error="please check all the details before Submitting"), 500

    finally:
        if cursor: cursor.close()
        if con: con.close()



# Place this in your buyer's blueprint file as well

@buyer_bp.route("/cancel_appointment", methods=["POST"])
def cancel_appointment():
    """
    Allows a user to cancel one of their own appointments,
    but only if the appointment's status is 'pending'.
    """
    con = None
    cursor = None

    try:
        # 1. Get and validate input
        data = request.get_json()
        user_id = data.get("user_id")
        appointment_id = data.get("appointment_id")
        print(data)
        

        if not all([user_id, appointment_id]):
            return jsonify(error="user_id and appointment_id are required"), 400

        con = getConnection()
        cursor = con.cursor()

        # 2. Execute a targeted DELETE query
        # The WHERE clause is critical: it ensures a user can only delete
        # their own appointments AND only if the status is 'pending'.
        query = """
            DELETE FROM appointments 
            WHERE appointment_id = %s 
              AND user_id = %s 
              AND status = 'pending';
        """
        
        cursor.execute(query, (appointment_id, user_id))

        # 3. Check if a row was actually deleted
        if cursor.rowcount > 0:
            con.commit()
            logging.info(f"User {user_id} cancelled pending appointment {appointment_id}.")
            return jsonify(message="Appointment cancelled successfully."), 200
        else:
            # If no rows were affected, it means the appointment either
            # didn't exist, didn't belong to the user, or was no longer pending.
            logging.warning(f"Failed cancellation attempt by user {user_id} for appointment {appointment_id}.")
            return jsonify(error="Appointment could not be cancelled. It may have already been confirmed, rejected, or does not exist."), 403 # 403 Forbidden is appropriate here

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /cancel_appointment: {e}", exc_info=True)
        return jsonify(error="please check all the details before Submitting"), 500

    finally:
        if cursor: cursor.close()
        if con: con.close()






# In routes/buyer.py

@buyer_bp.route("/compare_properties", methods=["POST"])
def compare_properties():
    """
    Fetches detailed data for up to 3 properties for a side-by-side comparison.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        property_ids = data.get("property_ids")
        print (data)

        # 1. Input Validation
        if not property_ids or not isinstance(property_ids, list):
            return jsonify(error="A 'property_ids' array is required."), 400

        if not property_ids: # Check for empty list
            return jsonify(error="'property_ids' array cannot be empty."), 400

        if len(property_ids) > 3:
            return jsonify(error="You can compare a maximum of 3 properties at a time."), 400

        # Ensure all IDs are integers to prevent SQL injection
        try:
            sanitized_ids = [pid for pid in property_ids]
        except (ValueError, TypeError):
            return jsonify(error="All property IDs must be valid integers."), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # 2. Dynamically build the query
        # Create a string of placeholders like '%s, %s, %s'
        placeholders = ', '.join(['%s'] * len(sanitized_ids))

        # This query fetches all details and groups images.
        # It also uses FIELD() to maintain the order of IDs sent from the frontend.
        query = f"""
            SELECT
                p.*,
                GROUP_CONCAT(i.image_url) AS images
            FROM
                properties AS p
            LEFT JOIN
                property_images AS i ON p.property_id = i.property_id
            WHERE
                p.property_id IN ({placeholders})
                AND p.is_deleted = FALSE
            GROUP BY
                p.property_id
            ORDER BY
                FIELD(p.property_id, {placeholders});
        """
        
        # The parameters must be provided twice: once for IN() and once for FIELD()
        params = tuple(sanitized_ids + sanitized_ids)
        
        cursor.execute(query, params)
        properties = cursor.fetchall()

        # 3. Post-process the results
        for prop in properties:
            prop['images'] = prop['images'].split(',') if prop['images'] else []
            prop['is_featured'] = bool(prop['is_featured'])

        return jsonify(properties=properties), 200

    except Exception as e:
        logging.error(f"Error in /compare_properties: {e}", exc_info=True)
        return jsonify(error="please check all the details before Submitting"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()
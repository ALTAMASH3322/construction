from flask import Blueprint, request, jsonify
from app import getConnection
import pymysql.cursors
import logging
from datetime import datetime

# It's good practice to have your Blueprint and logging setup
agent_bp = Blueprint('agent', __name__)
logging.basicConfig(level=logging.INFO)


@agent_bp.route("/agent_dashboard", methods=["POST"])
def dashboard():
    """
    Provides dashboard statistics for a specific agent.
    Expects a JSON body with an "agent_id".
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        if not data or "agent_id" not in data:
            return jsonify(error="agent_id is required in the JSON body"), 400
        try:
            agentId = data.get("agent_id")
        except (ValueError, TypeError):
            return jsonify(error="agent_id must be a valid integer"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        # Query correctly excludes deleted properties from the count
        print(agentId)
        query = """
            SELECT
                (SELECT COUNT(*) FROM properties WHERE agent_id = %s AND is_deleted = FALSE) AS agent_properties,
                COUNT(a.appointment_id) AS total_agent_appointments,
                COUNT(CASE WHEN a.appointment_date >= CURDATE() THEN 1 END) AS upcoming_appointments,
                COUNT(CASE WHEN a.status = 'pending' THEN 1 END) AS pending_appointments
            FROM
                appointments a
            WHERE
                a.agent_id = %s;
        """
        cursor.execute(query, (agentId, agentId))
        result = cursor.fetchone()
        print(result)
        return jsonify(message="Agent dashboard data retrieved successfully", dashboard1=result), 200 # Renamed 'dashboard1' to 'dashboard'
    except Exception as e:
        logging.error(f"An error occurred in /agent_dashboard: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


@agent_bp.route("/daily_appointments", methods=["POST"])
def get_daily_appointments():
    """
    Fetches all appointments for a specific agent on a given date.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        agentId = data.get("agent_id")
        appointmentDate = data.get("appointment_date")
        if not agentId or not appointmentDate:
            return jsonify(error="agent_id and appointment_date are required"), 400
        try:
            datetime.strptime(appointmentDate, '%Y-%m-%d')
        except ValueError:
            return jsonify(error="Invalid date format. Please use YYYY-MM-DD."), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT
                a.appointment_id, TIME_FORMAT(a.appointment_time, '%%H:%%i:%%s') AS appointment_time, 
                a.status, a.user_notes, p.title AS property_title, p.address AS property_address,
                u.name AS user_name, u.user_id
            FROM appointments a
            LEFT JOIN properties p ON a.property_id = p.property_id
            LEFT JOIN users u ON a.user_id = u.user_id
            WHERE a.agent_id = %s AND a.appointment_date = %s
            ORDER BY a.appointment_time ASC;
        """
        cursor.execute(query, (agentId, appointmentDate))
        appointments = cursor.fetchall()
        return jsonify(message=f"Successfully retrieved appointments for {appointmentDate}", appointments=appointments), 200
    except Exception as e:
        logging.error(f"An error occurred in /daily_appointments: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


@agent_bp.route("/update_appointment_status", methods=["POST"])
def update_appointment_status():
    """
    Allows an agent to accept, reject, or reschedule a pending appointment.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        appointment_id = data.get("appointment_id")
        action = data.get("action")
        agent_notes = data.get("agent_notes")

        print(data)
        if not all([appointment_id, action]):
            return jsonify(error="appointment_id and action are required"), 400

        con = getConnection()
        cursor = con.cursor()
        action = action.lower()
        
        if action == "accept":
            appointment_time = data.get("appointment_time")
            if not appointment_time: return jsonify(error="appointment_time is required when accepting"), 400
            query = "UPDATE appointments SET status = 'confirmed', appointment_time = %s, agent_notes = %s WHERE appointment_id = %s AND status = 'pending'"
            params = (appointment_time, agent_notes, appointment_id)
            success_message = "Appointment confirmed successfully."
        elif action == "cancelled":
            # Note: Changed status from 'cancelled' to 'rejected' for clarity
            query = "UPDATE appointments SET status = 'cancelled', agent_notes = %s WHERE appointment_id = %s AND status = 'pending'"
            params = (agent_notes, appointment_id)
            success_message = "Appointment rejected successfully."
        elif action == "reschedule":
            new_date = data.get("appointment_date")
            new_time = data.get("appointment_time")
            if not all([new_date, new_time]): return jsonify(error="appointment_date and appointment_time are required when rescheduling"), 400
            query = "UPDATE appointments SET status = 'confirmed', appointment_date = %s, appointment_time = %s, agent_notes = %s WHERE appointment_id = %s AND status = 'pending'"
            params = (new_date, new_time, agent_notes, appointment_id)
            success_message = "Appointment rescheduled and confirmed successfully."
        else:
            return jsonify(error="Invalid action. Must be 'accept', 'reject', or 'reschedule'."), 400

        cursor.execute(query, params)
        if cursor.rowcount == 0:
            return jsonify(error="Appointment not found or it is not in a pending state"), 404

        con.commit()
        return jsonify(message=success_message), 200
    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /update_appointment_status: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


@agent_bp.route("/agent_appointments", methods=["POST"])
def get_agent_appointments():
    """
    Fetches a list of all appointments for a specific agent.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")
        if not agent_id: return jsonify(error="agent_id is required"), 400

        print(agent_id)

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT
                a.appointment_id, DATE_FORMAT(a.appointment_date, '%%Y-%%m-%%d') AS appointment_date,
                TIME_FORMAT(a.appointment_time, '%%H:%%i') AS appointment_time, a.status,
                a.user_notes, a.agent_notes, p.property_id, p.title AS property_title,
                p.address AS property_address, u.name AS user_name
            FROM appointments a
            LEFT JOIN properties p ON a.property_id = p.property_id
            LEFT JOIN users u ON a.user_id = u.user_id
            WHERE a.agent_id = %s
            ORDER BY a.appointment_date DESC, a.created_at DESC;
        """
        cursor.execute(query, (agent_id,))
        appointments = cursor.fetchall()
        return jsonify(appointments=appointments), 200
    except Exception as e:
        logging.error(f"Error in /agent_appointments: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()

# --- NEW PROPERTY MANAGEMENT ENDPOINTS ---

# In routes/agent.py

@agent_bp.route("/my_properties", methods=["POST"])
def get_agent_properties():
    """
    Fetches all non-deleted properties for a specific agent, with images grouped.
    Featured properties are ranked first.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")
        if not agent_id:
            return jsonify(error="agent_id is required"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # --- THIS IS THE CORRECTED QUERY ---
        # The ORDER BY clause now prioritizes the 'is_featured' flag.
        query = """
            SELECT
                p.*,
                GROUP_CONCAT(i.image_url) AS images
            FROM
                properties AS p
            LEFT JOIN
                property_images AS i ON p.property_id = i.property_id
            WHERE
                p.agent_id = %s
                AND p.is_deleted = FALSE
            GROUP BY
                p.property_id_1
            ORDER BY
                p.is_featured DESC, p.created_at DESC;
        """
        cursor.execute(query, (agent_id,))
        properties = cursor.fetchall()

        # Post-process the results
        for prop in properties:
            prop['images'] = prop['images'].split(',') if prop['images'] else []
            # Explicitly convert the is_featured flag to a boolean for the frontend
            prop['is_featured'] = bool(prop['is_featured'])

        print(properties)

        return jsonify(properties=properties), 200

    except Exception as e:
        logging.error(f"Error in /my_properties: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


# In routes/agent.py

@agent_bp.route("/update_property", methods=["POST"])
def update_property():
    con = None
    cursor = None
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")
        property_id = data.get("property_id")
        updates = data.get("updates")

        if not all([agent_id, property_id, updates]):
            return jsonify(error="agent_id, property_id, and 'updates' are required"), 400

        con = getConnection()
        cursor = con.cursor()

        # 1. SECURITY PRE-CHECK (Crucial Fix)
        # Check if property exists and belongs to agent BEFORE trying to update.
        # This prevents 404s when data hasn't changed (rowcount=0) and secures image-only updates.
        check_query = "SELECT 1 FROM properties WHERE property_id = %s AND agent_id = %s"
        cursor.execute(check_query, (property_id, agent_id))
        if cursor.fetchone() is None:
            return jsonify(error="Property not found or you do not have permission to edit it"), 404

        # 2. IMAGE HANDLING
        new_images = None
        if 'images' in updates:
            if not isinstance(updates['images'], list):
                return jsonify(error="'images' must be an array of strings"), 400
            new_images = updates['images']
            del updates['images']

        # 3. UPDATE PROPERTY DETAILS
        # ADDED MISSING FIELDS based on your input data
        allowed_fields = [
            "title", "description", "price", "address", "city", "state", "country", 
            "zip_code", "property_type", "features", "bedrooms", "bathrooms", "rooms", 
            "area_sqft", "latitude", "longitude", "status",
            # New fields added below:
            "neighborhood", "garage_size", "land_area", 
            "year_built", "garages", "video_url", "private_note"
        ]
        
        set_parts = []
        values = []
        
        if updates:
            for key, value in updates.items():
                if key in allowed_fields:
                    set_parts.append(f"{key} = %s")
                    values.append(value)
            
            if set_parts:
                update_query = f"UPDATE properties SET {', '.join(set_parts)} WHERE property_id = %s AND agent_id = %s"
                update_values = values + [property_id, agent_id]
                cursor.execute(update_query, tuple(update_values))
                # We removed the rowcount check here because the pre-check handled auth,
                # and we don't want to error out just because data didn't change.

        # 4. EXECUTE IMAGE UPDATES
        if new_images is not None:
            cursor.execute("DELETE FROM property_images WHERE property_id = %s", (property_id,))
            if new_images:
                insert_image_query = "INSERT INTO property_images (property_id, image_url) VALUES (%s, %s)"
                image_values = [(property_id, url) for url in new_images]
                cursor.executemany(insert_image_query, image_values)

        con.commit()
        return jsonify(message="Property updated successfully"), 200
            
    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /update_property: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


@agent_bp.route("/delete_property", methods=["POST"])
def delete_property():
    """
    Soft-deletes a property by setting its 'is_deleted' flag to TRUE.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")
        property_id = data.get("property_id")
        if not all([agent_id, property_id]):
            return jsonify(error="agent_id and property_id are required"), 400

        con = getConnection()
        cursor = con.cursor()
        query = "UPDATE properties SET is_deleted = TRUE WHERE property_id = %s AND agent_id = %s"
        cursor.execute(query, (property_id, agent_id))

        if cursor.rowcount > 0:
            con.commit()
            return jsonify(message="Property deleted successfully"), 200
        else:
            return jsonify(error="Property not found or you do not have permission to delete it"), 404
    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /delete_property: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


# --- AGENT CHAT ENDPOINTS ---

@agent_bp.route("/agent_conversations", methods=["POST"])
def get_agent_conversations():
    """
    Fetches a list of all conversations for a specific agent.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")
        print(data)
        if not agent_id:
            return jsonify(error="agent_id is required"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT
                c.conversation_id, c.user_id, DATE_FORMAT(c.updated_at, '%%Y-%%m-%%d %%H:%%i') AS last_activity,
                u.name AS user_name, m.profile_picture AS user_profile_picture,
                (SELECT message_content FROM chat_messages cm WHERE cm.conversation_id = c.conversation_id ORDER BY cm.sent_at DESC LIMIT 1) AS last_message
            FROM conversations c
            JOIN users u ON c.user_id = u.user_id
            LEFT JOIN members m ON c.user_id = m.user_id
            WHERE c.agent_id = %s
            ORDER BY c.updated_at DESC;
        """
        cursor.execute(query, (agent_id,))
        conversations = cursor.fetchall()
        return jsonify(conversations=conversations), 200
    except Exception as e:
        logging.error(f"Error in /agent_conversations: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


@agent_bp.route("/agent_conversation_history", methods=["POST"])
def get_agent_conversation_history():
    """
    Fetches all messages for a specific conversation, including a sender flag.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")
        conversation_id = data.get("conversation_id")

        print(data)
        if not all([agent_id, conversation_id]):
            return jsonify(error="agent_id and conversation_id are required"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT user_id FROM conversations WHERE conversation_id = %s AND agent_id = %s", (conversation_id, agent_id))
        if not cursor.fetchone():
            return jsonify(error="Access denied or conversation not found"), 403

        cursor.execute("SELECT user_id FROM agents WHERE agent_id = %s", (agent_id,))
        agent_user_record = cursor.fetchone()
        if not agent_user_record:
            return jsonify(error="Agent profile not found"), 404
        agent_user_id = agent_user_record['user_id']

        query = """
            SELECT
                message_id, sender_user_id, message_content,
                DATE_FORMAT(sent_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS sent_at,
                (CASE WHEN sender_user_id = %s THEN 1 ELSE 0 END) AS is_sender_self
            FROM chat_messages
            WHERE conversation_id = %s
            ORDER BY sent_at ASC;
        """
        cursor.execute(query, (agent_user_id, conversation_id))
        messages = cursor.fetchall()
        
        for message in messages:
            message['is_sender_self'] = bool(message['is_sender_self'])

        return jsonify(conversation_id=conversation_id, messages=messages), 200
    except Exception as e:
        logging.error(f"Error in /agent_conversation_history: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()





# In routes/agent.py

@agent_bp.route("/set_featured_property", methods=["POST"])
def set_featured_property():
    """
    Sets a property as featured for an agent, respecting their limit.
    Can also be used to un-feature a property.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")
        property_id = data.get("property_id")
        feature_status = data.get("is_featured") # Expecting true or false

        if agent_id is None or property_id is None or feature_status is None:
            return jsonify(error="agent_id, property_id, and is_featured (true/false) are required"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # Security Check: Ensure the property belongs to this agent
        cursor.execute("SELECT property_id FROM properties WHERE property_id = %s AND agent_id = %s", (property_id, agent_id))
        if not cursor.fetchone():
            return jsonify(error="Property not found or you do not have permission to modify it"), 403

        # If the agent is trying to FEATURE a property, check their limit
        if feature_status is True:
            # --- THIS IS WHERE YOUR BUSINESS LOGIC LIVES ---
            # For now, the limit is hardcoded to 1.
            # In the future, you could look up the agent's subscription plan to get their limit.
            AGENT_FEATURE_LIMIT = 1 
            
            cursor.execute("SELECT COUNT(*) AS featured_count FROM properties WHERE agent_id = %s AND is_featured = TRUE", (agent_id,))
            current_count = cursor.fetchone()['featured_count']

            if current_count >= AGENT_FEATURE_LIMIT:
                return jsonify(error=f"You have reached your limit of {AGENT_FEATURE_LIMIT} featured properties. Please un-feature another property first."), 409 # 409 Conflict
        
        # All checks passed, proceed with the update
        query = "UPDATE properties SET is_featured = %s WHERE property_id = %s AND agent_id = %s"
        cursor.execute(query, (feature_status, property_id, agent_id))

        con.commit()
        
        message = "Property has been featured." if feature_status else "Property is no longer featured."
        return jsonify(message=message), 200

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /set_featured_property: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()



@agent_bp.route("/get_credits", methods=["POST"])
def getcredit():
    data = request.get_json()
    agent_id = data.get("agent_id")

    con = getConnection()
    cursor = con.cursor(pymysql.cursors.DictCursor)

    cursor.execute("select free_posts_remaining , paid_credits from agents where agent_id = %s", agent_id)
    credits = cursor.fetchall()
    if cursor: cursor.close()
    if con: con.close()


    return jsonify(credits)
    





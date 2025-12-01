import pymysql.cursors
import logging
from flask import Blueprint, request, jsonify
from app import getConnection

admin_bp = Blueprint('admin', __name__)
logging.basicConfig(level=logging.INFO)


@admin_bp.route("/admin/set_free_posts", methods=["POST"])
def set_free_posts():
    """
    Allows an admin to set the default number of free posts for new agents.
    NOTE: In a real app, this should be protected by an admin authentication check.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        new_count = data.get("free_posts")
        print(data)
        if new_count is None or not isinstance(new_count, int):
            return jsonify(error="'count' is required and must be an integer."), 400

        con = getConnection()
        cursor = con.cursor()
        
        # Use INSERT ... ON DUPLICATE KEY UPDATE to set the value, which is robust
        query = "INSERT INTO system_settings (setting_key, setting_value) VALUES ('default_free_posts', %s) ON DUPLICATE KEY UPDATE setting_value = %s"
        cursor.execute(query, (new_count, new_count))
        
        con.commit()
        
        return jsonify(message=f"Default free posts for new agents has been set to {new_count}."), 200
        
    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /admin/set_free_posts: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


@admin_bp.route("/admin/get_freepost", methods=["GET"])
def get_freepost():
    con = None
    cursor = None

    Query ="Select * from system_settings"
    
    con = getConnection()
    cursor = con.cursor()
    cursor.execute(Query)

    con.commit()
    data = cursor.fetchall()
    if cursor: cursor.close()
    if con: con.close()

    return jsonify (freepost = data),200

       
    



# In routes/admin.py

# --- ADMIN CREDIT PLAN MANAGEMENT ---

@admin_bp.route("/admin/create_credit_plan", methods=["POST"])
def create_credit_plan():
    """
    Admin: Creates a new credit purchase plan.
    """
    # NOTE: Add admin authentication here
    con = None
    cursor = None
    try:
        data = request.get_json()
        plan_name = data.get("plan_name")
        credits_amount = data.get("credits_amount")
        price = data.get("price")
        description = data.get("description") # Optional

        if not all([plan_name, credits_amount, price]):
            return jsonify(error="plan_name, credits_amount, and price are required"), 400

        con = getConnection()
        cursor = con.cursor()
        query = "INSERT INTO credit_plans (plan_name, credits_amount, price, description) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (plan_name, credits_amount, price, description))
        plan_id = cursor.lastrowid
        con.commit()
        
        return jsonify(message="Credit plan created successfully.", plan_id=plan_id), 201
    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /admin/create_credit_plan: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


@admin_bp.route("/admin/update_credit_plan", methods=["POST"])
def update_credit_plan():
    """
    Admin: Updates an existing credit plan (e.g., change price, name, or deactivate).
    """
    # NOTE: Add admin authentication here
    con = None
    cursor = None
    try:
        data = request.get_json()
        plan_id = data.get("plan_id")
        updates = data.get("updates") # A dictionary of fields to update

        print(data)

        if not all([plan_id, updates]):
            return jsonify(error="plan_id and an 'updates' object are required"), 400
        
        # Build query dynamically
        set_parts = []
        values = []
        allowed_fields = ["plan_name", "credits_amount", "price", "description", "is_active"]
        for key, value in updates.items():
            if key in allowed_fields:
                set_parts.append(f"{key} = %s")
                values.append(value)
        
        if not set_parts: return jsonify(error="No valid fields to update."), 400

        values.append(plan_id)
        query = f"UPDATE credit_plans SET {', '.join(set_parts)} WHERE plan_id = %s"
        
        con = getConnection()
        cursor = con.cursor()
        cursor.execute(query, tuple(values))
        
        if cursor.rowcount == 0: return jsonify(error="Credit plan not found."), 404
        
        con.commit()
        return jsonify(message="Credit plan updated successfully."), 200

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /admin/update_credit_plan: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


@admin_bp.route("/admin/get_all_credit_plans", methods=["GET"])
def get_all_credit_plans():
    """
    Admin: Retrieves ALL credit plans (active and inactive).
    Used to populate the Admin Dashboard table.
    """
    # NOTE: Add admin authentication here
    con = None
    cursor = None
    try:
        con = getConnection()
        cursor = con.cursor()

        # Select all columns. 
        # We assume you have an 'is_active' column to know status.
        # Ordered by plan_id ASC so the list doesn't jump around.
        query = """
            SELECT * 
            FROM credit_plans 
            ORDER BY plan_id ASC
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()

        # Convert database tuples into a list of dictionaries (JSON)
        # This makes it easy to read in React/Frontend
        # cursor.description contains column headers
        

        return jsonify(creditplans = rows), 200

    except Exception as e:
        logging.error(f"Error in /admin/get_all_credit_plans: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()















@admin_bp.route("/admin_agents", methods=["GET"])
def pending_agent():
    con=None
    cursor=None
    query = "select * from agents a join users u on u.user_id = a.user_id"

    try:
        con = getConnection()
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        return jsonify(agents = data)
    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /admin/update_credit_plan: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


@admin_bp.route("/change_status_agent" , methods = ["POST"])
def change_status_agent():
    con=None
    cursor=None
    try:
        data = request.get_json()
        agent_id = data.get("agent_id")
        user_id = data.get("user_id")
        agent_status = data.get("agent_status")
        con = getConnection()
        cursor = con.cursor()
        query1 = "update users set role_id = %s where user_id = %s"
        query2 = "update agents set agent_status = %s where agent_id = %s"

        if(agent_status == "approved"):
            t = (2 , user_id)
            t2 = (agent_status,agent_id)

            cursor.execute(query1 , t)
            cursor.execute(query2 , t2)
            con.commit()

            return jsonify("success")
        elif (agent_status == "rejected"):
            t = (1 , user_id)
            t2 = (agent_status,agent_id)

            print(t)
            print(t2)

            cursor.execute(query1 , t)
            cursor.execute(query2 , t2)
            con.commit()
            return jsonify("success")
    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /admin/update_credit_plan: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


            












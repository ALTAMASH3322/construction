import logging
from flask import Blueprint, app, request, redirect, url_for, flash, session, jsonify, Flask ,current_app
from app import getConnection 
import os
from werkzeug.utils import secure_filename
from flask import current_app , send_from_directory
import pymysql.cursors
import pymysql
import uuid







auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth_bp.route("/users", methods=["POST", "GET"])
def User():
    """
    Handles creating a new user (POST) and fetching all users (GET).
    """
    con = None
    cursor = None

    try:
        if request.method == "POST":
            # --- POST LOGIC: CREATE A NEW USER ---
            data = request.get_json()
            name = data.get("fullName")
            email = data.get("email")
            password = data.get("password")

            print(data)

            # 1. Input Validation
            if not all([name, email, password]):
                return jsonify(error="fullName, email, and password are required"), 400

            con = getConnection()
            cursor = con.cursor()

            try:
                # 2. Execute the INSERT query
                query = "INSERT INTO users (role_id, name, email, password_hash) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (1, name, email, password))
                con.commit()
                
                cursor.execute( "select user_id from users WHERE email = %s ", (email))
                data = cursor.fetchall()
                user_id = data[0]
                logging.info(f"Successfully created user with ID: {user_id}")
                return jsonify(message="User created successfully", user_id=user_id), 201 # 201 Created

            except pymysql.err.IntegrityError as e:
                # 3. Gracefully handle duplicate email errors
                if 'Duplicate entry' in str(e):
                    logging.warning(f"Attempted to create user with existing email: {email}")
                    return jsonify(error="A user with this email already exists"), 409 # 409 Conflict
                else:
                    # Handle other potential integrity errors
                    raise e

        elif request.method == "GET":
            # --- GET LOGIC: FETCH ALL USERS ---
            con = getConnection()
            # Use a DictCursor for a user-friendly JSON response
            cursor = con.cursor(pymysql.cursors.DictCursor)
            
            cursor.execute("SELECT user_id, role_id, name, email, is_active, created_at FROM users")
            all_users = cursor.fetchall()

            return jsonify(users=all_users), 200

    except Exception as e:
        if con:
            con.rollback()
        logging.error(f"Error in /users: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500

    finally:
        # 4. This is CRITICAL. It ensures the connection is always closed for both GET and POST.
        if cursor:
            cursor.close()
        if con:
            con.close()

# second api for Login

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Handles user login with plain text passwords.
    This version is stable and fixes all crashing bugs.
    """
    con = None
    cursor = None

    try:
        # 1. Get and validate input
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify(error="Email and password are required"), 400

        con = getConnection()
        # 2. FIX: Use a DictCursor to access results by column name (e.g., user['user_id'])
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # 3. FIX: Changed LIKE to = for correct and faster matching
        query = """
            SELECT 
                u.name,
                u.user_id, 
                u.role_id, 
                a.agent_id
            FROM users u 
            LEFT JOIN agents a ON u.user_id = a.user_id 
            WHERE u.email = %s AND u.password_hash = SHA2(%s, 256)
        """
        cursor.execute(query, (email, password))
        
        # 4. FIX: Use fetchone() for a single result and to prevent crashes
        user = cursor.fetchall()

        # 5. FIX: Safely check if a user was found before trying to access data
        if user:
            # Login successful
            logging.info(f"Successful login for user_id: {user}")
            return jsonify(
                message="success",
                
                name = user[0]["name"],user_id = user[0]["user_id"], role_id = user[0]["role_id"] , agent_id = user[0]["agent_id"]), 200
        else:
            # Login failed. This now works without crashing.
            logging.warning(f"Failed login attempt for email: {email}")
            return jsonify(message="failed", error="Invalid email or password"), 401

    except Exception as e:
        logging.error(f"Error in /login: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500

    finally:
        # 6. FIX: Added a finally block to always close the connection
        if cursor:
            cursor.close()
        if con:
            con.close()




@auth_bp.route("/company", methods=["POST", "GET"])
def company():
    """
    Handles creating/updating a company profile (POST) and
    fetching all company profiles (GET).
    """
    con = None
    cursor = None

    try:
        if request.method == "POST":
            # --- POST LOGIC: CREATE OR UPDATE A COMPANY ---
            data = request.get_json()
            company_name = data.get("company_name")

            # 1. Input Validation
            if not company_name:
                return jsonify(error="company_name is a required field"), 400

            # 2. Gather all data into a dictionary for clean execution
            # This also corrects the typos from the original code
            company_data = {
                "company_name": company_name,
                "company_type": data.get("company_type"),
                "license_number": data.get("company_licence"),
                "country": data.get("country"),
                "state": data.get("state"),
                "city": data.get("city"),
                "company_address": data.get("address"),
                "postal_code": data.get("postal_code"),
                "contact_person_name": data.get("contact_company_person"),
                "contact_person_role": data.get("contact_person_role"), # Corrected key
                "phone_number": data.get("company_contact"),
                "email": data.get("email"),
                "website": data.get("website"),
                "description": data.get("description"),
                "years_in_business": data.get("years_in_bussiness"), # Corrected key
                "facebook": data.get("facebook"),
                "instagram": data.get("instagram"),
                "linkedin": data.get("linkdin"), # Corrected key
                "x_account": data.get("x")
            }

            con = getConnection()
            cursor = con.cursor()

            # 3. Use "INSERT ... ON DUPLICATE KEY UPDATE" for an efficient "upsert".
            # NOTE: This requires a UNIQUE index on the `company_name` column in your 'companies' table.
            query = """
                INSERT INTO companies (company_name, company_type, license_number, country, state, city, company_address, postal_code, contact_person_name, contact_person_role, phone_number, email, website, description, years_in_business, facebook, instagram, linkedin, x_account)
                VALUES (%(company_name)s, %(company_type)s, %(license_number)s, %(country)s, %(state)s, %(city)s, %(company_address)s, %(postal_code)s, %(contact_person_name)s, %(contact_person_role)s, %(phone_number)s, %(email)s, %(website)s, %(description)s, %(years_in_business)s, %(facebook)s, %(instagram)s, %(linkedin)s, %(x_account)s)
                ON DUPLICATE KEY UPDATE
                    company_type=VALUES(company_type), license_number=VALUES(license_number), country=VALUES(country), state=VALUES(state), city=VALUES(city), company_address=VALUES(company_address), postal_code=VALUES(postal_code), contact_person_name=VALUES(contact_person_name), contact_person_role=VALUES(contact_person_role), phone_number=VALUES(phone_number), email=VALUES(email), website=VALUES(website), description=VALUES(description), years_in_business=VALUES(years_in_business), facebook=VALUES(facebook), instagram=VALUES(instagram), linkedin=VALUES(linkedin), x_account=VALUES(x_account);
            """
            cursor.execute(query, company_data)
            
            company_id = cursor.lastrowid
            
            if cursor.rowcount == 1:
                message = "Company profile created successfully"
                status_code = 201
            else:
                message = "Company profile updated successfully"
                status_code = 200
                # If it's an update, lastrowid is 0. We need to fetch the ID.
                if company_id == 0:
                    cursor.execute("SELECT company_id FROM companies WHERE company_name = %s", (company_name,))
                    result = cursor.fetchone()
                    company_id = result[0] if result else None

            con.commit()
            return jsonify(message=message, company_id=company_id), status_code

        elif request.method == "GET":
            # --- GET LOGIC: FETCH ALL COMPANIES ---
            con = getConnection()
            cursor = con.cursor(pymysql.cursors.DictCursor)
            
            cursor.execute("SELECT * FROM companies")
            all_companies = cursor.fetchall()

            return jsonify(companies=all_companies), 200

    except Exception as e:
        if con:
            con.rollback()
        logging.error(f"Error in /company: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500

    finally:
        if con:
            con.close()
        if cursor:
            cursor.close()

# In routes/auth.py

@auth_bp.route("/agent", methods=["POST", "GET"])
def agents():
    """
    Handles creating a new agent profile (and assigning free posts)
    or updating an existing agent profile.
    """
    con = None
    cursor = None
    try:
        if request.method == "POST":
            user_id = request.form.get("user_id")
            
            print(request.form)

            if not user_id:
                return jsonify(error="user_id is a required field"), 400
            
            

            con = getConnection()
            cursor = con.cursor(pymysql.cursors.DictCursor)

            # First, check if an agent profile already exists for this user_id
            cursor.execute("SELECT agent_id FROM agents WHERE user_id = %s", (user_id,))
            agent_record = cursor.fetchone()
            is_new_agent = agent_record is None

            # Handle file upload (this logic is the same for both create and update)
            image_url, file_to_save, unique_filename, save_path = None, None, None, None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    unique_filename = f"{user_id}_{secure_filename(file.filename)}"
                    image_url = f"/uploads/{unique_filename}"
                    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                    file_to_save = file
            
            # If no new file is uploaded on an update, keep the old one.
            if not is_new_agent and not file_to_save:
                image_url = request.form.get("existing_profile_pic_url")


# --- FULLY CORRECTED FORM DATA BUILDER ---

# Gather all form data into a dictionary
            form_data = {
                "user_id": user_id,
                "agent_type": request.form.get("agent_type"),
                "company_id": request.form.get("company_id"),
                "company_position": request.form.get("company_position"),
                # This might be optional, but use the correct name from the form if it exists
                "company_license_number": request.form.get("company_licence"), 
                "personal_license_number": request.form.get("personal_license_number"),

                # FIX: Correct the typo to match the form field name
                "license_issuing_authority": request.form.get("license_issuing_authority"), 

                "country": request.form.get("country"),
                "state": request.form.get("region"),

                # FIX: Decide what 'city' should be. If the form doesn't send it, it will be None.
                # If 'address_city' is supposed to be the city, you can do this:
                # "city": request.form.get("address_city"),
                # For now, we assume 'city' might be a separate, optional field.
                "city": request.form.get("city"), 

                "address_city": request.form.get("address_city"),
                "address_postal_code": request.form.get("address_postal_code"),
                "contact_number": request.form.get("contact"),
                "email": request.form.get("email"),
                "experience_years": request.form.get("experience"),
                "specialization": request.form.get("specialization"),
                "bio": request.form.get("bio"),
                "linkedin": request.form.get("linkdin"),
                "instagram": request.form.get("instagram"),
                "facebook": request.form.get("facebook"),
                "x_account": request.form.get("x_account"),
                "personal_website": request.form.get("personal_website"),
                "profile_picture": image_url
            }

            print(form_data)

            if is_new_agent:
                # --- THIS IS AN INSERT FOR A NEW AGENT ---
                # Fetch the default number of free posts from system_settings
                cursor.execute("SELECT setting_value FROM system_settings WHERE setting_key = 'default_free_posts'")
                settings = cursor.fetchone()
                free_posts = int(settings['setting_value']) if settings else 1
                form_data['free_posts_remaining'] = free_posts

                # Build the INSERT query dynamically
                columns = ', '.join(form_data.keys())
                placeholders = ', '.join([f"%({key})s" for key in form_data.keys()])
                query = f"INSERT INTO agents ({columns}) VALUES ({placeholders})"
                
                message = "Agent profile created successfully."
                status_code = 201
            else:
                # --- THIS IS AN UPDATE FOR AN EXISTING AGENT ---
                # We do not update free_posts_remaining on an edit
                set_clause = ', '.join([f"{key}=%({key})s" for key in form_data.keys() if key != 'user_id'])
                query = f"UPDATE agents SET {set_clause} WHERE user_id = %(user_id)s"
                
                message = "Agent profile updated successfully."
                status_code = 200

            # Execute the chosen query (either INSERT or UPDATE)
            cursor.execute(query, form_data)
            
            # Save the file only after a successful DB operation
            if file_to_save:
                file_to_save.save(save_path)
            
            # Determine the agent_id to return
            agent_id = agent_record['agent_id'] if agent_record else cursor.lastrowid
            con.commit()
            
            return jsonify(message=message, agent_id=agent_id), status_code

        elif request.method == "GET":
            # GET logic is unchanged
            con = getConnection()
            cursor = con.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM agents")
            all_agents = cursor.fetchall()
            return jsonify(agents=all_agents), 200

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /agent: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()

@auth_bp.route("/agentstatus", methods=["POST"])
def update_agent_status():
    data = request.get_json()
    status = data.get("status")
    user_id = data.get("user_id")

    print(status, user_id)

    if not status or not user_id:
        return jsonify({"error": "Missing status or user_id"}), 400

    con = getConnection()
    cursor = con.cursor()

    try:
        # Step 1: Get current agent_status
        cursor.execute("SELECT agent_status FROM agents WHERE user_id = %s", (user_id,))
        current_status = cursor.fetchone()
        print(current_status["agent_status"])

        if not current_status:
            return jsonify({"error": "Agent not found"}), 404

        current_status = current_status["agent_status"]

        # Step 2: Check if already approved or rejected
        if current_status in ["approved", "rejected"]:
            return jsonify({"error": f"Action denied. Current status is '{current_status}'."}), 400

        # Step 3: Proceed with update if status is 'pending'
        if status == "Accepted":
            cursor.execute("UPDATE agents SET agent_status = %s WHERE user_id = %s", ("approved", user_id))
            cursor.execute("UPDATE users SET role_id = %s WHERE user_id = %s", (2, user_id))
        elif status == "Rejected":
            cursor.execute("UPDATE agents SET agent_status = %s WHERE user_id = %s", ("rejected", user_id))
            cursor.execute("UPDATE users SET role_id = %s WHERE user_id = %s", (1, user_id))
        else:
            return jsonify({"error": "Invalid status value"}), 400

        con.commit()
        return jsonify({"message": "Agent status updated successfully"}), 200

    except Exception as e:
        con.rollback()
        print(f"[ERROR] Failed to update agent status: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        con.close()

@auth_bp.route("/member", methods=["POST", "GET"])
def members():
    """
    Handles creating/updating a member profile (POST) and
    fetching all member profiles (GET).
    """
    con = None
    cursor = None

    try:
        if request.method == "POST":
            # --- POST LOGIC: CREATE OR UPDATE A MEMBER ---
            data = request.get_json()
            user_id = data.get("user_id")

            # 1. Input Validation
            if not user_id:
                return jsonify(error="user_id is a required field"), 400

            # Collect all other fields from the request
            contact = data.get("contact")
            gender = data.get("gender")
            dob = data.get("dob") # Ensure frontend sends in 'YYYY-MM-DD' format
            address = data.get("address")
            profile = data.get("profilepic")
            occupation = data.get("occupation")
            bio = data.get("bio")

            con = getConnection()
            cursor = con.cursor()

            # 2. Use "INSERT ... ON DUPLICATE KEY UPDATE" for an efficient "upsert"
            query = """
                INSERT INTO members (user_id, contact, gender, date_of_birth, address, profile_picture, occupation, bio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    contact = VALUES(contact),
                    gender = VALUES(gender),
                    date_of_birth = VALUES(date_of_birth),
                    address = VALUES(address),
                    profile_picture = VALUES(profile_picture),
                    occupation = VALUES(occupation),
                    bio = VALUES(bio);
            """
            cursor.execute(query, (user_id, contact, gender, dob, address, profile, occupation, bio))

            # 3. Check cursor.rowcount to see what happened
            # 1 = A new row was inserted.
            # 2 = An existing row was updated.
            # 0 = An existing row was "updated" with the exact same data (no change).
            if cursor.rowcount == 1:
                message = "Profile created successfully"
                status_code = 201 # 201 Created
            else:
                message = "Profile updated successfully"
                status_code = 200 # 200 OK

            con.commit()
            return jsonify(message=message), status_code

        elif request.method == "GET":
            # --- GET LOGIC: FETCH ALL MEMBERS ---
            con = getConnection()
            # Use a DictCursor to get results as dictionaries
            cursor = con.cursor(pymysql.cursors.DictCursor)
            
            cursor.execute("SELECT * FROM members")
            all_members = cursor.fetchall()

            return jsonify(members=all_members), 200

    except Exception as e:
        if con:
            con.rollback() # Rollback any partial changes from the POST
        logging.error(f"Error in /member: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500

    finally:
        # This is CRITICAL. It ensures the connection is always closed.
        if cursor:
            cursor.close()
        if con:
            con.close()

@auth_bp.route("/getmember", methods=["POST"])
def onlyMember():
    """
    Fetches the profile details for a single member by their user_id.
    """
    con = None
    cursor = None

    try:
        # 1. Get and validate the input
        data = request.get_json()
        if not data or "user_id" not in data:
            return jsonify(error="user_id is required"), 400

        try:
            user_id = data.get("user_id")
        except (ValueError, TypeError):
            return jsonify(error="user_id must be a valid integer"), 400

        # 2. Connect to the database
        con = getConnection()
        # Use a DictCursor to get the result as a dictionary
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # 3. Execute the correct and efficient query
        # Use '=' for an exact match and 'fetchone' since we expect only one result
        query = "SELECT * FROM members WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        
        member_data = cursor.fetchall()

        # 4. Handle the result correctly
        if member_data:
            print(member_data)
            # A member profile was found
            logging.info(f"Successfully found member profile for user_id {user_id}")
            print(member_data)
            return jsonify(message="success", fullData =member_data), 200
        else:
            # No profile was found for this user_id
            logging.warning(f"No member profile found for user_id {user_id}")
            return jsonify(error="Member profile not found"), 404

    except Exception as e:
        logging.error(f"Error in /getmember: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500

    finally:
        # 5. Always ensure the connection is closed
        if cursor:
            cursor.close()
        if con:
            con.close()


@auth_bp.route("/agentid", methods=["POST"])
def agentId():
    """
    Checks if a user_id corresponds to an agent.
    If yes, returns the agent's IDs.
    If no, returns a clear 'not_agent' status.
    """
    con = None
    cursor = None

    try:
        # 1. Get and validate the input
        data = request.get_json()
        if not data or "user_id" not in data:
            return jsonify(error="user_id is required"), 400

        try:
            user_id = data.get("user_id")
        except (ValueError, TypeError):
            return jsonify(error="user_id must be a valid integer"), 400

        # 2. Connect to the database
        con = getConnection()
        # Use a DictCursor for dictionary-like results
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # 3. Execute the correct query
        # Fetch both the primary ID and the new public ID
        query = "SELECT agent_id FROM agents WHERE user_id = %s"
        
        cursor.execute(query, (user_id,))
        
        # Use fetchone() as there should only ever be one agent per user
        agent_record = cursor.fetchone()

        # 4. Handle both "found" and "not found" cases gracefully
        if agent_record:
            # The user IS an agent. Return their details.
            logging.info(f"Agent found for user_id {user_id}: agent_id {agent_record['agent_id']}")
            return jsonify(
                status="agent",
                agent_id=agent_record['agent_id'],
                
            ), 200
        else:
            # The user IS NOT an agent. Return a clear status.
            logging.info(f"No agent profile found for user_id {user_id}")
            return jsonify(status="not_agent"), 200 # Using 200 OK because the check was successful

    except Exception as e:
        logging.error(f"Error in /agentid: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500

    finally:
        # 5. Always ensure the connection is closed
        if cursor:
            cursor.close()
        if con:
            con.close()


# In routes/auth.py

# Make sure these imports are at the top of your auth_bp file


# Assuming 'auth_bp' and 'getConnection' are defined elsewhere

@auth_bp.route("/sendproperties", methods=["POST"])
def create_property():
    """
    Creates a new property listing from form data and uploaded images.
    Includes all extended fields (neighborhood, garages, video_url, etc.).
    """
    con = None
    cursor = None
    try:
        # 1. Get basic data
        agent_id = request.form.get("agent_id")
        title = request.form.get("title")

        # Debug print to see what is coming in
        print("Received Form Data:", request.form)

        if not agent_id:
            return jsonify(error="agent_id is required"), 400

        # 2. Get images
        uploaded_files = request.files.getlist("images")

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # --- CREDIT CHECKING LOGIC ---
        cursor.execute("SELECT free_posts_remaining, paid_credits FROM agents WHERE agent_id = %s", (agent_id,))
        agent = cursor.fetchone()
        
        if not agent:
            return jsonify(error="Agent not found"), 404

        if agent['free_posts_remaining'] > 0:
            cursor.execute("UPDATE agents SET free_posts_remaining = free_posts_remaining - 1 WHERE agent_id = %s", (agent_id,))
            logging.info(f"Agent {agent_id} used a free post.")
        elif agent['paid_credits'] > 0:
            cursor.execute("UPDATE agents SET paid_credits = paid_credits - 1 WHERE agent_id = %s", (agent_id,))
            description = f"Spent 1 credit to post property: {title}"
            cursor.execute("INSERT INTO transactions (agent_id, transaction_type, amount, description) VALUES (%s, 'spend', -1, %s)", (agent_id, description))
            logging.info(f"Agent {agent_id} spent 1 paid credit.")
        else:
            return jsonify(error="Insufficient credits or free posts. Please purchase more credits to post a property."), 402
        # --- END CREDIT LOGIC ---

        # 3. Insert Property
        # Note: 'longitude' is kept as requested (matching your DB column name)
        insert_property_query = """
            INSERT INTO properties (
                agent_id, title, description, price, address, city, state, country, zip_code, 
                property_type, features, bedrooms, bathrooms, rooms, area_sqft, latitude, longitude, status,
                neighborhood, label, price_unit, before_label, after_label, land_area, garages, 
                garage_size, year_built, private_note, video_url
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s
            )
        """

        property_values = (
            agent_id,
            title,
            request.form.get("description"),
            request.form.get("price"),
            request.form.get("address"),
            request.form.get("city"),
            request.form.get("state"),
            request.form.get("country"),
            request.form.get("zip_code"),
            request.form.get("property_type"),
            request.form.get("features"), # This maps to featuresString from your list
            request.form.get("bedrooms"),
            request.form.get("bathrooms"),
            request.form.get("rooms"),
            request.form.get("area_sqft"),
            request.form.get("latitude"),
            request.form.get("longitude"), # Value comes from form 'longitude', saves to DB column 'longitude'
            request.form.get("status"),
            # --- New Fields ---
            request.form.get("neighborhood"),
            request.form.get("label"),
            request.form.get("price_unit"),
            request.form.get("before_label"),
            request.form.get("after_label"),
            request.form.get("land_area"),
            request.form.get("garages"),
            request.form.get("garage_size"),
            request.form.get("year_built"),
            request.form.get("private_note"),
            request.form.get("video_url")
        )
        
        cursor.execute(insert_property_query, property_values)

        # The corrected code
        internal_property_id = cursor.lastrowid
        cursor.execute(
            "SELECT property_id FROM properties WHERE property_id_1 = %s", 
            (internal_property_id,)
        )
        # Use fetchone() to get the single dictionary result directly
        new_property_dict = cursor.fetchone() 
        
        # Access the 'property_id' value FROM the dictionary
        property_id = new_property_dict['property_id']
        
        # 4. Update Transaction Reference (if applicable)
        if agent['free_posts_remaining'] <= 0 and agent['paid_credits'] > 0:
             cursor.execute("UPDATE transactions SET reference_id = %s WHERE transaction_id = LAST_INSERT_ID()", (property_id,))

        # 5. Image Saving Logic
        saved_image_names = []
        if uploaded_files:
            for image_file in uploaded_files:
                if image_file and image_file.filename != '':
                    filename = secure_filename(image_file.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{filename}"
                    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                    image_file.save(save_path)
                    saved_image_names.append(unique_filename)

        # 6. Insert Images into DB
        if saved_image_names:
            insert_image_query = "INSERT INTO property_images (property_id, image_url) VALUES (%s, %s)"
            image_values = [(property_id, name) for name in saved_image_names]
            cursor.executemany(insert_image_query, image_values)

        con.commit()
        return jsonify(message="Your property has been submitted.", property_id=property_id), 201

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /sendproperties: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()







@auth_bp.route("/change_password", methods=['POST'])
def change_password():
    data = request.get_json()
    user_id = data.get('user_id')
    old_p = data.get('old_password')
    new_p = data.get('new_password')
    print(data)

    if not user_id:
        return jsonify(error="user_id is required"), 400
    if not old_p:
        return jsonify(error="old Password is required"), 400
    if not new_p:
        return jsonify(error="new Password is required"), 400   
    
    con = None
    cursor = None
    try:
        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # STEP 1: Verify the OLD password
        # We use SHA2(%s, 256) to hash the input and compare it to the stored hash
        verify_query = "SELECT user_id FROM users WHERE user_id = %s AND password_hash = SHA2(%s, 256)"
        cursor.execute(verify_query, (user_id, old_p))
        
        user = cursor.fetchone()

        if user:
            # STEP 2: Update to the NEW password
            # We must wrap the new password in SHA2(%s, 256) so it is stored correctly
            update_query = "UPDATE users SET password_hash = %s WHERE user_id = %s"
            cursor.execute(update_query, (new_p, user_id))
            
            # CRITICAL: Save the changes to the database
            con.commit()

            return jsonify("Password Updated successfully"), 200
        else:
            return jsonify(error="User_id and Password Do not match"), 400

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /changePassword: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()
    





# In routes/auth.py

@auth_bp.route("/getproperties", methods=["GET", "POST"])
def getProperty():
    con = None
    cursor = None
    try:
        request_data = request.get_json(silent=True) or request.args
        print("Incoming Data:", request_data)

        conditions = ["p.is_deleted = FALSE"]
        values = []

        # 1. Standard Filters
        # Removed 'status' from here to handle it manually below
        filter_fields = {
            "property_type": "string", 
            "city": "string", 
            "bedrooms": "int", 
            "bathrooms": "int"
        }

        for field, f_type in filter_fields.items():
            value = request_data.get(field)
            if value:
                try:
                    conditions.append(f"p.{field} {'LIKE' if f_type == 'string' else '='} %s")
                    values.append(f"%{value}%" if f_type == 'string' else int(value))
                except ValueError:
                    return jsonify(error=f"Invalid value for '{field}'"), 400

        # 2. FILTER FIX: Map 'listing_type' (Frontend) -> 'status' (Database)
        listing_type = request_data.get("listing_type") 
        if listing_type:
            # Maps "RENT" -> "rent" and checks p.status
            conditions.append("p.status = %s")
            values.append(listing_type.lower()) 
        
        # 3. Handle 'status' if sent directly
        status_req = request_data.get("status")
        if status_req:
             conditions.append("p.status = %s")
             values.append(status_req.lower())

        # 4. Range Filters
        range_filters = {
            "min_price": "p.price >= %s", 
            "max_price": "p.price <= %s", 
            "min_bedrooms": "p.bedrooms >= %s", 
            "max_bedrooms": "p.bedrooms <= %s"
        }
        for key, condition_str in range_filters.items():
            value = request_data.get(key)
            if value:
                conditions.append(condition_str)
                values.append(int(value))

        sort_by = request_data.get("sort_by", "default_rank")
        sort_order = request_data.get("sort_order", "desc").lower()
        #limit = int(request_data.get("limit", 6))
        limit =6
        offset = int(request_data.get("offset", 0))

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # 5. IMAGE FIX: Reverted to 'p.property_id' (String ID) for the JOIN
        query = """
            SELECT p.*, GROUP_CONCAT(i.image_url) AS images
            FROM properties p
            LEFT JOIN property_images i ON p.property_id = i.property_id
        """
        
        query += " WHERE " + " AND ".join(conditions)
        
        order_clause = ""
        if sort_by == 'default_rank':
            order_clause = "ORDER BY p.is_featured DESC, p.created_at DESC"
        else:
            allowed_sort_fields = ["price", "bedrooms", "created_at"]
            if sort_by not in allowed_sort_fields: sort_by = "created_at"
            order_clause = f"ORDER BY p.{sort_by} {sort_order}"

        # Group by the Primary Key (property_id_1)
        query += f" GROUP BY p.property_id_1 {order_clause} LIMIT %s OFFSET %s"
        values.extend([limit, offset])
        
        cursor.execute(query, tuple(values))
        properties = cursor.fetchall()

        for prop in properties:
            prop['images'] = prop['images'].split(',') if prop['images'] else []
            prop['is_featured'] = bool(prop['is_featured'])

        return jsonify(count=len(properties), properties=properties), 200

    except Exception as e:
        logging.error(f"Error in /getproperties: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()
   



@auth_bp.route("/favourite", methods=["POST"])
def favourite():
    """
    Adds a property to a user's favorites list.
    Handles duplicate requests gracefully.
    """
    con = None
    cursor = None

    try:
        # 1. Get and validate the input
        data = request.get_json()
        print(data)
        if not data or "user_id" not in data or "property_id" not in data:
            return jsonify(error="user_id and property_id are required"), 400

        try:
            user_id = data.get("user_id")
            property_id = data.get("property_id")
            print(user_id,property_id)
        except (ValueError, TypeError):
            return jsonify(error="user_id and property_id must be valid integers"), 400

        # 2. Connect to the database
        con = getConnection()
        cursor = con.cursor()

        # 3. Use 'INSERT IGNORE' to prevent crashes on duplicate entries.
        # If the (user_id, property_id) pair already exists, this query will
        # do nothing and will not raise an error.
        query = "INSERT IGNORE INTO favorites (user_id, property_id) VALUES (%s, %s)"
        cursor.execute(query, (user_id, property_id))

        # 4. Check if a new row was actually inserted
        if cursor.rowcount > 0:
            # A new favorite was added, so commit the transaction.
            con.commit()
            logging.info(f"User {user_id} added property {property_id} to favorites.")
            return jsonify(message="Added to favorites successfully"), 201  # 201 Created
        else:
            # No rows were inserted, meaning it was already a favorite.
            # No commit is needed.
            logging.info(f"User {user_id} tried to add existing favorite property {property_id}.")
            return jsonify(message="This property is already in your favorites"), 200 # 200 OK

    except Exception as e:
        # If any other error occurs, roll back the transaction
        if con:
            con.rollback()
        logging.error(f"Error in /favourite: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500

    finally:
        # 5. This is CRITICAL to prevent lock timeouts.
        # It ensures the connection is always closed, no matter what.
        if cursor:
            cursor.close()
        if con:
            con.close()


@auth_bp.route("/getfavourite", methods=["POST"])
def getFavourite():
    """
    Fetches all favorite properties for a user, with images grouped correctly.
    """
    con = None
    cursor = None
    
    try:
        data = request.get_json()
        print(data)
        if not data or "user_id" not in data:
            return jsonify(error="user_id is required"), 400
            
        try:
            user_id = data.get("user_id")
        except (ValueError, TypeError):
            return jsonify(error="user_id must be a valid integer"), 400

        con = getConnection()
        # Use a DictCursor to get results as dictionaries
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # This query uses GROUP_CONCAT to solve the image duplication problem
        query = """
            SELECT
                p.*,
                f.favorite_id,
                f.created_at AS favorited_at,
                GROUP_CONCAT(i.image_url) AS images
            FROM
                favorites AS f
            LEFT JOIN
                properties AS p ON f.property_id = p.property_id
            LEFT JOIN
                property_images AS i ON p.property_id = i.property_id
            WHERE
                f.user_id = %s
            GROUP BY
                p.property_id, f.favorite_id;
        """
        
        cursor.execute(query, (user_id,))
        
        favorites = cursor.fetchall()
        print(favorites)

        # Post-process the results to turn the image string into a proper list
        for fav in favorites:
            if fav['images']:
                fav['images'] = fav['images'].split(',')
            else:
                fav['images'] = [] # Ensure it's an empty list if there are no images

        return jsonify(message="Your favourites", favorites=favorites), 200

    except Exception as e:
        logging.error(f"Error in /getfavourite: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

@auth_bp.route("/deletefavourite", methods=["POST"])
def deleteFavourite():
    """
    Deletes a favorite record for a specific user and property.
    """
    con = None
    cursor = None

    try:
        # 1. Get and validate the input
        data = request.get_json()
        if not data or "user_id" not in data or "property_id" not in data:
            return jsonify(error="user_id and property_id are required"), 400

        try:
            user_id = data.get("user_id")
            property_id = data.get("property_id")
        except (ValueError, TypeError):
            return jsonify(error="user_id and property_id must be valid integers"), 400

        # 2. Connect to the database
        con = getConnection()
        cursor = con.cursor()

        # 3. Execute the DELETE query using '=' for correctness
        query = "DELETE FROM favorites WHERE user_id = %s AND property_id = %s"
        cursor.execute(query, (user_id, property_id))

        # 4. Check if a row was actually deleted
        if cursor.rowcount > 0:
            # If a row was affected, commit the change
            con.commit()
            logging.info(f"User {user_id} removed property {property_id} from favorites.")
            return jsonify(message="Removed from favorites successfully"), 200
        else:
            # If no rows were affected, it means the favorite didn't exist
            logging.warning(f"Attempted to remove non-existent favorite for user {user_id}, property {property_id}.")
            return jsonify(error="Favorite not found or already removed"), 404

    except Exception as e:
        # If any error occurs, roll back the transaction
        if con:
            con.rollback()
        logging.error(f"Error in /deletefavourite: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500

    finally:
        # 5. Always ensure the connection is closed
        if cursor:
            cursor.close()
        if con:
            con.close()



import urllib.parse
from flask import jsonify, request
# Make sure your blueprint (auth_bp) and getConnection are imported


# Ensure you have imported urllib.parse at the top

@auth_bp.route("/detailproperty", methods=["POST"])
def detailProperty():
    property_id = request.json.get("property_id")
    # print(property_id) # Debugging

    if not property_id:
        return jsonify(error="property_id is required"), 400

    con = None
    cursor = None
    try:
        con = getConnection()
        cursor = con.cursor()

        # --- QUERY 1: Get the main property details ---
        property_query = "SELECT * FROM properties WHERE property_id = %s"
        cursor.execute(property_query, (property_id,))
        
        property_details = cursor.fetchone() 

        if not property_details:
            return jsonify(message="Property not found"), 404

        # --- QUERY 2: Get all associated images ---
        images_query = "SELECT image_id, image_url, is_cover FROM property_images WHERE property_id = %s"
        cursor.execute(images_query, (property_id,))
        
        # --- THE FIX IS HERE ---
        # Since cursor.fetchone() above worked as a dictionary, fetchall() here 
        # returns a list of dictionaries. We don't need zip/dict conversion.
        images_list = cursor.fetchall() 
        
        property_details['images'] = images_list

        # --- Generate Google Maps Link ---
        google_maps_link = None
        lat = property_details.get('latitude')
        lon = property_details.get('longitude') 

        if lat and lon:
            try:
                # Basic check if they look like numbers
                float(lat); float(lon)
                # Ensure they aren't empty strings
                if str(lat).strip() != "" and str(lon).strip() != "":
                    google_maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            except (ValueError, TypeError):
                pass
        
        # Fallback to address
        if not google_maps_link:
            address_parts = [
                property_details.get('address'),
                property_details.get('city'),
                property_details.get('state'),
                property_details.get('zip_code'),
                property_details.get('country')
            ]
            full_address = ", ".join(part for part in address_parts if part)
            if full_address:
                encoded_address = urllib.parse.quote_plus(full_address)
                google_maps_link = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"
        
        property_details['google_maps_link'] = google_maps_link

        print(property_details)

        return jsonify(message="detail property", detail=property_details)

    except Exception as e:
        # print(f"An error occurred: {e}") 
        logging.error(f"Error in /detailproperty: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    
    finally:
        if cursor: cursor.close()
        if con: con.close()
















@auth_bp.route("/particularagent", methods=["POST"])  # Optional: fix typo in route
def particularAgent():
    agentId = request.json.get("agent_id")
    print(agentId)

    if not agentId:
        return jsonify(error="agent_id is required"), 400

    con = getConnection()
    cursor = con.cursor()

    # Prefer INNER JOIN or LEFT JOIN, depending on what data you need
    query = """
        SELECT * FROM agents AS a
        LEFT JOIN users AS u ON a.user_id = u.user_id
        left join companies c on a.company_id = c.company_id
        WHERE a.agent_id = %s
    """
    cursor.execute(query, (agentId,))
    result = cursor.fetchall()

    con.close()  # commit not needed
    print ("check")
    print(result)

    return jsonify(message="property agent", agent=result)






# @auth_bp("/booking", methods=["POST", "GET"])
# def booking():
#     user_id = request.json.get("user_id")




# In routes/auth.py

# Make sure this import is at the top of your file
from utils.email_helpers import send_email

# ... (rest of your auth_bp code) ...

@auth_bp.route("/contact_agent", methods=["POST"])
def contact_agent():
    """
    Handles the 'Contact Agent' form submission.
    Sends a notification email to the agent and a confirmation to the user.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        
        # 1. Get and validate all form fields
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        user_email = data.get("email")
        phone_number = data.get("phone") # Optional
        message = data.get("message")
        agent_id = data.get("agent_id")

        if not all([first_name, last_name, user_email, message, agent_id]):
            return jsonify(error="All required fields must be provided."), 400

        # 2. Fetch the agent's details (name and email) from the database
        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        
        # We need to join agents and users to get the agent's email address
        query = """
            SELECT u.name AS agent_name, u.email AS agent_email
            FROM agents a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.agent_id = %s;
        """
        cursor.execute(query, (agent_id,))
        agent_details = cursor.fetchone()

        if not agent_details:
            return jsonify(error="Agent not found."), 404

        # 3. Send the notification email TO THE AGENT
        agent_subject = f"New Lead: Inquiry from {first_name} {last_name}"
        agent_html_body = f"""
            <html>
            <body>
                <h2>You have a new property inquiry!</h2>
                <p>You've received a new message from a potential buyer. Here are their details:</p>
                <ul>
                    <li><b>Name:</b> {first_name} {last_name}</li>
                    <li><b>Email:</b> {user_email}</li>
                    <li><b>Phone:</b> {phone_number or "Not provided"}</li>
                </ul>
                <hr>
                <h3>Message:</h3>
                <p><i>"{message}"</i></p>
                <hr>
                <p>Please follow up with them soon!</p>
            </body>
            </html>
        """
        send_email(
            to=agent_details['agent_email'],
            subject=agent_subject,
            html_body=agent_html_body
        )

        # 4. Send the confirmation email TO THE USER
        user_subject = "Your message has been sent!"
        user_html_body = f"""
            <html>
            <body>
                <h2>Thank You, {first_name}!</h2>
                <p>Your message has been successfully sent to the agent, <b>{agent_details['agent_name']}</b>.</p>
                <p>They should get back to you shortly.</p>
                <br>
                <p>--- Your Sent Message ---</p>
                <p><i>"{message}"</i></p>
            </body>
            </html>
        """
        send_email(
            to=user_email,
            subject=user_subject,
            html_body=user_html_body
        )

        return jsonify(message="Your message has been sent successfully."), 200

    except Exception as e:
        logging.error(f"Error in /contact_agent: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred while sending your message."), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()




# In routes/auth.py

@auth_bp.route("/update_member", methods=["POST"])
def update_member():
    """
    Updates one or more fields of an existing member profile.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        updates = data.get("updates") # A dictionary of fields to update

        print(data)

        # 1. Input Validation
        if not user_id or not updates:
            return jsonify(error="user_id and an 'updates' object are required"), 400

        if not isinstance(updates, dict) or not updates:
            return jsonify(error="'updates' must be a non-empty dictionary"), 400

        con = getConnection()
        cursor = con.cursor()

        # 2. Dynamically build the SET part of the query for flexibility
        set_parts = []
        values = []
        
        # Whitelist of columns that are allowed to be updated
        allowed_fields = [
            "contact", "gender", "date_of_birth", "address", 
            "profile_picture", "occupation", "bio"
        ]

        for key, value in updates.items():
            if key in allowed_fields:
                set_parts.append(f"{key} = %s")
                values.append(value)
        
        # If no valid fields were sent, there's nothing to update
        if not set_parts:
            return jsonify(error="No valid fields to update were provided"), 400

        # Add the user_id for the WHERE clause
        values.append(user_id)

        # 3. Construct and execute the final UPDATE query
        query = f"UPDATE members SET {', '.join(set_parts)} WHERE user_id = %s"
        
        cursor.execute(query, tuple(values))

        # 4. Check if a row was actually affected
        if cursor.rowcount > 0:
            con.commit()
            logging.info(f"Successfully updated member profile for user_id {user_id}")
            return jsonify(message="Profile updated successfully"), 200
        else:
            # This can happen if the user_id doesn't exist in the members table
            logging.warning(f"Attempted to update a non-existent member profile for user_id {user_id}")
            return jsonify(error="Member profile not found to update"), 404

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /update_member: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()









# In routes/auth.py (or agent.py)

# In routes/auth.py (or agent.py)

@auth_bp.route("/update_agent", methods=["POST"])
def update_agent():
    """
    
    Updates an existing agent's profile, including their profile picture.
    Correctly handles keeping the existing picture if a new one is not provided.

    """
    con = None
    cursor = None
    try:
        agent_id = request.form.get("agent_id")
        user_id = request.form.get("user_id")
        print(user_id , agent_id)
        if not agent_id or not user_id:
            return jsonify(error="agent_id and user_id are required fields"), 400

        con = getConnection()
        cursor = con.cursor()
        
        # Dynamically build the SET part of the query
        set_parts = []
        values = []
        
        # --- THIS IS THE CORRECTED IMAGE LOGIC ---
        file_to_save = None
        save_path = None
        new_profile_picture_url = None

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                unique_filename = f"{user_id}_{secure_filename(file.filename)}"
                save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                new_profile_picture_url = f"/uploads/{unique_filename}"
                file_to_save = file
                
                # Add the profile picture update to the query
                set_parts.append("profile_picture = %s")
                values.append(new_profile_picture_url)
        # -------------------------------------------

        # Whitelist of text columns that are allowed to be updated
        allowed_fields = [
            "agent_type", "company_id", "company_position", "company_license_number",
            "personal_license_number", "license_issuing_authority", "country", "state",
            "city", "address_city", "address_postal_code", "contact_number", "email",
            "experience_years", "specialization", "bio", "linkedin", "instagram",
            "facebook", "x_account", "personal_website" , "daily_booking_limit"
        ]

        for field in allowed_fields:
            if field in request.form:
                set_parts.append(f"{field} = %s")
                values.append(request.form.get(field))
        
        # If nothing is being updated (no text fields and no new image), return an error.
        if not set_parts:
            return jsonify(error="No fields to update were provided."), 400

        # Add the agent_id for the WHERE clause
        values.append(agent_id)

        # Construct and execute the final UPDATE query
        query = f"UPDATE agents SET {', '.join(set_parts)} WHERE agent_id = %s"
        cursor.execute(query, tuple(values))

        if cursor.rowcount > 0:
            # Only save the new file if the database update was successful
            if file_to_save:
                file_to_save.save(save_path)
            
            con.commit()
            # Return the new URL if it was generated
            response = {"message": "Agent profile updated successfully"}
            if new_profile_picture_url:
                response["profile_picture_url"] = new_profile_picture_url
            return jsonify(response), 200
        else:
            return jsonify(error="Agent not found, or no data was changed."), 404

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /update_agent: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()





# In routes/auth.py

# In routes/auth.py

@auth_bp.route("/properties/search", methods=["POST"])
def search_properties():
    """
    A powerful and flexible endpoint for searching properties with multiple filters,
    sorting, and pagination. Featured properties are ranked first by default.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        print(data)
        if not data: data = {}

        # ... (all your filter logic is excellent, no changes needed there) ...
        conditions = ["p.is_deleted = FALSE"]
        values = []
        listing_type = data.get("listing_type")
        if listing_type and listing_type.lower() in ['sale', 'rent']:
            conditions.append("p.status = %s")
            values.append(listing_type.lower())
        text_filters = ["city", "state", "country", "property_type", "title"]
        for field in text_filters:
            value = data.get(field)
            if value and str(value).strip():
                conditions.append(f"p.{field} LIKE %s")
                values.append(f"%{str(value).strip()}%")
        bedrooms = data.get("bedrooms")
        if bedrooms and str(bedrooms).strip():
            try:
                conditions.append("p.bedrooms = %s")
                values.append(int(bedrooms))
            except (ValueError, TypeError): pass
        range_filters = {
            "min_price": "p.price >= %s", "max_price": "p.price <= %s",
            "min_bedrooms": "p.bedrooms >= %s", "max_bedrooms": "p.bedrooms <= %s",
            "min_bathrooms": "p.bathrooms >= %s", "max_bathrooms": "p.bathrooms <= %s",
            "min_area_sqft": "p.area_sqft >= %s", "max_area_sqft": "p.area_sqft <= %s"
        }
        for key, condition_str in range_filters.items():
            value = data.get(key)
            if value and str(value).strip():
                try:
                    conditions.append(condition_str)
                    values.append(float(value))
                except (ValueError, TypeError): pass
        
        where_clause = " WHERE " + " AND ".join(conditions)

        sort_by = data.get("sort_by", "default_rank")
        sort_order = data.get("sort_order", "desc").lower()
        limit = int(data.get("limit", 20))
        offset = int(data.get("offset", 0))

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        count_query = f"SELECT COUNT(DISTINCT p.property_id_1) AS total_count FROM properties p {where_clause}" # Also good practice to count by primary key
        cursor.execute(count_query, tuple(values))
        total_count = cursor.fetchone()['total_count']

        # --- THE FIX IS IN THIS QUERY STRING ---
        data_query = f"""
            SELECT p.*, GROUP_CONCAT(i.image_url) AS images
            FROM properties p LEFT JOIN property_images i ON p.property_id = i.property_id
            {where_clause}
            GROUP BY p.property_id_1  
            ORDER BY p.is_featured DESC, p.created_at DESC
            LIMIT %s OFFSET %s
        """
        
        data_values = values + [limit, offset]
        cursor.execute(data_query, tuple(data_values))
        properties = cursor.fetchall()

        for prop in properties:
            prop['images'] = prop['images'].split(',') if prop['images'] else []
            prop['is_featured'] = bool(prop['is_featured'])

        print(properties)

        return jsonify(total_count=total_count, properties=properties), 200

    except ValueError:
        return jsonify(error="Invalid number format for a filter parameter."), 400
    except Exception as e:
        logging.error(f"Error in /properties/search: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()




# In routes/auth.py

# Make sure these are imported at the top of your file



# Initialize the client (assuming you have OPENAI_API_KEY in your .env)



























import uuid
from datetime import datetime, timedelta
from flask import request, jsonify, render_template_string, current_app, url_for
from flask_mail import Message

# ---------------------------------------------------------
# ROUTE 1: REQUEST PASSWORD RESET (User enters email)
# ---------------------------------------------------------
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    con = None
    cursor = None
    try:
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify(error="Email is required"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # 1. Check if user exists
        cursor.execute("SELECT user_id, name FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            # Security: return 200 to prevent email enumeration
            return jsonify(message="If an account exists, a reset link has been sent."), 200

        # 2. Generate Token and Expiry (1 Hour)
        token = str(uuid.uuid4())
        expiration = datetime.now() + timedelta(hours=1)

        # 3. Save to Database
        cursor.execute(
            "UPDATE users SET reset_token = %s, reset_token_expires = %s WHERE user_id = %s",
            (token, expiration, user['user_id'])
        )
        con.commit()

        # 4. Create the Link
        # This builds the URL dynamically based on where your API is hosted
        reset_link = f"{request.host_url}auth/reset-page/{token}"

        # 5. Send Email via Mailjet
        msg = Message(
            subject="Reset Your Password",
            recipients=[email],
            body=f"Hello {user['name']},\n\nClick here to reset your password: {reset_link}",
            html=f"""
                <h3>Password Reset Request</h3>
                <p>Hello {user['name']},</p>
                <p>You requested to reset your password. Click the link below to set a new one:</p>
                <p><a href='{reset_link}' style='background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>Reset Password</a></p>
                <p>This link expires in 1 hour.</p>
            """
        )
        
        # Get the mail instance from the running app
        mail = current_app.extensions.get('mail')
        mail.send(msg)

        logging.info(f"Password reset email sent to {email}")
        return jsonify(message="If an account exists, a reset link has been sent."), 200

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /forgot-password: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


# ---------------------------------------------------------
# ROUTE 2: THE RESET PAGE (HTML Interface)
# User clicks the email link -> this page opens -> they type new pass
# ---------------------------------------------------------
@auth_bp.route("/reset-page/<token>", methods=["GET"])
def reset_password_page(token):
    # This serves a simple HTML page directly from the API.
    # It contains JavaScript to send the new password back to the API.
    submit_url = url_for('auth.reset_password_process')
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reset Password</title>
        <style>
            body {{ font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .card {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 320px; text-align: center; }}
            input {{ width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }}
            button {{ width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin-top: 10px;}}
            button:hover {{ background: #0056b3; }}
            .message {{ margin-top: 20px; font-size: 14px; }}
            .error {{ color: #dc3545; }}
            .success {{ color: #28a745; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>New Password</h2>
            <p>Enter your new password below.</p>
            <input type="password" id="new_pass" placeholder="New Password" required>
            <input type="password" id="confirm_pass" placeholder="Confirm Password" required>
            <button onclick="submitPassword()">Reset Password</button>
            <div id="message" class="message"></div>
        </div>

        <script>
            async function submitPassword() {{
                const p1 = document.getElementById('new_pass').value;
                const p2 = document.getElementById('confirm_pass').value;
                const msg = document.getElementById('message');

                if (!p1 || !p2) {{ msg.innerText = "Please fill in all fields"; msg.className = "message error"; return; }}
                if (p1 !== p2) {{ msg.innerText = "Passwords do not match"; msg.className = "message error"; return; }}

                msg.innerText = "Processing...";
                msg.className = "message";

                try {{
                    // UPDATED: We use the variable submit_url here
                    const response = await fetch('{submit_url}', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ token: '{token}', new_password: p1 }})
                    }});
                    
                    const data = await response.json();
                    
                    if (response.ok) {{
                        msg.innerText = "Success! Password changed.";
                        msg.className = "message success";
                    }} else {{
                        msg.innerText = data.error || "Failed to reset.";
                        msg.className = "message error";
                    }}
                }} catch (e) {{
                    msg.innerText = "Network error occurred.";
                    msg.className = "message error";
                    console.error(e);
                }}
            }}
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)


# ---------------------------------------------------------
# ROUTE 3: PROCESS THE RESET (Database Update)
# ---------------------------------------------------------
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password_process():
    con = None
    cursor = None
    try:
        data = request.get_json()
        token = data.get("token")
        new_password = data.get("new_password")

        if not token or not new_password:
            return jsonify(error="Missing token or password"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        # 1. Verify Token and Expiry
        now = datetime.now()
        query = "SELECT user_id FROM users WHERE reset_token = %s AND reset_token_expires > %s"
        cursor.execute(query, (token, now))
        user = cursor.fetchone()

        if not user:
            return jsonify(error="Invalid or expired token. Please request a new link."), 400

        # 2. Update Password and Clear Token
        # NOTE: This saves the password in plain text to match your existing login system.
        update_query = """
            UPDATE users 
            SET password_hash = %s, reset_token = NULL, reset_token_expires = NULL 
            WHERE user_id = %s
        """
        cursor.execute(update_query, (new_password, user['user_id']))
        con.commit()

        logging.info(f"Password successfully reset for user_id {user['user_id']}")
        return jsonify(message="Password reset successfully"), 200

    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /reset-password: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()



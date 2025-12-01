import pymysql.cursors
import logging
import os
import json
from flask import Blueprint, request, jsonify, current_app
from app import getConnection  # Your function to get a DB connection
from openai import OpenAI
from dotenv import load_dotenv
from decimal import Decimal # Import the Decimal type

# --- INITIAL SETUP ---

load_dotenv()
client = OpenAI()
chat_bp = Blueprint('chat', __name__)

# --- CUSTOM JSON ENCODER ---
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(CustomJSONEncoder, self).default(obj)

# --- TOOL DEFINITIONS ---

ALL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "find_properties",
            "description": "Search for real estate properties based on criteria like city, price, type, or bedrooms. This is the primary function for finding listings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city to search in, e.g., Kuala Lumpur, Malacca City"},
                    "state": {"type": "string", "description": "The state, e.g., Selangor, Perak"},
                    "property_type": {"type": "string", "description": "e.g., apartment, house, condo, villa"},
                    "min_price": {"type": "number", "description": "The minimum price"},
                    "max_price": {"type": "number", "description": "The maximum price"},
                    "bedrooms": {"type": "number", "description": "The minimum number of bedrooms"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_total_property_count",
            "description": "Gets the total number of properties available in the database. Use this when the user asks for a total count, like 'how many properties do you have?'.",
            "parameters": {"type": "object", "properties": {}},
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_favorites",
            "description": "Adds a specific property to the logged-in user's favorites list. This action requires the user to be logged in and to provide a property_id.",
            "parameters": {
                "type": "object",
                "properties": {"property_id": {"type": "number", "description": "The ID of the property to add to favorites."}},
                "required": ["property_id"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "request_appointment",
            "description": "Request an appointment to view a specific property on a given date. This action requires the user to be logged in and to provide a property_id and a date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "property_id": {"type": "number", "description": "The ID of the property for the appointment."},
                    "appointment_date": {"type": "string", "description": "The desired date in YYYY-MM-DD format, e.g., 2025-11-28."},
                },
                "required": ["property_id", "appointment_date"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_my_appointments",
            "description": "Fetches a list of the logged-in user's appointments, including their status (pending, confirmed, etc.). This action requires the user to be logged in.",
            "parameters": {"type": "object", "properties": {}},
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_my_favorites",
            "description": "Fetches the logged-in user's list of favorite properties. This action requires the user to be logged in.",
            "parameters": {"type": "object", "properties": {}},
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_appointment",
            "description": "Cancels a PENDING appointment. The user must be logged in and provide the appointment ID. This cannot be used for confirmed appointments.",
            "parameters": {
                 "type": "object",
                "properties": {"appointment_id": {"type": "number", "description": "The ID of the PENDING appointment to cancel."}},
                "required": ["appointment_id"],
            },
        }
    }
]

# --- MAIN CHATBOT ENDPOINT ---

@chat_bp.route("/chat", methods=["POST"])
def handle_chat():
    data = request.get_json()
    user_query = data.get("message")
    user_id = data.get("user_id")
    history = data.get("history", [])
    print(data)

    if not user_query:
        return jsonify(error="A 'message' is required."), 400

    try:
        messages = [
            # <-- THIS IS THE CORRECTED SYSTEM PROMPT -->
            {"role": "system", "content": "You are RealtyBot, a helpful real estate assistant. Your main job is to understand the user's request and choose the best tool to fulfill it. If a user's request matches a tool, you should call it. The system's backend will handle all authentication and will return an error if the user is not logged in for a protected action. When a query is too vague (e.g., 'suggest properties'), ask clarifying questions first (e.g., 'What city are you interested in?')."},
            *history,
            {"role": "user", "content": user_query}
        ]

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            tools=ALL_TOOLS,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)
            function_data_payload = None

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                function_response = {"status": "error", "message": f"Function '{function_name}' is not defined."}

                if function_name == "find_properties":
                    function_response = _find_properties_db(function_args)
                elif function_name == "get_total_property_count":
                    function_response = _get_total_property_count_db()
                elif user_id: # Your backend code correctly handles the check here
                    if function_name == "add_to_favorites":
                        function_response = _add_to_favorites_db(user_id, function_args.get("property_id"))
                    elif function_name == "request_appointment":
                        function_response = _request_appointment_db(user_id, function_args.get("property_id"), function_args.get("appointment_date"))
                    elif function_name == "get_my_appointments":
                        function_response = _get_my_appointments_db(user_id)
                    elif function_name == "get_my_favorites":
                        function_response = _get_my_favorites_db(user_id)
                    elif function_name == "cancel_appointment":
                        function_response = _cancel_appointment_db(user_id, function_args.get("appointment_id"))
                else:
                    function_response = {"status": "error", "message": "This action requires you to be logged in. Please log in to continue."}

                function_data_payload = function_response
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response, cls=CustomJSONEncoder),
                })

            second_response = client.chat.completions.create(model="gpt-4-turbo-preview", messages=messages)
            ai_summary_text = second_response.choices[0].message.content

            print(ai_summary_text)

            return jsonify(reply_text=ai_summary_text, data=function_data_payload)
        else:
            ai_response_content = response_message.content
            return jsonify(reply_text=ai_response_content, data=None)

    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}", exc_info=True)
        return jsonify(error="An error occurred while processing your request."), 500


# --- DATABASE HELPER FUNCTIONS ---

def _find_properties_db(args):
    """
    Searches for properties, checking both city and state in a case-insensitive manner.
    """
    con = None
    try:
        con = getConnection()
        conditions = []
        values = []

        # --- THIS IS THE CRITICAL FIX ---
        # If a location is provided, search it against BOTH city and state
        location = args.get("city") or args.get("state")
        if location:
            # Use TRIM() to remove leading/trailing spaces and LOWER() for case-insensitivity
            conditions.append("(LOWER(TRIM(p.city)) LIKE %s OR LOWER(TRIM(p.state)) LIKE %s)")
            search_term = f"%{location.lower().strip()}%"
            values.extend([search_term, search_term])
        # ------------------------------------

        if args.get("property_type"):
            conditions.append("LOWER(TRIM(p.property_type)) = %s")
            values.append(args['property_type'].lower().strip())
            
        if args.get("min_price"):
            conditions.append("p.price >= %s")
            values.append(args['min_price'])
            
        if args.get("max_price"):
            conditions.append("p.price <= %s")
            values.append(args['max_price'])
            
        if args.get("bedrooms"):
            conditions.append("p.bedrooms >= %s")
            values.append(args['bedrooms'])
        
        query = "SELECT p.property_id, p.title, p.description, p.price, p.city, p.state, p.property_type, p.bedrooms FROM properties p"
        if conditions:
            query += " WHERE " + " AND ".join(conditions) + "AND is_deleted = 0"
        query += " LIMIT 5;"
        
        cursor = con.cursor()
        cursor.execute(query, tuple(values))
        return cursor.fetchall()
    finally:
        if con: con.close()

def _get_total_property_count_db():
    """Counts the total number of properties in the database."""
    con = None
    try:
        con = getConnection()
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) AS total_count FROM properties")
        result = cursor.fetchone()
        return result if result else {"total_count": 0}
    finally:
        if con: con.close()

def _add_to_favorites_db(user_id, property_id):
    con = None
    try:
        if not property_id: return {"status": "error", "message": "Please specify which property you'd like to favorite by its ID."}
        con = getConnection()
        cursor = con.cursor()
        query = "INSERT IGNORE INTO favorites (user_id, property_id) VALUES (%s, %s)"
        cursor.execute(query, (user_id, property_id))
        if cursor.rowcount > 0:
            con.commit()
            return {"status": "success", "message": f"Done! I've added property ID {property_id} to your favorites."}
        else:
            return {"status": "success", "message": f"It looks like property ID {property_id} is already in your favorites."}
    finally:
        if con: con.close()

def _request_appointment_db(user_id, property_id, appointment_date):
    con = None
    try:
        if not all([property_id, appointment_date]):
            return {"status": "error", "message": "To book an appointment, please provide the property ID and the date."}
        con = getConnection()
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) AS active_count FROM appointments WHERE user_id = %s AND property_id = %s AND status IN ('pending', 'confirmed')", (user_id, property_id))
        if cursor.fetchone()['active_count'] > 0:
            return {"status": "error", "message": "You already have an active appointment for this property."}
        cursor.execute("SELECT agent_id FROM properties WHERE property_id = %s", (property_id,))
        agent_id = cursor.fetchone()['agent_id']
        cursor.execute("INSERT INTO appointments (user_id, property_id, agent_id, appointment_date, status) VALUES (%s, %s, %s, %s, 'pending')", (user_id, property_id, agent_id, appointment_date))
        con.commit()
        return {"status": "success", "message": f"Great! Your request to view property {property_id} on {appointment_date} has been sent to the agent for confirmation."}
    except Exception as e:
        return {"status": "error", "message": f"I couldn't book the appointment. The system reported an error: {str(e)}"}
    finally:
        if con: con.close()

def _get_my_appointments_db(user_id):
    con = None
    try:
        con = getConnection()
        query = "SELECT p.title AS property_title, DATE_FORMAT(a.appointment_date, '%%Y-%%m-%%d') AS appointment_date, TIME_FORMAT(a.appointment_time, '%%H:%%i') AS appointment_time, a.status FROM appointments a JOIN properties p ON a.property_id = p.property_id WHERE a.user_id = %s ORDER BY a.appointment_date DESC"
        cursor = con.cursor()
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        if not results:
            return {"message": "You don't seem to have any appointments scheduled."}
        return results
    finally:
        if con: con.close()

def _get_my_favorites_db(user_id):
    con = None
    try:
        con = getConnection()
        query = "SELECT p.property_id, p.title, p.price, p.city FROM favorites f JOIN properties p ON f.property_id = p.property_id WHERE f.user_id = %s"
        cursor = con.cursor()
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        if not results:
            return {"message": "You haven't added any properties to your favorites yet."}
        return results
    finally:
        if con: con.close()

def _cancel_appointment_db(user_id, appointment_id):
    con = None
    try:
        if not appointment_id: return {"status": "error", "message": "Please tell me the ID of the appointment you wish to cancel."}
        con = getConnection()
        cursor = con.cursor()
        query = "DELETE FROM appointments WHERE appointment_id = %s AND user_id = %s AND status = 'pending'"
        cursor.execute(query, (appointment_id, user_id))
        if cursor.rowcount > 0:
            con.commit()
            return {"status": "success", "message": f"Appointment {appointment_id} has been successfully cancelled."}
        else:
            return {"status": "error", "message": "I couldn't cancel that appointment. It might not exist, or it may have already been confirmed by the agent."}
    finally:
        if con: con.close()





# In routes/chatbot.py

# Your existing imports should be here:
# import pymysql.cursors
# import logging
# import os
# import json
# from flask import Blueprint, request, jsonify
# from app import getConnection
# from openai import OpenAI
# from dotenv import load_dotenv
# from decimal import Decimal

# Your existing Blueprint, client, and CustomJSONEncoder should already be here
# load_dotenv()
# client = OpenAI()
# chat_bp = Blueprint('chat', __name__)
# class CustomJSONEncoder...


# --- START: MALAYSIAN NORMALIZATION DATA AND FUNCTION ---

STATE_MAP = { "kualalumpur": "Kuala Lumpur", "kl": "Kuala Lumpur", "labuan": "Labuan", "putrajaya": "Putrajaya", "johor": "Johor", "kedah": "Kedah", "kelantan": "Kelantan", "melaka": "Melaka", "malacca": "Melaka", "negerisembilan": "Negeri Sembilan", "pahang": "Pahang", "perak": "Perak", "perlis": "Perlis", "pulaupinang": "Pulau Pinang", "penang": "Pulau Pinang", "sabah": "Sabah", "sarawak": "Sarawak", "selangor": "Selangor", "sgor": "Selangor", "terengganu": "Terengganu", }
CITY_MAP = { "shahalam": "Shah Alam", "petalingjaya": "Petaling Jaya", "pj": "Petaling Jaya", "subangjaya": "Subang Jaya", "subang": "Subang Jaya", "klang": "Klang", "cyberjaya": "Cyberjaya", "puchong": "Puchong", "damansara": "Damansara", "cheras": "Cheras", "bangi": "Bangi", "kajang": "Kajang", "rawang": "Rawang", "selayang": "Selayang", "ampang": "Ampang", "montkiara": "Mont Kiara", "bangsar": "Bangsar", "hartamas": "Sri Hartamas", "srihartamas": "Sri Hartamas", "ttdi": "Taman Tun Dr Ismail", "kepong": "Kepong", "sentul": "Sentul", "bukitjalil": "Bukit Jalil", "klcc": "KLCC", "georgetown": "George Town", "butterworth": "Butterworth", "bukitmertajam": "Bukit Mertajam", "bayanlepas": "Bayan Lepas", "johorbahru": "Johor Bahru", "jb": "Johor Bahru", "iskandarputeri": "Iskandar Puteri", "ipoh": "Ipoh", "kotakinabalu": "Kota Kinabalu", "kk": "Kota Kinabalu", "kuching": "Kuching", "kuantan": "Kuantan", "seremban": "Seremban", }
PROPERTY_TYPE_MAP = { "condo": "Condominium", "condominium": "Condominium", "apartment": "Apartment", "flat": "Apartment", "serviceapartment": "Serviced Residence", "servicedresidence": "Serviced Residence", "terrace": "Terrace", "terracehouse": "Terrace", "linkhouse": "Terrace", "bungalow": "Bungalow", "semid": "Semi-Detached", "semidetached": "Semi-Detached", "house": "House" }
STATUS_MAP = {"forsale": "sale", "sale": "sale", "buy": "sale", "forrent": "rent", "rent": "rent", "lease": "rent"}

def normalize_filters(filters):
    """
    Cleans and standardizes filter values using our Malaysian data maps.
    """
    normalized = {}
    if not isinstance(filters, dict): return {} # Safety check
    
    city = filters.get("city")
    if city and isinstance(city, str):
        normalized["city"] = CITY_MAP.get(city.lower().replace(" ", ""), city.title())

    state = filters.get("state")
    if state and isinstance(state, str):
        normalized["state"] = STATE_MAP.get(state.lower().replace(" ", ""), state.title())

    prop_type = filters.get("property_type")
    if prop_type and isinstance(prop_type, str):
        normalized["property_type"] = PROPERTY_TYPE_MAP.get(prop_type.lower().replace(" ", ""), prop_type.title())

    status = filters.get("status")
    if status and isinstance(status, str):
        lookup_key = status.lower().replace(" ", "")
        if lookup_key in STATUS_MAP:
            normalized["status"] = STATUS_MAP[lookup_key]

    numeric_keys = ["min_price", "max_price", "min_bedrooms", "max_bedrooms", "min_bathrooms", "max_bathrooms"]
    for key in numeric_keys:
        if key in filters and filters[key] is not None:
            try:
                normalized[key] = int(filters[key])
            except (ValueError, TypeError):
                pass # Ignore non-numeric values
            
    return normalized

# --- END: NORMALIZATION LOGIC ---


# --- NEW PARSE SEARCH ENDPOINT ---

@chat_bp.route("/parse_search_query", methods=["POST"])
def parse_search_query():
    """
    Translates a natural language query, normalizes it, and then directly
    calls the /properties/search endpoint to return a list of properties.
    """
    try:
        data = request.get_json()
        user_query = data.get("query")
        if not user_query:
            return jsonify(error="A 'query' string is required."), 400

        # Define tools for OpenAI
        tools = [
            { "type": "function", "function": { "name": "generate_search_filters", "description": "Generates structured filters from a user's natural language query.", "parameters": { "type": "object", "properties": { "city": {"type": "string"}, "state": {"type": "string"}, "property_type": {"type": "string"}, "min_price": {"type": "number"}, "max_price": {"type": "number"}, "min_bedrooms": {"type": "number"}, "max_bedrooms": {"type": "number"}, "min_bathrooms": {"type": "number"}, "max_bathrooms": {"type": "number"}, "status": {"type": "string"} }, "required": [] } } }
        ]
        
        # Step 1: Call OpenAI to get raw filters
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert real estate search query parser. Extract search filters from the user's text and call the generate_search_filters function. Do not include keys for values that are not mentioned."},
                {"role": "user", "content": user_query}
            ],
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "generate_search_filters"}},
        )
        search_filters_raw = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        
        # Step 2: Normalize the filters
        normalized_filters = normalize_filters(search_filters_raw)
        logging.info(f"Normalized filters for internal search: {normalized_filters}")

        # Step 3: Call the /properties/search endpoint internally
        with current_app.test_client() as app_client: # RENAMED to app_client
            search_response = app_client.post( # USE new name
                '/properties/search',
                json=normalized_filters,
                headers={'Content-Type': 'application/json'}
            )
            search_data = search_response.get_json()

        if search_response.status_code != 200:
            return jsonify(search_data), search_response.status_code

        # Step 4: Return the final property list
        return jsonify(search_data), 200

    except Exception as e:
        logging.error(f"Error in /parse_search_query: {e}", exc_info=True)
        return jsonify(error="An error occurred while processing your search query."), 500

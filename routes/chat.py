import pymysql.cursors
import logging
from flask import Blueprint, request, jsonify
from app import getConnection

# Renamed to match the alias in app.py for clarity
chat_system = Blueprint('chat_system', __name__)

# --- ENDPOINT 1: Get a list of all of a user's conversations ---

@chat_system.route("/my_conversations", methods=["POST"])
def get_my_conversations():
    """
    Fetches a list of all conversations for a user, including the agent's name
    and the last message sent.
    """
    con = None
    cursor = None # Initialize cursor

    try:
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify(error="user_id is required"), 400

        con = getConnection()
        # FIX: Use a DictCursor to get dictionary results
        cursor = con.cursor(pymysql.cursors.DictCursor)
        
        query = """
            SELECT
                c.conversation_id,
                c.agent_id,
                DATE_FORMAT(c.updated_at, '%%Y-%%m-%%d %%H:%%i') AS last_activity,
                u.name AS agent_name,
                ag.profile_picture AS agent_profile_picture,
                (SELECT message_content FROM chat_messages cm 
                 WHERE cm.conversation_id = c.conversation_id 
                 ORDER BY cm.sent_at DESC LIMIT 1) AS last_message
            FROM
                conversations c
            JOIN
                agents ag ON c.agent_id = ag.agent_id
            JOIN
                users u ON ag.user_id = u.user_id
            WHERE
                c.user_id = %s
            ORDER BY
                c.updated_at DESC;
        """
        
        cursor.execute(query, (user_id,))
        conversations = cursor.fetchall()
        
        return jsonify(conversations=conversations), 200

    except Exception as e:
        logging.error(f"Error in /my_conversations: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        # FIX: Ensure both cursor and connection are closed
        if cursor:
            cursor.close()
        if con: 
            con.close()


# --- ENDPOINT 2: Get the message history for a single conversation ---

@chat_system.route("/conversation_history", methods=["POST"])
def get_conversation_history():
    """
    Fetches all messages for a specific conversation.
    Includes a security check and a flag to identify the sender.
    """
    con = None
    cursor = None

    try:
        data = request.get_json()
        user_id = data.get("user_id")
        conversation_id = data.get("conversation_id")
        if not all([user_id, conversation_id]):
            return jsonify(error="user_id and conversation_id are required"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT agent_id FROM conversations WHERE conversation_id = %s AND user_id = %s", (conversation_id, user_id))
        if not cursor.fetchone():
            return jsonify(error="Access denied or conversation not found"), 403

        query = """
            SELECT
                message_id, sender_user_id, message_content,
                DATE_FORMAT(sent_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS sent_at,
                (CASE WHEN sender_user_id = %s THEN 1 ELSE 0 END) AS is_sender_self
            FROM chat_messages
            WHERE conversation_id = %s
            ORDER BY sent_at ASC;
        """
        cursor.execute(query, (user_id, conversation_id))
        messages = cursor.fetchall()

        for message in messages:
            message['is_sender_self'] = bool(message['is_sender_self'])

        print(messages)
        
        return jsonify(messages=messages), 200

    except Exception as e:
        logging.error(f"Error in /conversation_history: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor:
            cursor.close()
        if con: 
            con.close()


# --- ENDPOINT 3: Send a new message ---

@chat_system.route("/send_message", methods=["POST"])
def send_message():
    """
    Sends a new message. Handles both starting a new conversation and replying to an existing one.
    """
    con = None
    cursor = None

    try:
        data = request.get_json()
        sender_user_id = data.get("user_id")
        message_content = data.get("message_content")
        agent_id = data.get("agent_id")
        conversation_id = data.get("conversation_id")

        print(data)

        if not sender_user_id or not message_content:
            return jsonify(error="user_id and message_content are always required"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor) # Using DictCursor for consistency

        if conversation_id:
            cursor.execute("SELECT conversation_id FROM conversations WHERE conversation_id = %s", (conversation_id,))
            if not cursor.fetchone():
                return jsonify(error="Conversation not found"), 404
            logging.info(f"Adding message from user {sender_user_id} to existing conversation {conversation_id}")

        elif agent_id:
            buyer_user_id = sender_user_id
            cursor.execute("SELECT conversation_id FROM conversations WHERE user_id = %s AND agent_id = %s", (buyer_user_id, agent_id))
            existing_convo = cursor.fetchone()
            if existing_convo:
                conversation_id = existing_convo['conversation_id']
                logging.info(f"Found existing conversation: {conversation_id}")
            else:
                cursor.execute("INSERT INTO conversations (user_id, agent_id) VALUES (%s, %s)", (buyer_user_id, agent_id))
                conversation_id = cursor.lastrowid
                logging.info(f"Created new conversation thread with ID: {conversation_id}")
        else:
            return jsonify(error="Either conversation_id (for replies) or agent_id (to start a new chat) is required"), 400
        
        query_insert = "INSERT INTO chat_messages (conversation_id, sender_user_id, message_content) VALUES (%s, %s, %s)"
        cursor.execute(query_insert, (conversation_id, sender_user_id, message_content))
        message_id = cursor.lastrowid
        
        con.commit()
        
        return jsonify(message="Message sent successfully", message_id=message_id, conversation_id=conversation_id), 201
    
    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error in /send_message: {e}", exc_info=True)
        return jsonify(error="An internal server error occurred"), 500
    finally:
        if cursor:
            cursor.close()
        if con: 
            con.close()
import pymysql.cursors
import logging
import stripe
import os
from flask import Blueprint, request, jsonify
from app import getConnection
from flask_cors import CORS

billing_bp = Blueprint('billing', __name__)
logging.basicConfig(level=logging.INFO)

# Configure Stripe with your secret key from the .env file
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


# --- NEW SUCCESS AND CANCEL REDIRECT ENDPOINTS ---

from flask import Blueprint, request, render_template_string, url_for, redirect
import stripe
import logging

# Ensure you have your blueprint defined
# billing_bp = Blueprint('billing', __name__)

@billing_bp.route("/payment-success", methods=["GET"])
def payment_success():
    """
    Landing page for successful payments.
    """
    session_id = request.args.get('session_id')
    
    # 1. Generate the correct Home/Dashboard URL dynamically
    # Replace 'main.dashboard' with the actual function name of your dashboard route
    try:
        dashboard_url = url_for('main.dashboard') 
    except:
        # Fallback if route name is wrong, prevents 500 error
        dashboard_url = "http://165.227.220.96:8080/dash" 

    # 2. Payment Verification Logic
    if session_id:
        try:
            # Retrieve the session from Stripe
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            
            if checkout_session.payment_status == "paid":
                # IMPORTANT: In a real app, you must check your database here.
                # Check: Has this session_id already been fulfilled?
                # if not is_order_fulfilled(session_id):
                #     fulfill_order(session_id, checkout_session.payment_intent)
                
                # For now, we proceed with your existing logic:
                fulfill_order(session_id, checkout_session.payment_intent)
                
        except Exception as e:
            # Log the error but allow the user to see the success page
            # (The webhook should handle the actual fulfillment if this fails)
            logging.error(f"Error during backup verification on success page: {e}")

    # 3. Return the HTML (using f-string to inject the dashboard_url)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Payment Successful</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            body {{
                background: linear-gradient(135deg, #f0f9f0 0%, #e6f3ff 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            
            .container {{
                max-width: 450px;
                width: 100%;
                background: white;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                padding: 40px 30px;
                text-align: center;
            }}
            
            .success-icon {{
                position: relative;
                display: inline-block;
                margin-bottom: 25px;
            }}
            
            .icon-circle {{
                width: 80px;
                height: 80px;
                background: #d4edda;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto;
            }}
            
            .check-icon {{
                color: #28a745;
                font-size: 40px;
            }}
            
            .star-badge {{
                position: absolute;
                top: -5px;
                right: -5px;
                width: 24px;
                height: 24px;
                background: #ffc107;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 12px;
            }}
            
            h1 {{
                color: #333;
                font-size: 28px;
                margin-bottom: 15px;
                font-weight: 700;
            }}
            
            .message {{
                color: #666;
                margin-bottom: 10px;
                line-height: 1.5;
            }}
            
            .credits {{
                color: #28a745;
                font-weight: 600;
                margin-bottom: 30px;
            }}
            
            .buttons {{
                display: flex;
                flex-direction: column;
                gap: 15px;
                margin-top: 20px;
            }}
            
            @media (min-width: 480px) {{
                .buttons {{
                    flex-direction: row;
                }}
            }}
            
            .btn {{
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                padding: 14px 20px;
                border-radius: 10px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                border: none;
                font-size: 16px;
                text-decoration: none;
            }}
            
            .btn-home {{
                background: #b48b5e;
                color: white;
            }}
            
            .btn-home:hover {{
                background: #996e41;
            }}
            
            .additional-info {{
                margin-top: 25px;
                padding-top: 25px;
                border-top: 1px solid #eee;
                color: #777;
                font-size: 14px;
            }}
            
            .additional-info p {{
                margin-bottom: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Success Icon -->
            <div class="success-icon">
                <div class="icon-circle">
                    <i class="fas fa-check-circle check-icon"></i>
                </div>
                <div class="star-badge">
                    <i class="fas fa-star"></i>
                </div>
            </div>
            
            <!-- Success Message -->
            <h1>Payment Successful!</h1>
            <p class="message">
                Thank you for your purchase. Your payment has been processed successfully.
            </p>
            <p class="credits">
                Credits have been added to your account.
            </p>
            
            <!-- Action Buttons -->
            <div class="buttons">
                <a href="{dashboard_url}" class="btn btn-home">
                    <i class="fas fa-home"></i>
                    Go Home
                </a>
            </div>
            
            <!-- Additional Information -->
            <div class="additional-info">
                <p>If you have any questions, contact our support team.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_content), 200

# In routes/billing.py

@billing_bp.route("/payment-cancelled", methods=["POST"])
def payment_cancelled():
    """
    Handles the redirect when a user cancels a payment.
    Updates the corresponding invoice status to 'cancelled'.
    """
    session_id = request.args.get('session_id')
    print(session_id)
    
    # If a session_id is provided in the URL, update our database
    if session_id:
        con = None
        cursor = None
        try:
            con = getConnection()
            cursor = con.cursor()
            
            # Find the pending invoice and update its status to 'cancelled'
            cursor.execute(
                "UPDATE invoices SET status = 'cancelled' WHERE stripe_session_id = %s AND status = 'pending'",
                (session_id,)
            )
            con.commit()
            
            if cursor.rowcount > 0:
                logging.info(f"Marked invoice for session {session_id} as 'cancelled'.")
        except Exception as e:
            logging.error(f"Error updating invoice to cancelled: {e}", exc_info=True)
            if con: con.rollback()
        finally:
            if cursor: cursor.close()
            if con: con.close()

    # Always return a user-friendly message
    return """
        <h1>Payment Cancelled</h1>
        <p>Your payment process was cancelled. You have not been charged.</p>
    """, 200


# --- EXISTING BILLING ENDPOINTS ---

@billing_bp.route("/get_credit_plans", methods=["GET"])
def get_credit_plans():
    """
    Fetches a list of all ACTIVE credit plans available for purchase.
    """
    con = None
    cursor = None
    try:
        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT plan_id, plan_name, credits_amount, price, description FROM credit_plans WHERE is_active = TRUE ORDER BY price ASC")
        plans = cursor.fetchall()
        print(plans)
        return jsonify(credit_plans=plans), 200
    except Exception as e:
        logging.error(f"Error in /get_credit_plans: {e}", exc_info=True)
        return jsonify(error="please check all the details before Submitting"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


@billing_bp.route("/billing/create-checkout-session", methods=["POST"])
def create_checkout_session():
    """
    1. Creates a 'pending' invoice in our database.
    2. Creates a Stripe Checkout session linked to our invoice.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        plan_id = data.get("plan_id")
        agent_id = data.get("agent_id")

        print(data)
        if not plan_id or not agent_id:
            return jsonify(error="plan_id and agent_id are required"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT plan_name, price, credits_amount FROM credit_plans WHERE plan_id = %s AND is_active = TRUE", (plan_id,))
        plan = cursor.fetchone()
        if not plan:
            return jsonify(error="Credit plan not found or is not active."), 404

        cursor.execute(
            "INSERT INTO invoices (agent_id, status, credits_purchased, amount_paid) VALUES (%s, 'pending', %s, %s)",
            (agent_id, plan['credits_amount'], plan['price'])
        )
        invoice_id = cursor.lastrowid
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{ 'price_data': { 'currency': 'myr', 'product_data': { 'name': plan['plan_name'] }, 'unit_amount': int(plan['price'] * 100) }, 'quantity': 1 }],
            mode='payment',
            metadata={ 'agent_id': agent_id, 'plan_id': plan_id, 'invoice_id': invoice_id },
            # --- UPDATED URLS FOR TESTING ---
            success_url=f'http://165.227.220.96:5001/payment-success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'http://165.227.220.96:5001/payment-cancelled',
        )

        cursor.execute("UPDATE invoices SET stripe_session_id = %s WHERE invoice_id = %s", (session.id, invoice_id))
        con.commit()
        
        return jsonify(id=session.id)
    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error creating Stripe session: {e}", exc_info=True)
        return jsonify(error=str(e)), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


@billing_bp.route("/billing/webhook", methods=["POST"])
def stripe_webhook():
    """
    Listens for events from Stripe and calls the appropriate fulfillment function.
    Handles both successful and failed payments.
    """
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    if not webhook_secret:
        logging.error("Stripe webhook secret is not configured.")
        return 'Webhook secret not configured', 500
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return 'Invalid payload or signature', 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_ref = session.get('payment_intent')
        stripe_session_id = session.get('id')
        if stripe_session_id and payment_ref:
            fulfill_order(stripe_session_id, payment_ref)
        else:
            logging.error("Webhook (success) received with missing session_id or payment_intent")
    elif event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
        stripe_session_id = session.get('id')
        if stripe_session_id:
            handle_failed_payment(stripe_session_id)
        else:
            logging.error("Webhook (failure) received with missing session_id")
    else:
        logging.info(f"Received unhandled Stripe event type: {event['type']}")

    return jsonify(status='success'), 200


@billing_bp.route("/verify_payment_status", methods=["POST"])
def verify_payment_status():
    """
    Called by the frontend from the success page. Verifies a Stripe session
    and fulfills the order if the webhook has been missed or is delayed.
    """
    con = None
    cursor = None
    try:
        data = request.get_json()
        session_id = data.get("session_id")
        print(data)
        if not session_id:
            return jsonify(error="session_id is required"), 400

        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT status FROM invoices WHERE stripe_session_id = %s", (session_id,))
        invoice = cursor.fetchone()
        
        if invoice and invoice['status'] == 'paid':
            return jsonify(message="Payment already verified and credits added."), 208

        checkout_session = stripe.checkout.Session.retrieve(session_id)
        if checkout_session.payment_status == "paid":
            payment_ref = checkout_session.payment_intent
            success, message = fulfill_order(session_id, payment_ref)
            if success:
                return jsonify(message="Payment verified successfully. Credits have been added.")
            else:
                return jsonify(error=message), 500
        else:
            return jsonify(error="Payment not successful according to Stripe."), 402
    except Exception as e:
        logging.error(f"Error verifying payment: {e}", exc_info=True)
        return jsonify(error="An error occurred while verifying payment."), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()


def fulfill_order(stripe_session_id, payment_ref):
    """
    The centralized, idempotent function for fulfilling an order.
    Returns (True, "Success") or (False, "Error message").
    """
    con = None
    cursor = None
    try:
        con = getConnection()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM invoices WHERE stripe_session_id = %s AND status = 'pending'", (stripe_session_id,))
        invoice = cursor.fetchone()
        if not invoice:
            logging.warning(f"Fulfillment attempted for already processed or non-existent session: {stripe_session_id}")
            return (False, "Order already fulfilled or not found.")

        agent_id, credits_purchased = invoice['agent_id'], invoice['credits_purchased']
        
        cursor.execute("UPDATE invoices SET status = 'paid', payment_gateway_ref = %s WHERE invoice_id = %s", (payment_ref, invoice['invoice_id']))
        cursor.execute("UPDATE agents SET paid_credits = paid_credits + %s WHERE agent_id = %s", (credits_purchased, agent_id))
        
        description = f"Purchase of {credits_purchased} credits "
        cursor.execute("INSERT INTO transactions (agent_id, transaction_type, amount, description, reference_id) VALUES (%s, 'purchase', %s, %s, %s)", (agent_id, credits_purchased, description, invoice['invoice_id']))
        
        con.commit()
        logging.info(f"Successfully fulfilled order for invoice {invoice['invoice_id']} / session {stripe_session_id}.")
        return (True, "Success")
    except Exception as e:
        if con: con.rollback()
        logging.error(f"DATABASE ERROR during fulfillment: {e}", exc_info=True)
        return (False, "Database error during fulfillment.")
    finally:
        if cursor: cursor.close()
        if con: con.close()


def handle_failed_payment(stripe_session_id):
    """
    Updates the internal invoice status to 'failed' when a payment fails on Stripe.
    """
    con = None
    cursor = None
    try:
        con = getConnection()
        cursor = con.cursor()
        cursor.execute("UPDATE invoices SET status = 'failed' WHERE stripe_session_id = %s AND status = 'pending'", (stripe_session_id,))
        con.commit()
        if cursor.rowcount > 0:
            logging.info(f"Marked invoice for session {stripe_session_id} as 'failed'.")
    except Exception as e:
        if con: con.rollback()
        logging.error(f"Error handling failed payment: {e}", exc_info=True)
    finally:
        if cursor: cursor.close()
        if con: con.close()


@billing_bp.route("/my_transactions", methods=["POST"])
def get_my_transactions():
    """
    Fetches the transaction history for a specific agent.
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
        query = "SELECT transaction_id,transaction_number, transaction_type, amount, description, DATE_FORMAT(transaction_date, '%%Y-%%m-%%d %%H:%%i') AS transaction_date FROM transactions WHERE agent_id = %s ORDER BY transaction_date DESC"
        cursor.execute(query, (agent_id,))
        transactions = cursor.fetchall()
        print(transactions)
        return jsonify(transactions=transactions), 200
    except Exception as e:
        logging.error(f"Error in /my_transactions: {e}", exc_info=True)
        return jsonify(error="please check all the details before Submitting"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()





















from flask import Blueprint, request, jsonify
# import your db connection function here, e.g., from db import getConnection


@billing_bp.route("/get_transaction_detail", methods=["POST"])
def get_transaction_detail():
    tx_number = request.json.get("transaction_number")

    if not tx_number:
        return jsonify(error="transaction_number is required"), 400

    con = None
    cursor = None
    try:
        con = getConnection()
        cursor = con.cursor()

        query = """
            SELECT 
                t.transaction_id,
                t.transaction_number,
                t.transaction_date,
                t.transaction_type,
                t.amount AS credit_amount,
                t.description,
                i.invoice_id,
                i.invoice_number,
                i.amount_paid,
                i.status AS payment_status,
                i.payment_gateway_ref,
                i.created_at AS invoice_date
            FROM transactions t
            LEFT JOIN invoices i ON t.reference_id = i.invoice_id
            WHERE t.transaction_number = %s
        """

        cursor.execute(query, (tx_number,))
        row = cursor.fetchone()

        if not row:
            return jsonify(message="Transaction not found"), 404
            
        # --- FIX STARTS HERE ---
        # Since your DB returns a dict, we don't need zip().
        # We just rename 'row' to 'row_dict' for clarity.
        row_dict = row 
        # --- FIX ENDS HERE ---

        result = {
            "transaction_number": row_dict["transaction_number"],
            "date": row_dict["transaction_date"],
            "type": row_dict["transaction_type"],
            # Ensure we handle decimals correctly
            "credits": float(row_dict["credit_amount"]) if row_dict["credit_amount"] is not None else 0.0,
            "description": row_dict["description"],
            "invoice_details": None 
        }

        # Check for invoice_id (it will be None if this is a 'spend' transaction)
        if row_dict.get("invoice_id"):
            result["invoice_details"] = {
                "invoice_id": row_dict["invoice_id"],
                "invoice_number": row_dict["invoice_number"],
                "amount_paid": float(row_dict["amount_paid"]) if row_dict["amount_paid"] else 0.00,
                "status": row_dict["payment_status"],
                "gateway_ref": row_dict["payment_gateway_ref"],
                "created_at": row_dict["invoice_date"]
            }

        return jsonify(message="Transaction details fetched", data=result), 200

    except Exception as e:
        print(f"Error: {e}") 
        # Ideally import logging and use: logging.error(f"Error: {e}", exc_info=True)
        return jsonify(error=f"Server Error: {str(e)}"), 500
    finally:
        if cursor: cursor.close()
        if con: con.close()
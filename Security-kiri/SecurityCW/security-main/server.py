from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response, jsonify
import time
from datetime import datetime
import sqlite3

bank_database = "bank.db"
def get_db_connect():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(database=bank_database)
    conn.row_factory = sqlite3.Row
    return conn

host_name = 'localhost' # Must be 'localhost' for https
port_number = 8080 # 8080 for localhost or 5000 (flask defualt port number)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = 'my_secret_key' # unsecure key only for test
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['SESSION_COOKIE_SECURE'] = True   # Use only with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Prevent cross-site access
app.config['SESSION_PERMANENT'] = False  # Ensure session is non-permanent

SESSION_TIMEOUT = 300  # after this time of no activities, log the user out 

@app.before_request
def enforce_session_timeout():
    """Check if the session has expired to log out users who 
    does no activity in a period of time."""
    if 'username' in session:
        last_activity = session.get("last_activity", time.time())
        if time.time() - last_activity > SESSION_TIMEOUT:
            session.pop("username", None)  # Remove user session
            session.pop("last_activity", None)
            flash("Session expired. Please log in again.", "warning")
            return redirect(url_for("login"))

        session["last_activity"] = time.time()  # Update last activity timestamp

@app.after_request
def prevent_caching(response):
    """Prevent browser caching login data."""
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login operations."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username,':',password)
        # record valid username
        with get_db_connect() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()

            if user:
                session['username'] = username
                session['user_id'] = user['id']
                session['last_activity'] = time.time()
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid credentials, please try again.", "error")
    return render_template('login.html') 

@app.route("/update_activity", methods=["POST"])
def update_activity():
    """Update session activity when user interacts."""
    if "username" in session:
        session["last_activity"] = time.time()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 403

@app.route("/transfer", methods=["POST"])
def transfer():
    """Transfer money operations."""
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    sender_id = session['user_id']
    receiver_id = data.get("receiver_id")
    amount = float(data.get("amount"))

    if not sender_id or not receiver_id or amount <= 0:
        return jsonify({"error": "Invalid input"}), 400

    with get_db_connect() as conn:
        cursor = conn.cursor()
        sender = cursor.execute("SELECT * FROM users WHERE id = ?", (sender_id,)).fetchone()
        receiver = cursor.execute("SELECT * FROM users WHERE id = ?", (receiver_id,)).fetchone()

        if not sender or not receiver:
            return jsonify({"error": "User not found"}), 404

        if sender['balance'] < amount:
            return jsonify({"error": "Insufficient funds"}), 400

        # Process transaction
        new_sender_balance = sender['balance'] - amount
        new_receiver_balance = receiver['balance'] + amount

        cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_sender_balance, sender_id))
        cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_receiver_balance, receiver_id))
        cursor.execute("INSERT INTO transactions (sender_id, receiver_id, amount, timestamp) VALUES (?, ?, ?, ?)",
                       (sender_id, receiver_id, amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()

        return jsonify({"message": "Transfer successful"}), 200

@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Log user out and clear the session."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/")
def home():
    """Check if there is a valid user. If so, go to the home page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

if __name__ == "__main__":
    # record start time
    start_timestamp = time.time()
    start_time = datetime.fromtimestamp(start_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(f"server starts at {start_time}")

    try:
        context = ("cert.pem", "key.pem")  # Use the generated SSL certificate
        app.run(host=host_name, port=port_number, ssl_context=context)
    except KeyboardInterrupt:
        pass

    # record end time
    end_timestamp = time.time()
    end_time = datetime.fromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(f"server ends at {end_time}")
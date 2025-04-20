import random
import smtplib
from email.mime.text import MIMEText

# Step 1: Basic username/password authentication
def verify_credentials(username_input, password_input):
    # Simulated stored credentials
    correct_username = "user123"
    correct_password = "securepassword"
    return username_input == correct_username and password_input == correct_password

# Step 2: Generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Step 3: Send OTP via email (optional)
def send_otp_email(otp, to_email):
    from_email = "your_email@gmail.com"
    app_password = "your_app_password"  # use an app-specific password

    msg = MIMEText(f"Your One-Time Password (OTP) is: {otp}")
    msg['Subject'] = "Your MFA Code"
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_email, app_password)
            smtp.send_message(msg)
        print("[+] OTP sent via email.")
    except Exception as e:
        print(f"[!] Failed to send OTP via email: {e}")

# === Main Program ===
username = input("Enter your username: ")
password = input("Enter your password: ")

if verify_credentials(username, password):
    otp = generate_otp()
    
    # Choose delivery method
    print(f"\n[DEBUG] OTP for testing: {otp}")  # Simulate sending OTP
    # send_otp_email(otp, "recipient@example.com")  # Uncomment to send email

    entered_otp = input("Enter the OTP sent to your device: ")

    if entered_otp == otp:
        print("[✅] Authentication successful.")
    else:
        print("[❌] Incorrect OTP. Access denied.")
else:
    print("[❌] Invalid username or password.")

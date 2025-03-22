import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import re
import socket
from datetime import datetime
from email.utils import formataddr
import time

# Function to validate email addresses
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# HTML content template for the email
html_content_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Security Alert</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #ffffff;  /* Background remains white for the page */
        }}
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;  /* Changed to white for the middle section */
            color: #333333;  /* Set text color to dark gray for contrast */
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .email-header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .email-header img {{
            height: 30px;
        }}
        .email-content {{
            font-size: 16px;
            line-height: 1.5;
            text-align: center;
        }}
        .email-content a {{
            color: #3182CE;  /* Set the link color to blue */
            text-decoration: none;  /* Remove underlines from links */
        }}
        .email-buttons {{
            text-align: center;
        }}
        .email-buttons a {{
            display: inline-block;
            width: 145px;
            margin: 5px;
            padding: 10px 0;
            background-color: #3182CE;  /* Set button color to blue */
            color: #ffffff;
            text-decoration: none;
            border-radius: 7px;
            border: 2px solid transparent; /* Add transparent border to buttons */
            transition: border-color 0.3s ease, box-shadow 0.3s ease; /* Smooth transition */
        }}
        .email-buttons a.secondary {{
            background-color: #fffefe;  /* Secondary button color */
            color: #3182CE; /* Set text color for secondary button */
            border: 2px solid #3182CE; /* Add border to secondary button */
        }}
        .email-buttons a:hover {{
            border-color: #ffffff; /* Change border color to white on hover */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow effect */
        }}
        .email-buttons a.secondary:hover {{
            border-color: #3182CE; /* Keep border color same for secondary button on hover */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow effect */
        }}
        span {{
            content: "\2609";
        }}
        .email-footer {{
            text-align: center;
            font-size: 14px;
            color: #A0AEC0;  /* Lighter color for footer text */
        }}
        .footer-buttons {{
            text-align: center;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Email Header -->
        <div class="email-header">
            <img src="https://www.gstatic.com/images/branding/googlelogo/1x/googlelogo_color_74x24dp.png" alt="Google Logo">
        </div>

        <!-- Email Content -->
        <h1 style="text-align: center; font-size: 22px; margin-bottom: 20px;">A new sign-in on Windows</h1>
        <p class="email-content">
            We noticed a new sign-in to your Google Account on a Windows device. If this was you, you don’t need to do anything. If not, we’ll help you secure your account.
        </p>
        <p class="email-content" style="text-align:left;font-size: 14px;">
            Device: DESKTOP-FEBHC03R <br> Time: {send_time}
        </p>

        <!-- Email Buttons -->
        <h4 style="text-align: left;">Do you recognize this activity?</h4>
        <div class="email-buttons">
            <a href="https://hackedd.vercel.app/" class="secondary" style="color:#3182CE; border: #faf3f3 solid 1pt;">Yes, it was me</a>
            <a href="https://hackedd.vercel.app/" class="secondary" style="color:#c43c4a; border: #faf3f3 solid 1pt;">No, secure account</a>
        </div>

        <!-- Email Footer -->
        <p class="email-footer">
            You can also see security activity at
        </p>
        <p class="email-footer">
            <a href="https://hackedd.vercel.app/" style="color: #3182CE;">https://myaccount.google.com/notifications</a>
        </p>
    </div>
</body>
</html>

"""



# # Plain text version of the email content
# plain_text_content = """
# Security Alert: New Sign-in on Windows

# We noticed a new sign-in to your Google Account on a Windows device. If this was you, you don’t need to do anything. If not, we’ll help you secure your account.

# Yes, it's me: https://myaccount.google.com/notifications
# No, it's not me: https://myaccount.google.com/notifications

# For more details, visit: https://myaccount.google.com/notifications
# """

# Function to send email
def send_email(receiver_email, sender_email, password):
    # Get current time and device name
    send_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    device_name = socket.gethostname()

    # Format the HTML content with dynamic values
    html_content = html_content_template.format(send_time=send_time, device_name=device_name)

    # Create the message object
    message = MIMEMultipart()
    message["From"] = formataddr(("Google","no-reply@google.com"))
    message["To"] = receiver_email
    message["Subject"] = "Security Alert: New Sign-in Attempt"
    message["List-Unsubscribe"] = "<https://myaccount.google.com/notifications>"

    # Attach both plain text and HTML versions
    # message.attach(MIMEText(plain_text_content, "plain"))
    message.attach(MIMEText(html_content, "html"))

    # Send the email using SMTP with login credentials
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.set_debuglevel(0)  # Debugging output disabled
            server.login(sender_email, password)
            server.send_message(message)
            print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email to {receiver_email}. Error: {str(e)}")

while True:
    sender_email = input("Enter your email address: ")
    if is_valid_email(sender_email):
        break
    print("Invalid email address. Please try again.")

while True:
    password = getpass.getpass("Enter your email password (App password if 2FA is enabled): ")
    if password:
        break
    print("Password cannot be empty. Please try again.")

# Send email to multiple recipients
while True:
    receiver_email = input("Enter receiver's email (or 'q' to quit): ")
    if receiver_email.lower() == 'q':
        break
    if is_valid_email(receiver_email):
        send_email(receiver_email, sender_email, password)
        time.sleep(5)  # Delay of 5 seconds between each email to reduce the chances of being flagged as spam
    else:
        print("Invalid email address. Please try again.")

print("Email sending process completed.")

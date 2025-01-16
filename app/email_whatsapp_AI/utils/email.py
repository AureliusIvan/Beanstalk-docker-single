import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send an email
def send_email_smtp(sender_email, sender_password, recipient_email, subject, body, smtp_server, smtp_port=587):
    # Set up the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Login
            server.sendmail(sender_email, recipient_email, msg.as_string())  # Send the email
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Function to fetch the latest email
def fetch_email_imap(email_account, email_password, imap_server):
    try:
        # Connect to IMAP server
        with imaplib.IMAP4_SSL(imap_server) as mail:
            mail.login(email_account, email_password)  # Login
            mail.select("inbox")  # Select the mailbox you want to use

            # Search for all emails
            result, data = mail.search(None, "ALL")
            if result == "OK":
                email_ids = data[0].split()  # Get list of email IDs
                latest_email_id = email_ids[-1]  # Get the latest email ID

                # Fetch the email by ID
                result, message_data = mail.fetch(latest_email_id, "(RFC822)")
                if result == "OK":
                    # Parse email content
                    raw_email = message_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    # Extract subject and body
                    email_subject = msg["subject"]
                    email_from = msg["from"]
                    email_body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                email_body = part.get_payload(decode=True).decode()
                    else:
                        email_body = msg.get_payload(decode=True).decode()

                    print("From:", email_from)
                    print("Subject:", email_subject)
                    print("Body:", email_body)
                else:
                    print("Failed to fetch email.")
            else:
                print("No emails found.")
    except Exception as e:
        print(f"Failed to fetch email: {e}")

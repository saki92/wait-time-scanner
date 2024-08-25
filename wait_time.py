import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def fetch_and_parse(url):
    try:
        # Define a User-Agent string that mimics a Firefox browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
        }

        # Fetch the content from the URL with the User-Agent header
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Handle plain text response
        text_content = response.text.strip()  # Remove any leading/trailing whitespace

        # Extract the first word
        first_word = text_content.split()[0] if text_content else ""

        print(f"First word extracted: '{first_word}'")

        # Attempt to convert the first word to a number
        try:
            number = int(first_word)
            print(f"Converted to number: {number}")

            # Define the threshold value
            threshold = 10.0

            # Check if the number is below the threshold and send an email if it is
            if number < threshold:
                send_email(number)
            else:
                print(f"Number {number} is above the threshold of {threshold}.")

        except ValueError:
            print(f"'{first_word}' is not a valid number.")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def send_email(number):
    # Email configuration
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_user = 'your-email@example.com'
    smtp_password = 'your-email-password'
    from_email = 'your-email@example.com'
    to_email = 'recipient@example.com'
    subject = 'Alert: Number Below Threshold'
    
    # Create email message
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    
    body = f"The extracted number {number} is below the threshold."
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade to a secure connection
            server.login(smtp_user, smtp_password)
            server.send_message(message)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    url = input("Enter the URL to fetch and parse: ")
    fetch_and_parse(url)


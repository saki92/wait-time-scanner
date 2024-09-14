import requests
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def read_from_json(filename, field, default):
    try:
        with open(filename, 'r') as file:
            config = json.load(file)
            return config.get(field, default)
    except FileNotFoundError:
        print(f"File {filename} not found. Using default {field}.")
        return default
    except json.JSONDecodeError:
        print("Error decoding JSON file. Using default {field}.")
        return default

def write_to_json(filename, field, val):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)

        data[field] = val

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    except IOError as e:
        print(f"Error writing to JSON file: {e}")

def fetch_and_parse(url, config_file):
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

        # Read the threshold value from the JSON file
        threshold = read_from_json(config_file, 'threshold', 30)

        # Attempt to convert the first word to a number
        try:
            number = int(first_word)
            print(f"Converted to number: {number}")

            # Check if the number is below the threshold and send an email if it is
            if number < threshold:
                send_email(number)
                write_to_json(config_file, 'threshold', number)
            else:
                print(f"Number {number} is above the threshold of {threshold}.")

        except ValueError:
            print(f"'{first_word}' is not a valid number.")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def send_email(number):
    # Email configuration
    smtp_server = read_from_json(config_file, 'smtp_server', "")
    smtp_port = read_from_json(config_file, 'smtp_port', 465)
    smtp_user = read_from_json(config_file, 'smtp_user', "")
    smtp_password = read_from_json(config_file, 'smtp_password', "")
    from_email = smtp_user
    to_email = read_from_json(config_file, 'to_email', "")
    subject = 'Alert: Number Below Threshold'
    
    # Create email message
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    
    body = f"Current wait time is {number} is below the threshold."
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(message)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    config_file = 'config.json'
    url = read_from_json(config_file, 'url', '')
    fetch_and_parse(url, config_file)


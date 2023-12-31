import cv2
import os

# Open the video file (replace 'video.mp4' with your video file)
video_file = '/Users/manumaddi/Downloads/eye-track.mp4'
output_folder = 'I:/Users/manumaddi/Desktop/eye-dataset'

# Check if the output folder exists, and create it if not
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cap = cv2.VideoCapture(video_file)

# Check if the video file was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file")
    exit()

frame_number = 0

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # If the frame was not read successfully, we've reached the end of the video
    if not ret:
        break

    # Define the filename for the frame
    frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.png")

    # Save the frame as an image file
    cv2.imwrite(frame_filename, frame)

    # Increment the frame number
    frame_number += 1

# Release the video capture object and close any open windows
cap.release()
cv2.destroyAllWindows()

print(f"Saved {frame_number} frames to {output_folder}")




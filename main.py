# main.py
#
# Python QR Code Scanner with Tkinter Display
#
# This script uses your computer's camera to detect and scan QR codes in real-time
# using the built-in detector in OpenCV. A separate Tkinter window displays the
# decoded information.
#
# To use this script, you will need to have the following libraries installed:
# - opencv-python: For accessing the camera and detecting the QR code.
# - numpy: For processing the bounding box data from the detector.
#
# You can install these libraries by running the following command in your terminal:
# pip install opencv-python numpy
#
# Once the libraries are installed, you can run this script from your terminal:
# python main.py
#
# Two windows will open: one showing your camera's feed and another to display text.
# When a QR code is detected, a green box will be drawn around it in the camera feed,
# and the decoded information will appear in the text area of the second window.
#
# To close the application, press the 'q' key while the camera feed window is active.

import cv2
import numpy as np
import tkinter as tk
from tkinter import scrolledtext

def qr_code_scanner():
    """
    Initializes a Tkinter window, the camera, and starts the QR code scanning process.
    """
    # --- Initialize Tkinter Window ---
    root = tk.Tk()
    root.title("Decoded QR Code")
    root.geometry("400x300")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=48, height=15)
    text_area.pack(pady=10, padx=10)
    text_area.configure(state='disabled')

    last_decoded_data = ""

    # --- Initialize OpenCV Camera and Detector ---
    # Initialize the video capture object to access the camera.
    # '0' is typically the default camera.
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        root.destroy()
        return

    # Initialize the QRCodeDetector
    detector = cv2.QRCodeDetector()

    print("Starting QR code scanner... Press 'q' to quit.")

    while True:
        # Read a frame from the camera.
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Detect and decode the QR code in the frame.
        data, bbox, _ = detector.detectAndDecode(frame)

        # If a QR code is detected.
        if bbox is not None:
            # If the decoded data is new, update the Tkinter text area.
            if data and data != last_decoded_data:
                print(f"QR Code Detected: {data}")
                
                # Enable the text area to insert text, then disable it again
                text_area.configure(state='normal')
                text_area.insert(tk.END, data + "\n\n")
                text_area.configure(state='disabled')
                
                # Autoscroll to the bottom
                text_area.see(tk.END)
                
                last_decoded_data = data

            # Draw the bounding box around the QR code
            points = bbox[0].astype(int)
            num_points = len(points)
            for i in range(num_points):
                cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % num_points]), (0, 255, 0), 2)

            # Put the decoded text on the frame above the QR code.
            text_origin = tuple(points[0])
            cv2.putText(frame, data, (text_origin[0], text_origin[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

        # Display the camera feed.
        cv2.imshow("QR Code Scanner", frame)

        # Update the Tkinter window
        root.update()
        root.update_idletasks()
        
        # Break the loop if 'q' is pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release all resources.
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()
    print("QR code scanner stopped.")

if __name__ == "__main__":
    qr_code_scanner()
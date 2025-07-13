import cv2
import numpy as np
import tkinter as tk
from tkinter import scrolledtext
import time

def qr_code_scanner():
    """
    Initializes a GUI and camera to scan QR codes without displaying a live feed.
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
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        root.destroy()
        return

    detector = cv2.QRCodeDetector()

    print("Starting QR code scanner... Press Ctrl+C to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                # If the camera disconnects or fails
                print("Error: Failed to capture image. Retrying...")
                time.sleep(2)
                continue
            
            data, bbox = None, None
            try:
                data, bbox, _ = detector.detectAndDecode(frame)
            except cv2.error as e:
                print(f"OpenCV detection error: {e}")
                continue

            # If a QR code is detected and the data is new.
            if bbox is not None and data and data != last_decoded_data:
                print(f"QR Code Detected: {data}")
                
                # Update Tkinter Text Area by replacing the content
                text_area.configure(state='normal')
                text_area.delete(1.0, tk.END)  # Clear the text area
                text_area.insert(tk.END, data)     # Insert new data
                text_area.configure(state='disabled')
                
                last_decoded_data = data
            
            root.update_idletasks()
            root.update()
            
            # Add a small delay to prevent high CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        # Handle the user pressing Ctrl+C.
        print("\nInterrupted by user. Shutting down.")
    
    finally:
        # This block will always run, ensuring resources are released.
        print("Releasing resources...")
        cap.release()
        cv2.destroyAllWindows()
        # Check if the root window exists before trying to destroy it
        if 'root' in locals() and root.winfo_exists():
            root.destroy()
        print("Scanner stopped.")

if __name__ == "__main__":
    qr_code_scanner()

import cv2
import numpy as np
import tkinter as tk
from tkinter import scrolledtext

def qr_code_scanner():
    """
    Initializes a GUI, camera, and QR scanner with robust exception handling.
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
    print("Starting QR code scanner... Press 'q' or Ctrl+C to quit.")

    try:
        while True:
            # Read a frame from the camera.
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image. Exiting.")
                break
            
            data, bbox = None, None
            try:
                # Attempt to detect and decode the QR code in the frame.
                data, bbox, _ = detector.detectAndDecode(frame)
            except cv2.error as e:
                # Catch and print OpenCV errors, then continue to the next frame.
                print(f"OpenCV detection error: {e}")
                continue

            # If a QR code is detected.
            if bbox is not None and data:
                # If the decoded data is new, update the Tkinter text area.
                if data != last_decoded_data:
                    print(f"QR Code Detected: {data}")
                    
                    # --- MODIFIED SECTION ---
                    # Update Tkinter Text Area by replacing the content
                    text_area.configure(state='normal')
                    text_area.delete(1.0, tk.END)  # Clear the text area
                    text_area.insert(tk.END, data)     # Insert new data
                    text_area.configure(state='disabled')
                    # --- END MODIFIED SECTION ---
                    
                    last_decoded_data = data

                # Draw the bounding box and display the data on the frame
                points = bbox[0].astype(int)
                cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=2)
                text_origin = tuple(points[0])
                cv2.putText(frame, data, (text_origin[0], text_origin[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)

            # Display the camera feed.
            cv2.imshow("QR Code Scanner", frame)

            # Update the Tkinter window
            root.update_idletasks()
            root.update()
            
            # Break the loop if 'q' is pressed.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

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

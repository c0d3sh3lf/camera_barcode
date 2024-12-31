import cv2
from pyzbar.pyzbar import decode
import pytesseract
import numpy as np

def process_frame(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Enhance the image by applying a GaussianBlur and adaptive threshold
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Decode barcodes/QR codes from the thresholded image
    barcodes = decode(thresh)
    found_barcode = False

    for barcode in barcodes:
        found_barcode = True
        # Extract the bounding box location
        x, y, w, h = barcode.rect
        # Draw a rectangle around the detected barcode/QR code
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Extract the barcode data
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        # Display the barcode type and data on the frame
        text = f"{barcode_type}: {barcode_data}"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print(f"Detected {barcode_type}: {barcode_data}")

    if not found_barcode:
        print("No barcodes/QR codes detected in this frame.")

    # Perform OCR on the frame
    ocr_text = pytesseract.image_to_string(gray)
    if ocr_text.strip():
        print("OCR Text:")
        print(ocr_text.strip())

    return frame

def main():
    # Open the camera feed
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Press 'q' to quit.")
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Process the frame
        processed_frame = process_frame(frame)

        # Display the processed frame
        cv2.imshow('Barcode/QR Code Scanner with OCR', processed_frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

import cv2
import os
import time
from PIL import ImageGrab
import numpy as np
import subprocess

os.makedirs("samples", exist_ok=True)

print("=" * 50)
print("Improved Face Capture System")
print("=" * 50)

# Open Windows Camera app
print("\n📸 Opening Camera app...")
subprocess.Popen("start microsoft.windows.camera:", shell=True)
time.sleep(3)

print("\nPosition the Camera app window so your face is visible")
print("The system will only save HIGH QUALITY face samples")
print("Press ESC to quit\n")

# Load face detector
detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

face_id = input("Enter a Numeric user ID (e.g., 1 for Yu): ")
print(f"\n📸 Capturing samples for ID: {face_id}")

count = 0
last_capture_time = 0
capture_delay = 0.5  # 0.5 seconds between captures
good_quality_threshold = 50  # Minimum face size for good quality

while count < 100:
    # Capture screen
    screenshot = ImageGrab.grab()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (800, 600))
    img = cv2.flip(img, 1)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces with multiple scales for better detection
    faces = detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(100, 100))
    
    # Display status
    cv2.putText(img, f"Samples: {count}/100", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    current_time = time.time()
    
    if len(faces) > 0:
        # Take the largest face
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face
        
        # Check if face is large enough for good quality
        if w >= good_quality_threshold and h >= good_quality_threshold:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.putText(img, "GOOD QUALITY FACE", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Auto-capture
            if current_time - last_capture_time >= capture_delay:
                count += 1
                face_img = gray[y:y+h, x:x+w]
                # Resize to consistent size
                face_img = cv2.resize(face_img, (200, 200))
                filename = f"samples/face.{face_id}.{count}.jpg"
                cv2.imwrite(filename, face_img)
                print(f"✅ Captured good sample {count}/100 (Face size: {w}x{h})")
                last_capture_time = current_time
                
                # Visual feedback
                cv2.putText(img, f"CAPTURED! ({count})", (x, y+h+25), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(img, "MOVE CLOSER - Face too small", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    else:
        cv2.putText(img, "NO FACE DETECTED - Look at camera", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    cv2.imshow('Face Capture - Move closer for better quality', img)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

print(f"\n✅ Capture complete! {count} good quality samples saved")
print("📁 Location: samples/")
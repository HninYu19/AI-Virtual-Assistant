import cv2
import os
import numpy as np
from PIL import ImageGrab
import time
import subprocess
import sys

def AuthenticateFace():
    print("=" * 50)
    print("Face Recognition Authentication System")
    print("=" * 50)
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths
    trainer_path = os.path.join(script_dir, 'trainer', 'trainer.yml')
    cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
    
    # Check if trainer file exists
    if not os.path.exists(trainer_path):
        print(f"\n❌ Trainer file not found: {trainer_path}")
        print("Please run trainer.py first to train the model")
        return 0
    
    if not os.path.exists(cascade_path):
        print(f"\n❌ Cascade file not found: {cascade_path}")
        return 0
    
    print("\n✅ Files found")
    
    # Load recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(trainer_path)
    print("✅ Model loaded")
    
    # Load cascade
    faceCascade = cv2.CascadeClassifier(cascade_path)
    
    # Names list (index 1 = Yu)
    names = ['Unknown', 'Yu']
    
    # Open Windows Camera app for screen capture
    print("\n📸 Opening Camera app...")
    subprocess.Popen("start microsoft.windows.camera:", shell=True)
    time.sleep(3)
    
    print("\nPosition the Camera app window so your face is visible")
    print("You have 10 seconds to authenticate...")
    print("Press 'ESC' to cancel")
    print("=" * 50)
    
    start_time = time.time()
    timeout = 10  # 10 seconds timeout
    recognized = False
    best_accuracy = 0
    
    while time.time() - start_time < timeout and not recognized:
        # Capture screen
        screenshot = ImageGrab.grab()
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (800, 600))
        img = cv2.flip(img, 1)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(80, 80))
        
        # Show remaining time
        remaining = int(timeout - (time.time() - start_time))
        cv2.putText(img, f"Time remaining: {remaining}s", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(img, "Face Recognition Authentication", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
        
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                # Draw rectangle
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Predict
                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                accuracy = round(100 - confidence)
                
                if confidence < 100 and accuracy > 50:
                    name = names[id] if id < len(names) else f"ID_{id}"
                    color = (0, 255, 0)
                    cv2.putText(img, f"{name} - {accuracy}%", (x+5, y-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    
                    if name == "Yu" and accuracy > best_accuracy:
                        best_accuracy = accuracy
                        recognized = True
                        cv2.putText(img, "ACCESS GRANTED!", (img.shape[1]//2 - 100, img.shape[0]//2), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                else:
                    cv2.putText(img, "Unknown", (x+5, y-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow('Face Recognition - Look at camera', img)
        
        # Check for quit
        if cv2.waitKey(10) & 0xFF == 27:
            print("\n❌ Authentication cancelled by user")
            break
    
    cv2.destroyAllWindows()
    
    # Return result
    print("\n" + "=" * 50)
    if recognized and best_accuracy > 50:
        print(f"✅ ACCESS GRANTED!")
        print(f"   Recognized as: Yu")
        print(f"   Confidence: {best_accuracy}%")
        print("=" * 50)
        return 1
    else:
        print(f"❌ ACCESS DENIED!")
        if best_accuracy > 0:
            print(f"   Best match confidence: {best_accuracy}% (needs >50%)")
        else:
            print("   No face detected or recognized")
        print("=" * 50)
        return 0

# For direct testing
if __name__ == "__main__":
    result = AuthenticateFace()
    sys.exit(0 if result == 1 else 1)
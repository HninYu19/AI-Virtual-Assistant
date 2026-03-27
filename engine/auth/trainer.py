import cv2
import numpy as np
import os

print("=" * 50)
print("Retraining Face Recognition System")
print("=" * 50)

script_dir = os.path.dirname(os.path.abspath(__file__))
samples_dir = os.path.join(script_dir, 'samples')
cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
trainer_dir = os.path.join(script_dir, 'trainer')
trainer_file = os.path.join(trainer_dir, 'trainer.yml')

# Check samples
sample_files = [f for f in os.listdir(samples_dir) if f.endswith('.jpg')]
print(f"\nFound {len(sample_files)} sample images")

if len(sample_files) == 0:
    print("❌ No samples found!")
    exit()

# Load cascade
detector = cv2.CascadeClassifier(cascade_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()

face_samples = []
ids = []

print("\nProcessing samples...")
for file in sample_files:
    try:
        img_path = os.path.join(samples_dir, file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            continue
        
        # Extract ID from filename
        user_id = int(file.split('.')[1])
        
        # Detect face
        faces = detector.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
        
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                face_roi = img[y:y+h, x:x+w]
                face_samples.append(face_roi)
                ids.append(user_id)
                print(f"✓ Processed: {file}")
        else:
            print(f"⚠️ No face in: {file}")
            
    except Exception as e:
        print(f"❌ Error with {file}: {e}")

if len(face_samples) == 0:
    print("\n❌ No valid face samples found!")
    exit()

print(f"\n✅ Loaded {len(face_samples)} face samples from {len(set(ids))} user(s)")

# Train
print("\n🔄 Training...")
recognizer.train(face_samples, np.array(ids))

# Save
os.makedirs(trainer_dir, exist_ok=True)
recognizer.write(trainer_file)

print(f"✅ Model saved to: {trainer_file}")
print("\n🎉 Training complete! You can now run recognition.")
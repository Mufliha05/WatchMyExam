import cv2
from datetime import datetime
from flask import current_app
from models import db, Violation


import os

def log_violation(user_id, violation_type, frame):

    timestamp = datetime.now()
    filename = f"{user_id}_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join("evidence", filename)

    # Save image
    cv2.imwrite(filepath, frame)

    with current_app.app_context():
        violation = Violation(
            user_id=user_id,
            violation_type=violation_type,
            timestamp=timestamp,
            image_path=filepath
        )

        db.session.add(violation)
        db.session.commit()


def start_monitoring(user_id=1):

    cap = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    print("AI Monitoring Started... Press ESC to stop")

    last_violation_time = None
    cooldown_seconds = 5

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        current_time = datetime.now()

        violation_type = None

        if len(faces) == 0:
            violation_type = "No face detected"

        elif len(faces) > 1:
            violation_type = "Multiple faces detected"

        else:
            print("Face detected")

        # 🚨 Log only if cooldown passed
        if violation_type:
            if (
                last_violation_time is None or
                (current_time - last_violation_time).seconds > cooldown_seconds
            ):
                print("VIOLATION:", violation_type)
                log_violation(user_id, violation_type, frame)
                last_violation_time = current_time

        cv2.imshow("Monitoring", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
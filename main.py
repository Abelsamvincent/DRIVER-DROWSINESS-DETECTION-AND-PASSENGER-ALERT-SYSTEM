import cv2
from detector import DrowsinessDetector
from alert import SoundManager
from state_tracker import StateTracker
import config

def main():
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    detector = DrowsinessDetector()
    sound_manager = SoundManager()
    tracker = StateTracker()

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        results, image = detector.detect(image)
        image = detector.draw_landmarks(image, results)

        # Default info
        status_info = {
            "overall": "NORMAL",
            "eye": "NONE",
            "yawn": "NONE",
            "nod": "NONE",
            "action": None
        }
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_ear, right_ear = detector.get_eye_landmarks(face_landmarks.landmark)
                avg_ear = (left_ear + right_ear) / 2.0
                
                mar = detector.calculate_mar(face_landmarks.landmark)
                
                img_h, img_w, _ = image.shape
                rot_vec, trans_vec = detector.get_head_pose(face_landmarks.landmark, img_w, img_h)
                pitch, yaw, roll = detector.get_euler_angles(rot_vec)
                
                # Update tracker
                status_info = tracker.update(avg_ear, mar, pitch)
                
                # Trigger alerts
                if status_info["action"] == "driver_short":
                    sound_manager.play_driver_short_alarm()
                elif status_info["action"] == "driver_passenger_long":
                    sound_manager.play_driver_long_alarm()
                    sound_manager.play_passenger_long_alarm()
                
                # Display Raw Values
                cv2.putText(image, f'EAR: {avg_ear:.2f}', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(image, f'MAR: {mar:.2f}', (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(image, f'Pitch: {pitch:.2f}', (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Display Warnings/Critical Messages
        y_offset = 130
        
        # Eye State
        if status_info["eye"] == StateTracker.STATE_WARNING:
            cv2.putText(image, "Eyes closing - WARNING", (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
            y_offset += 30
        elif status_info["eye"] == StateTracker.STATE_CRITICAL:
            cv2.putText(image, "Eyes closed - CRITICAL", (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            y_offset += 30
            
        # Yawn State
        if status_info["yawn"] == StateTracker.STATE_WARNING:
            cv2.putText(image, "Yawning - WARNING", (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
            y_offset += 30
        elif status_info["yawn"] == StateTracker.STATE_CRITICAL:
            cv2.putText(image, "Yawning - CRITICAL", (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            y_offset += 30
            
        # Nod State
        if status_info["nod"] == StateTracker.STATE_WARNING:
            cv2.putText(image, "Head nodding - WARNING", (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
            y_offset += 30
        elif status_info["nod"] == StateTracker.STATE_CRITICAL:
            cv2.putText(image, "Head nodding - CRITICAL", (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            y_offset += 30

        # Overall State (Optional, but good for summary)
        if status_info["overall"] == StateTracker.STATE_NORMAL:
             cv2.putText(image, "Status: NORMAL", (30, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow('Driver Drowsiness Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    sound_manager.stop()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

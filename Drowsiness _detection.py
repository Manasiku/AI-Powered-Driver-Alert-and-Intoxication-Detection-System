import cv2
import numpy as np
import mediapipe as mp
import simpleaudio as sa
import threading
import time
from twilio.rest import Client

# ---------------------- Twilio WhatsApp Setup ----------------------
account_sid = "AC0b741053fd810e254af2f54d7807e4e1"
auth_token = "d78796e1d8112bdb6f352859e3359678"
client = Client(account_sid, auth_token)

FROM_WHATSAPP = "whatsapp:+14155238886"  # Twilio Sandbox
TO_WHATSAPP   = "whatsapp:+916361334416"   # Replace with your WhatsApp

def send_alert_whatsapp():
    try:
        message = client.messages.create(
            body="⚠️ ALERT: Drowsiness detected! Please take a break.",
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP
        )
        print("✅ WhatsApp alert sent:", message.sid)
    except Exception as e:
        print("❌ WhatsApp alert failed:", e)

# ---------------------- Audio ----------------------
wave_obj = sa.WaveObject.from_wave_file("beep.wav")
play_obj = None
lock = threading.Lock()

def start_alarm():
    global play_obj
    with lock:
        if play_obj is None or not play_obj.is_playing():
            play_obj = wave_obj.play()

def stop_alarm():
    global play_obj
    with lock:
        if play_obj and play_obj.is_playing():
            play_obj.stop()
            play_obj = None

# ---------------------- EAR & MAR ----------------------
def eye_aspect_ratio(landmarks, eye_indices):
    p = [np.array([landmarks[i].x, landmarks[i].y]) for i in eye_indices]
    A = np.linalg.norm(p[1] - p[5])
    B = np.linalg.norm(p[2] - p[4])
    C = np.linalg.norm(p[0] - p[3])
    return (A + B) / (2.0 * C)

def mouth_aspect_ratio(landmarks, mouth_indices):
    p = [np.array([landmarks[i].x, landmarks[i].y]) for i in mouth_indices]
    A = np.linalg.norm(p[1] - p[5])
    B = np.linalg.norm(p[2] - p[4])
    C = np.linalg.norm(p[0] - p[3])
    return (A + B) / (2.0 * C)

# ---------------------- Mediapipe ----------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
INNER_LIPS = [78, 308, 13, 14, 87, 317]

# ---------------------- Parameters ----------------------
EAR_THRESH = 0.25
MAR_THRESH = 0.6
EYE_CLOSED_SECONDS = 0.3
MOUTH_OPEN_SECONDS = 0.8

eye_closed_start = None
mouth_open_start = None
last_sent = 0
cooldown = 60

cap = cv2.VideoCapture(0)

def draw_bar(frame, value, max_value, position, color_safe, color_alert, label):
    x, y, w, h = position
    # background
    cv2.rectangle(frame, (x, y), (x + w, y + h), (50,50,50), -1)
    # fill bar
    fill_w = int((value / max_value) * w)
    color = color_alert if ((label=="EAR" and value < EAR_THRESH) or (label=="MAR" and value > MAR_THRESH)) else color_safe
    cv2.rectangle(frame, (x, y), (x + fill_w, y + h), color, -1)
    # text: show numeric value on the bar
    cv2.putText(frame, f"{label}: {value:.2f}", (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    ear_display = 0
    mar_display = 0
    alert_text = ""
    trigger_alert = False

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark

            # EAR
            left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
            right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
            ear_display = (left_ear + right_ear) / 2.0

            # MAR
            mar_display = mouth_aspect_ratio(landmarks, INNER_LIPS)

            # EAR alert
            if ear_display < EAR_THRESH:
                if eye_closed_start is None:
                    eye_closed_start = time.time()
                elif time.time() - eye_closed_start >= EYE_CLOSED_SECONDS:
                    alert_text = "DROWSINESS ALERT!"
                    trigger_alert = True
            else:
                eye_closed_start = None

            # MAR alert
            if mar_display > MAR_THRESH:
                if mouth_open_start is None:
                    mouth_open_start = time.time()
                elif time.time() - mouth_open_start >= MOUTH_OPEN_SECONDS:
                    alert_text = "YAWNING ALERT!"
                    trigger_alert = True
            else:
                mouth_open_start = None

            # Draw face landmarks
            mp_drawing.draw_landmarks(
                frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=(0,0,255), thickness=1)
            )

    # Draw bars with different colors
    draw_bar(frame, ear_display, 1.0, position=(30,30,250,25), color_safe=(0,255,0), color_alert=(0,0,255), label="EAR")
    draw_bar(frame, mar_display, 1.0, position=(30,70,250,25), color_safe=(0,200,255), color_alert=(0,0,200), label="MAR")

    # Alerts
    if trigger_alert:
        cv2.putText(frame, alert_text, (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        start_alarm()
        if time.time() - last_sent > cooldown:
            send_alert_whatsapp()
            last_sent = time.time()
    else:
        stop_alarm()

    cv2.imshow("Drowsiness Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
stop_alarm()
import cv2
import mediapipe as mp
import pyautogui
import time

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

# Previous points for smoothing (in normalized [0..1] space)
prev_norm_x, prev_norm_y = 0.5, 0.5  # start centered

# Autoclick system
auto_click_enabled = False
last_toggle_time = 0
idle_start_time = None
idle_threshold = 3  # seconds
last_cursor_x, last_cursor_y = 0, 0
tolerance = 10  # pixels for idle detection

# Right click system
right_click_mode = False
right_idle_start = None
right_idle_threshold = 2  # seconds

# Sensitivity / scaling: increase to make small head moves cover larger screen distance
scale_factor = 1.6  # try 1.2 - 2.0; higher = more sensitive

# smoothing weight for normalized coordinates (0..1)
smooth_alpha = 0.3  # new sample weight (0.0..1.0). Lower = more smoothing.

# helper clamp
def clamp(v, a, b):
    return max(a, min(b, v))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # mirror so movement feels natural
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            h, w, c = frame.shape
            # nose landmark in normalized coordinates
            nose = landmarks.landmark[1]
            norm_x = nose.x  # normalized 0..1
            norm_y = nose.y  # normalized 0..1

            # Smooth normalized coords (exponential moving average)
            smooth_norm_x = (prev_norm_x * (1 - smooth_alpha)) + (norm_x * smooth_alpha)
            smooth_norm_y = (prev_norm_y * (1 - smooth_alpha)) + (norm_y * smooth_alpha)
            prev_norm_x, prev_norm_y = smooth_norm_x, smooth_norm_y

            # Draw red dot on webcam preview (converted back to frame pixels)
            px = int(smooth_norm_x * w)
            py = int(smooth_norm_y * h)
            cv2.circle(frame, (px, py), 5, (0, 0, 255), -1)

            # --- SCALE AROUND CENTER to increase travel distance ---
            # center the normalized value (0 = left/top, 0.5 = center, 1 = right/bottom)
            centered_x = smooth_norm_x - 0.5
            centered_y = smooth_norm_y - 0.5

            # amplify the offset from center
            scaled_center_x = centered_x * scale_factor
            scaled_center_y = centered_y * scale_factor

            # convert back to normalized space and clamp 0..1
            scaled_norm_x = clamp(0.5 + scaled_center_x, 0.0, 1.0)
            scaled_norm_y = clamp(0.5 + scaled_center_y, 0.0, 1.0)

            # final screen coordinates (strict clamp to stay visible)
            screen_x = int(clamp(scaled_norm_x, 0.001, 0.999) * screen_w)
            screen_y = int(clamp(scaled_norm_y, 0.001, 0.999) * screen_h)

            # move the mouse safely
            try:
                pyautogui.moveTo(screen_x, screen_y, duration=0)
            except Exception:
                pass

            # -------- AutoClick Toggle Zone (Bottom-Right) -------- #
            if screen_x > screen_w - 100 and screen_y > screen_h - 100:
                current_time = time.time()
                if current_time - last_toggle_time > 1.5:
                    auto_click_enabled = not auto_click_enabled
                    last_toggle_time = current_time
                    idle_start_time = None  # reset when toggling

            # -------- Right Click Mode Toggle (Bottom-Left) -------- #
            if screen_x < 100 and screen_y > screen_h - 100:
                current_time = time.time()
                if current_time - last_toggle_time > 1.5:
                    right_click_mode = not right_click_mode
                    last_toggle_time = current_time
                    print("Right Click Mode:", "ON" if right_click_mode else "OFF")
                    right_idle_start = None

            # -------- Idle Left Click -------- #
            if auto_click_enabled:
                if (abs(screen_x - last_cursor_x) < tolerance and
                    abs(screen_y - last_cursor_y) < tolerance):
                    if idle_start_time is None:
                        idle_start_time = time.time()
                    else:
                        if time.time() - idle_start_time >= idle_threshold:
                            try:
                                pyautogui.click()
                                print("Left Click ✅")
                            except Exception:
                                pass
                            idle_start_time = None
                else:
                    idle_start_time = None

            # -------- Idle Right Click (when right_click_mode ON) -------- #
            if right_click_mode:
                if (abs(screen_x - last_cursor_x) < tolerance and
                    abs(screen_y - last_cursor_y) < tolerance):
                    if right_idle_start is None:
                        right_idle_start = time.time()
                    else:
                        if time.time() - right_idle_start >= right_idle_threshold:
                            try:
                                # small jiggle to ensure OS receives event, then rightClick
                                pyautogui.moveRel(1, 0)
                                pyautogui.moveRel(-1, 0)
                                pyautogui.rightClick()
                                print("Right Click ✅")
                            except Exception:
                                pass
                            right_idle_start = None
                else:
                    right_idle_start = None

            # Update last cursor pos
            last_cursor_x, last_cursor_y = screen_x, screen_y

    # -------- Messages on Screen -------- #
    if auto_click_enabled:
        cv2.putText(frame, "Idle AutoClick: ON", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    else:
        cv2.putText(frame, "Idle AutoClick: OFF", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    if right_click_mode:
        cv2.putText(frame, "Right Click Mode: ON", (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    else:
        cv2.putText(frame, "Right Click Mode: OFF", (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)

    # Zones
    cv2.rectangle(frame, (screen_w - 100, screen_h - 100), (screen_w - 10, screen_h - 10),
                  (255, 0, 0), 2)  # AutoClick Zone
    cv2.rectangle(frame, (10, screen_h - 100), (100, screen_h - 10),
                  (0, 255, 255), 2)  # RightClick Zone

    cv2.imshow("Nose Cursor - Idle Clicks", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import gestures as gest
import voice


def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("MediaPipe Hands", cv2.WINDOW_NORMAL)  
    cv2.resizeWindow("MediaPipe Hands", 400, 300)
    _, frame = cap.read()
    h, w, _ = frame.shape

    voice_listener = voice.VoiceListener()
    hand_controller = gest.HandController(w, h)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    with mp_hands.Hands(max_num_hands=2,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if len(results.multi_hand_landmarks) == 1:
                    hand_controller.handle_one_hand(results.multi_hand_landmarks[0], voice_listener)
                elif len(results.multi_hand_landmarks) == 2:
                    hand1, hand2 = results.multi_hand_landmarks
                    end_loop = hand_controller.handle_two_hands(hand1, hand2)
                    if end_loop:
                        break 

            #frame = hand_controller.draw_overlay(frame)
            frame = cv2.flip(frame, 1)
            cv2.imshow("MediaPipe Hands", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

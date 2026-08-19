import cv2
import time
import sys
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class HandTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Load the HandLandmarker model file dynamically
        model_path = resource_path('hand_landmarker.task')
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=int(maxHands),
            min_hand_detection_confidence=float(detectionCon),
            min_hand_presence_confidence=float(detectionCon),
            min_tracking_confidence=float(trackCon))
        self.detector = vision.HandLandmarker.create_from_options(options)

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
        
        self.results = self.detector.detect(mp_image)

        if draw and self.results.hand_landmarks:
            for hand_landmarks in self.results.hand_landmarks:
                self.draw_landmarks(img, hand_landmarks)
        return img

    def draw_landmarks(self, img, landmarks):
        h, w, c = img.shape
        HAND_CONNECTIONS = [(0, 1), (1, 2), (2, 3), (3, 4),
                            (0, 5), (5, 6), (6, 7), (7, 8),
                            (5, 9), (9, 10), (10, 11), (11, 12),
                            (9, 13), (13, 14), (14, 15), (15, 16),
                            (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)]
        
        # Draw connections
        for connection in HAND_CONNECTIONS:
            pt1 = landmarks[connection[0]]
            pt2 = landmarks[connection[1]]
            x1, y1 = int(pt1.x * w), int(pt1.y * h)
            x2, y2 = int(pt2.x * w), int(pt2.y * h)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
        # Draw dots
        for lm in landmarks:
            x, y = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (x, y), 5, (0, 0, 255), cv2.FILLED)

    def getPosition(self, img, handNo=0, draw=True):
        lmList = []
        if getattr(self, 'results', None) and self.results.hand_landmarks:
            if handNo < len(self.results.hand_landmarks):
                myHand = self.results.hand_landmarks[handNo]
                h, w, c = img.shape
                for lm in myHand:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append((cx, cy, lm.z))
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return lmList

    def getUpFingers(self, img):
        pos = self.getPosition(img, draw=False)
        self.upfingers = []
        if pos and len(pos) == 21:
            # thumb
            self.upfingers.append((pos[4][1] < pos[3][1] and (pos[5][0] - pos[4][0] > 10)))
            # index
            self.upfingers.append((pos[8][1] < pos[7][1] < pos[6][1]))
            # middle
            self.upfingers.append((pos[12][1] < pos[11][1] < pos[10][1]))
            # ring
            self.upfingers.append((pos[16][1] < pos[15][1] < pos[14][1]))
            # pinky
            self.upfingers.append((pos[20][1] < pos[19][1] < pos[18][1]))
        return self.upfingers

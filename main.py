import cv2
import numpy as np
import time
import datetime
import math
import random
from handTracker import HandTracker

class ColorRect:
    def drawRect(self, img, text_color=(255, 255, 255), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, thickness=2):
        # Draw The Box
        alpha = self.alpha
        bg_rec = img[self.y: self.y + self.h, self.x: self.x + self.w]
        white_rect = np.ones(bg_rec.shape, dtype=np.uint8)
        white_rect[:] = self.color
        res = cv2.addWeighted(bg_rec, alpha, white_rect, 1 - alpha, 1.0)

        # Putting The Image Back To Its Position
        img[self.y: self.y + self.h, self.x: self.x + self.w] = res

        # Put The Letter
        text_size = cv2.getTextSize(self.text, fontFace, fontScale, thickness)
        text_pos = (int(self.x + self.w / 2 - text_size[0][0] / 2), int(self.y + self.h / 2 + text_size[0][1] / 2))
        cv2.putText(img, self.text, text_pos, fontFace, fontScale, text_color, thickness)

    def isOver(self, x, y):
        if (self.x + self.w > x > self.x) and (self.y + self.h > y > self.y):
            return True
        return False

    def __init__(self, x, y, w, h, color, text='', alpha=0.5):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.text = text
        self.alpha = alpha
        self.expanded = False


drawing = False
start_point = (0, 0)
shape_to_draw = 1  # Default shape is a circle


def select_options(event, x, y, flags, param):
    global color, brushSize, canvas, colorsBtn, boardBtn, penBtn, pens, drawing, start_point, shape_to_draw

    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if the click is within the color options
        if colorsBtn.isOver(x, y):
            colorsBtn.expanded = not colorsBtn.expanded
            return

        # Check if the click is within the pen size options
        if penBtn.isOver(x, y):
            penBtn.expanded = not penBtn.expanded
            return

        # Check if the click is within the board button
        if boardBtn.isOver(x, y):
            boardBtn.expanded = not boardBtn.expanded
            return

        # Check if the click is within the color palette
        if not hideColors and colorsBtn.expanded:
            for c in colors:
                if c.isOver(x, y):
                    color = c.color
                    colorsBtn.expanded = False  # Collapse color palette
                    return

        # Check if the click is within the pen size options
        if not hidePenSizes and penBtn.expanded:
            for pen in pens:
                if pen.isOver(x, y):
                    brushSize = int(pen.text)
                    penBtn.expanded = False  # Collapse pen size options
                    return

        # Check if the click is within the clear button
        if clear.isOver(x, y):
            canvas = np.zeros((1080, 1920, 3), np.uint8)  # Clear the canvas
            return


cv2.namedWindow('video')
cv2.setMouseCallback('video', select_options)

# initilize the hand detector
detector = HandTracker(maxHands=1, detectionCon=0.4, trackCon=0.4)
# initilize the camera
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

# creating canvas to draw on it
canvas = np.zeros((1080, 1920, 3), np.uint8)

# define a previous point to be used with drawing a line
px, py = 0, 0
# initial brush color
color = (255, 0, 0)
#####
brushSize = 5
eraserSize = 20
####

########### creating colors ########
# Colors button
colorsBtn = ColorRect(170, 0, 100, 100, (120, 255, 0), 'Colors')

key_to_color = {
    ord('b'): (255, 0, 0),  # Blue
    ord('g'): (0, 255, 0),  # Green
    ord('r'): (0, 0, 255),  # Red
    ord('w'): (255, 255, 255),  # White
    ord('k'): (128, 128, 128),  # Black
    ord('e'): (0, 0, 0),  # Eraser
    ord('y'): (0, 255, 255),  # Yellow
    ord('o'): (0, 165, 255),  # Orange
    ord('p'): (180, 105, 255),  # Pink
    ord('i'): (130, 0, 75),  # Indigo
    ord('v'): (238, 130, 238),  # Violet
    ord('n'): (42, 42, 165),  # Brown
}
colors = []

pen_sizes = {
    5: 0,
    10: 1,
    15: 2,
    20: 3,
}

# random color
b = random.randint(0, 255)
g = random.randint(0, 255)
r = random.randint(0, 255)

colors.append(ColorRect(270, 0, 100, 100, (b, g, r)))
# red
colors.append(ColorRect(370, 0, 100, 100, (0, 0, 255)))
# blue
colors.append(ColorRect(470, 0, 100, 100, (255, 0, 0)))
# green
colors.append(ColorRect(570, 0, 100, 100, (0, 255, 0)))
# yellow
colors.append(ColorRect(670, 0, 100, 100, (0, 255, 255)))
# orange
colors.append(ColorRect(770, 0, 100, 100, (0, 165, 255)))
# pink
colors.append(ColorRect(870, 0, 100, 100, (180, 105, 255)))
# purple
colors.append(ColorRect(970, 0, 100, 100, (255, 0, 255)))
# erase (black)
colors.append(ColorRect(1070, 0, 100, 100, (0, 0, 0), "Eraser"))

# clear
clear = ColorRect(1170, 0, 100, 100, (100, 100, 100), "Clear")

# undo
undoBtn = ColorRect(1270, 0, 100, 100, (50, 100, 200), "Undo")

########## pen sizes #######
pens = []
for i, penSize in enumerate(range(5, 25, 5)):
    pens.append(ColorRect(1500 + 100 * i, 0, 100, 100, (50, 50, 50), str(penSize)))

penBtn = ColorRect(1400, 0, 100, 100, color, 'Pen')

# white board button
boardBtn = ColorRect(50, 0, 100, 100, (255, 255, 0), 'Board')

# define a white board to draw on
whiteBoard = ColorRect(50, 120, 1450, 650, (255, 255, 255), alpha=0.6)

coolingCounter = 10
clearCooldown = 0
shapeCooldown = 0
hideBoard = True
smoothed_x, smoothed_y = 0, 0
pinching = False
shape_start_x, shape_start_y = 0, 0
history = []
is_drawing = False
hideColors = True
hidePenSizes = True
pTime = 0

while True:

    if coolingCounter:
        coolingCounter -= 1
        
    if clearCooldown:
        clearCooldown -= 1
        
    if shapeCooldown:
        shapeCooldown -= 1
        # print(coolingCounter)

    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (1920, 1080))
    frame = cv2.flip(frame, 1)

    detector.findHands(frame)
    positions = detector.getPosition(frame, draw=False)
    upFingers = detector.getUpFingers(frame)

    if upFingers:
        x, y = positions[8][0], positions[8][1]
        z = positions[8][2]
        
        dist_pinch = math.hypot(positions[8][0] - positions[4][0], positions[8][1] - positions[4][1])
        
        # Shape Cycle Gesture (Rock On sign: Index + Pinky up, ignore thumb)
        if upFingers[1] and upFingers[4] and not upFingers[2] and not upFingers[3] and not shapeCooldown:
            shape_to_draw = (shape_to_draw % 4) + 1
            shapeCooldown = 20
            
        # Undo Gesture (Pinky only up, ignore thumb)
        elif upFingers[4] and not upFingers[1] and not upFingers[2] and not upFingers[3] and not clearCooldown:
            if len(history) > 0:
                canvas = history.pop().copy()
                clearCooldown = 20
                cv2.putText(frame, "UNDO!", (800, 500), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
        
        # 1. Magic Clear Gesture (4 main fingers up, ignore thumb)
        elif upFingers[1] and upFingers[2] and upFingers[3] and upFingers[4] and not clearCooldown:
            history.append(canvas.copy())
            canvas = np.zeros((1080, 1920, 3), np.uint8)
            clearCooldown = 30 # Prevent continuous clearing
            cv2.putText(frame, "CLEARED!", (800, 500), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
            
        elif upFingers[1] and not upFingers[3] and not upFingers[4] and not whiteBoard.isOver(x, y) and dist_pinch > 50:
            px, py = 0, 0

            ##### pen sizes ######
            if not hidePenSizes:
                for pen in pens:
                    if pen.isOver(x, y):
                        brushSize = int(pen.text)
                        pen.alpha = 0
                    else:
                        pen.alpha = 0.5

            ####### chose a color for drawing #######
            if not hideColors:
                for cb in colors:
                    if cb.isOver(x, y):
                        color = cb.color
                        cb.alpha = 0
                    else:
                        cb.alpha = 0.5

                # Clear
                if clear.isOver(x, y):
                    clear.alpha = 0
                    canvas = np.zeros((1080, 1920, 3), np.uint8)
                else:
                    clear.alpha = 0.5
                    
                # Undo
                if undoBtn.isOver(x, y):
                    undoBtn.alpha = 0
                    if not coolingCounter and len(history) > 0:
                        canvas = history.pop().copy()
                        coolingCounter = 15
                else:
                    undoBtn.alpha = 0.5

            # color button
            if colorsBtn.isOver(x, y) and not coolingCounter:
                coolingCounter = 10
                colorsBtn.alpha = 0
                hideColors = False if hideColors else True
                colorsBtn.text = 'Colors' if hideColors else 'Hide'
            else:
                colorsBtn.alpha = 0.5

            # Pen size button
            if penBtn.isOver(x, y) and not coolingCounter:
                coolingCounter = 10
                penBtn.alpha = 0
                hidePenSizes = False if hidePenSizes else True
                penBtn.text = 'Pen' if hidePenSizes else 'Hide'
            else:
                penBtn.alpha = 0.5

            # white board button
            if boardBtn.isOver(x, y) and not coolingCounter:
                coolingCounter = 10
                boardBtn.alpha = 0
                hideBoard = False if hideBoard else True
                boardBtn.text = 'Board' if hideBoard else 'Hide'
            else:
                boardBtn.alpha = 0.5

        # 2. Eraser Mode Gesture (Index + Middle fingers up, ignore thumb)
        elif upFingers[1] and upFingers[2] and not upFingers[3] and not upFingers[4] and dist_pinch > 50:
            if whiteBoard.isOver(x, y) and not hideBoard:
                is_drawing = True
                cv2.circle(frame, (x, y), eraserSize, (0, 0, 0), -1)
                if px == 0 and py == 0:
                    px, py = x, y
                cv2.line(canvas, (px, py), (x, y), (0, 0, 0), eraserSize)
                px, py = x, y
                
        # Magic Shape Drawer (Pinch gesture)
        elif dist_pinch < 40:
            if not pinching:
                pinching = True
                shape_start_x, shape_start_y = x, y
            
            # draw preview on frame
            if shape_to_draw == 1:
                radius = int(math.hypot(x - shape_start_x, y - shape_start_y))
                cv2.circle(frame, (shape_start_x, shape_start_y), radius, color, max(2, brushSize // 2))
            elif shape_to_draw == 2:
                cv2.rectangle(frame, (shape_start_x, shape_start_y), (x, y), color, max(2, brushSize // 2))
            elif shape_to_draw == 3:
                pts = np.array([[(shape_start_x, shape_start_y), (x, y), (shape_start_x - (x - shape_start_x), y)]], np.int32)
                cv2.polylines(frame, [pts], True, color, max(2, brushSize // 2))
            elif shape_to_draw == 4:
                cv2.line(frame, (shape_start_x, shape_start_y), (x, y), color, max(2, brushSize // 2))
                
        # 3. Dynamic Brush Thickness Mode (Index finger up, others down. Ignore thumb)
        elif upFingers[1] and not upFingers[2] and not upFingers[3] and not upFingers[4] and not pinching:
            if whiteBoard.isOver(x, y) and not hideBoard:
                is_drawing = True
                # Calculate dynamic size based on 3D depth (z-coordinate)
                # Z is typically negative and smaller when closer to the camera
                dynamicSize = max(2, int(brushSize - z * 150))
                
                cv2.circle(frame, (x, y), dynamicSize, color, -1)
                if px == 0 and py == 0:
                    px, py = x, y
                if color == (0, 0, 0):
                    cv2.line(canvas, (px, py), (x, y), color, eraserSize)
                else:
                    cv2.line(canvas, (px, py), (x, y), color, dynamicSize)
                px, py = x, y
        else:
            px, py = 0, 0
            if pinching:
                # Commit shape to canvas
                pinching = False
                history.append(canvas.copy())
                if len(history) > 10: history.pop(0)
                if shape_to_draw == 1:
                    radius = int(math.hypot(x - shape_start_x, y - shape_start_y))
                    cv2.circle(canvas, (shape_start_x, shape_start_y), radius, color, max(2, brushSize // 2))
                elif shape_to_draw == 2:
                    cv2.rectangle(canvas, (shape_start_x, shape_start_y), (x, y), color, max(2, brushSize // 2))
                elif shape_to_draw == 3:
                    pts = np.array([[(shape_start_x, shape_start_y), (x, y), (shape_start_x - (x - shape_start_x), y)]], np.int32)
                    cv2.polylines(canvas, [pts], True, color, max(2, brushSize // 2))
                elif shape_to_draw == 4:
                    cv2.line(canvas, (shape_start_x, shape_start_y), (x, y), color, max(2, brushSize // 2))
            
            if is_drawing:
                history.append(canvas.copy())
                if len(history) > 10: history.pop(0)
                is_drawing = False
                
    else:
        if pinching:
            pinching = False
        if is_drawing:
            history.append(canvas.copy())
            if len(history) > 10: history.pop(0)
            is_drawing = False

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Check if Esc key is pressed
        break
    elif 49 <= key <= 52:  # Check if number keys 1 to 4 are pressed
        shape_to_draw = key - 48
    elif key in key_to_color:
        color = key_to_color[key]
    elif key == ord('+'):
        brushSize += 1
    elif key == ord('-'):
        brushSize = max(1, brushSize - 1)
    elif key == ord('c'):
        canvas = np.zeros((1080, 1920, 3), np.uint8)
    elif key == ord('u'):
        if len(history) > 0:
            canvas = history.pop().copy()
    elif key == ord('s'): # 4. Save Artwork Feature
        timestampStr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"artwork_{timestampStr}.png"
        cv2.imwrite(filename, canvas)
        print(f"Artwork saved as {filename}!")

    # put colors button
    colorsBtn.drawRect(frame)
    cv2.rectangle(frame, (colorsBtn.x, colorsBtn.y), (colorsBtn.x + colorsBtn.w, colorsBtn.y + colorsBtn.h),
                  (255, 255, 255), 2)

    # put white board buttin
    boardBtn.drawRect(frame)
    cv2.rectangle(frame, (boardBtn.x, boardBtn.y), (boardBtn.x + boardBtn.w, boardBtn.y + boardBtn.h), (255, 255, 255),
                  2)

    # put the white board on the frame
    if not hideBoard:
        whiteBoard.drawRect(frame)
        # Fast canvas blending
        mask = canvas.any(axis=-1)
        frame[mask] = canvas[mask]

    # Show active shape mode
    shape_name = ["Circle", "Rectangle", "Triangle", "Line"][shape_to_draw - 1]
    cv2.putText(frame, f"Shape: {shape_name} (Hang Loose to swap)", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    ########## pen colors' boxes #########
    if not hideColors:
        for c in colors:
            c.drawRect(frame)
            cv2.rectangle(frame, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 255), 2)

        clear.drawRect(frame)
        cv2.rectangle(frame, (clear.x, clear.y), (clear.x + clear.w, clear.y + clear.h), (255, 255, 255), 2)
        
        undoBtn.drawRect(frame)
        cv2.rectangle(frame, (undoBtn.x, undoBtn.y), (undoBtn.x + undoBtn.w, undoBtn.y + undoBtn.h), (255, 255, 255), 2)

    ########## brush size boxes ######
    penBtn.color = color
    penBtn.drawRect(frame)
    cv2.rectangle(frame, (penBtn.x, penBtn.y), (penBtn.x + penBtn.w, penBtn.y + penBtn.h), (255, 255, 255), 2)
    if not hidePenSizes:
        for pen in pens:
            pen.drawRect(frame)
            cv2.rectangle(frame, (pen.x, pen.y), (pen.x + pen.w, pen.y + pen.h), (255, 255, 255), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(frame, str(int(fps)), (1400, 40), cv2.FONT_HERSHEY_PLAIN, 3,
                (6, 229, 20), 3)

    cv2.imshow('video', frame)

    # cv2.imshow('canvas', canvas)
cap.release()
cv2.destroyAllWindows()

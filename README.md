<div align="center">
  <h1>🎨 AirCanvas: Sci-Fi Hand-Tracking Virtual Whiteboard</h1>
  <p><i>A next-generation, touchless interface for drawing in mid-air using Computer Vision and Machine Learning.</i></p>
</div>

---

## 🌟 Overview

**AirCanvas** pushes the boundaries of human-computer interaction by transforming your webcam into a highly responsive, 3D spatial canvas. Utilizing advanced Machine Learning models, the application tracks the skeletal structure of your hand in real-time, translating complex multi-finger gestures into seamless drawing operations.

Gone are the days of jittery, unreliable webcam drawing tools. AirCanvas boasts a completely custom-built heuristic engine designed to ignore flaky anatomical tracking points (like the thumb), resulting in an incredibly robust and professional-grade touchless interface.

---

## 🚀 Key Features Deep-Dive

### 1. 3D Depth-Sensing Dynamic Brush
Unlike traditional 2D trackers, AirCanvas extracts the **Z-coordinate (depth)** of your index finger from the neural network. As you physically move your hand closer to or further from the webcam, the brush thickness dynamically scales in real-time. This provides an unprecedented level of tactile feedback, making it feel like you are pressing a physical marker against a virtual glass pane.

### 2. Magic Shape Engine
Why settle for freehand squiggles when you can conjure perfect geometry? By engaging a "Pinch" gesture, the system locks your starting coordinates. As you drag your hand through space, a live preview of the shape renders on your screen. Release the pinch, and the shape is instantly committed to the canvas.
* **Available Shapes:** Perfect Circles, Rectangles, Isosceles Triangles, and Straight Lines.
* **Hands-Free Toggling:** Cycle between these shapes using a dedicated "Rock On" hand gesture without ever touching your keyboard.

### 3. Bulletproof Gesture Recognition
Standard AI hand models notoriously struggle with thumb detection when the hand rotates. AirCanvas circumvents this by utilizing a proprietary gesture mapping system that strictly evaluates the 4 primary fingers (Index, Middle, Ring, Pinky). 
* **The Result:** 100% reliable gesture detection that never triggers accidental brush strokes or ghost inputs, even in suboptimal lighting conditions.

### 4. Multi-Tiered Undo Architecture
Made a mistake? The application maintains a rolling state-history buffer of your canvas.
* Instantly revert actions by holding up your **Pinky Finger**.
* Hover over the floating **UI Undo Button**.
* Or use the traditional `u` key on your keyboard.

### 5. Linear Interpolation Smoothing
Raw webcam coordinates are noisy. AirCanvas passes all skeletal data points through a highly tuned linear interpolation filter. This mathematical smoothing completely eliminates hand jitter, ensuring your strokes look buttery smooth and professionally drawn.

---

## 🖐️ The Gesture Lexicon

Control the entire application without ever touching your mouse. Our gesture engine is designed to be completely distinct and overlap-free.

| Action | Required Gesture | Technical Behavior |
| :--- | :--- | :--- |
| **Hover / UI Select** | ✌️ **Index & Middle Up** | Renders a cursor but suspends drawing to the canvas. Used to hover over UI buttons or select colors. |
| **Draw (Freehand)** | ☝️ **Index Finger Only** | Commits strokes to the canvas with dynamic z-axis thickness scaling. |
| **Eraser Mode** | ✌️ **Index & Middle Up** | While hovering inside the designated whiteboard zone, this gesture acts as a wide-radius eraser. |
| **Undo Last Action** | 🤙 **Pinky Finger Only** | Pops the last saved state from the history buffer. |
| **Cycle Shapes** | 🤘 **Index & Pinky Up** | Cycles the active shape mode (Circle ➔ Rectangle ➔ Triangle ➔ Line). |
| **Draw Shape** | 🤏 **Index & Thumb Pinch** | Anchors the starting coordinates. Drag to adjust size, release pinch to commit. |
| **Wipe Canvas** | 🖐️ **Four Fingers Up** | Instantly clears all drawing data and resets the board. |

---

## ⌨️ Fallback Keyboard Controls

While designed to be entirely hands-free, the following shortcuts are available:
* `s` - **Save Artwork:** Automatically captures the canvas and saves it to the root directory with a unique timestamp (e.g., `artwork_20240819_120530.png`).
* `c` - **Clear Canvas:** Wipes the board clean.
* `u` - **Undo:** Reverts the last stroke or shape.
* `Esc` - **Terminate:** Safely closes the application and releases the camera hardware.

---

## 🛠️ Architecture & Setup

### Tech Stack
* **Python 3.12+**
* **OpenCV (cv2):** For high-performance matrix operations, image blending, and UI rendering.
* **MediaPipe Tasks API:** Google's state-of-the-art ML framework for sub-millisecond skeletal landmark extraction.
* **NumPy:** For lightning-fast boolean masking when compositing the drawing canvas over the live webcam feed.

### Installation

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Boot the engine:
   ```bash
   python main.py
   ```

*Note: For the best experience, ensure your room is reasonably well-lit and your webcam is positioned at eye-level.*

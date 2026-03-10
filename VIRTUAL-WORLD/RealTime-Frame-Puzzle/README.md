# 🧩 Real-Time Frame Puzzle

An interactive puzzle game that converts live webcam feed or static photos into solvable puzzles, controlled entirely by hand gestures using computer vision technology.

## 📍 Current Status

**Version:** Alpha v0.3 (Commit 3/12)  
**Status:** ✅ Core Infrastructure Complete | 🚧 Gameplay Features In Development

### What's Working Now:
- ✅ Webcam capture with live preview
- ✅ Image file loading
- ✅ Difficulty selection (3×3, 4×4, 5×5)
- ✅ Puzzle grid generation
- ✅ Visual grid display with piece numbers

### Coming Next:
- 🔜 Puzzle shuffling (Commit 4)
- 🔜 Hand gesture integration (Commit 5+)
- 🔜 Drag & drop gameplay (Commits 6-8)

## 📝 Description

This project combines computer vision, hand tracking, and game development to create an immersive puzzle-solving experience. Capture a frame from your webcam or load an image, and watch it transform into an interactive puzzle that you can solve using natural hand gestures—no mouse or keyboard required!

## ✨ Features

### ✅ Currently Implemented (Commits 1-3)
- **📸 Live Webcam Frame Capture** - Capture any moment from your webcam to create a unique puzzle
- **🖼️ Image Loading** - Load images from file path
- **🎯 Multiple Difficulty Levels** - Choose from 3x3 (Easy), 4x4 (Medium), or 5x5 (Hard) grids
- **🧩 Puzzle Grid Generation** - Automatic splitting of images into puzzle pieces
- **🎨 Visual Grid Display** - Clean grid layout with piece numbers and borders
- **📊 Frame Preprocessing** - Intelligent resizing and quality checks

### 🚧 Coming Soon (Commits 4-12)
- **🔀 Puzzle Shuffling** - Randomize pieces for gameplay
- **🖐️ Hand Gesture Drag & Drop** - Use natural hand gestures to move puzzle pieces
- **🏆 Win Detection** - Automatic detection when puzzle is solved
- **⏱️ Performance Tracking** - Track your time and number of moves
- **✨ Animation Effects** - Smooth transitions and visual feedback

## 🛠️ Technology Stack

- **Python 3.8+** - Core programming language
- **OpenCV** - Computer vision and image processing
- **NumPy** - Numerical computations and array operations
- **MediaPipe** - Hand tracking and gesture recognition (via parent HandDetector)

## 📦 Installation

### Prerequisites

```bash
# Ensure Python 3.8 or higher is installed
python --version
```

### Install Dependencies

```bash
# Navigate to project directory
cd VIRTUAL-WORLD/RealTime-Frame-Puzzle

# Install required packages
pip install -r requirements.txt
```

## 🚀 Usage

### Step-by-Step Instructions

```bash
# Run the puzzle game
python main.py
```

**1. Main Menu**
   - Press **'W'** to capture from webcam
   - Press **'F'** to load from file
   - Press **'ESC'** to exit

**2. Capture/Load Image**
   - **Webcam Mode**: Live preview appears
     - Press **SPACE** to capture current frame
     - Press **ESC** to cancel
   - **File Mode**: Enter image file path when prompted

**3. Select Difficulty**
   - Press **'3'** for Easy (3×3 = 9 pieces)
   - Press **'4'** for Medium (4×4 = 16 pieces)
   - Press **'5'** for Hard (5×5 = 25 pieces)
   - Press **'ESC'** to go back

**4. View Puzzle Grid**
   - Puzzle grid is displayed with numbered pieces
   - Grid shows difficulty level and piece count
   - Currently displays unsolved grid (shuffling coming in Commit 4)

### Game Modes

#### 1. 📸 Webcam Mode (Available Now)
- Captures live frame from your webcam
- Real-time preview with instructions
- High-quality frame capture (640×480 → 600×600)
- Automatic brightness quality check

#### 2. 🖼️ File Mode (Available Now)
- Load existing images from file path
- Supports common formats (JPG, PNG, etc.)
- Automatic image preprocessing and resizing

### Difficulty Levels

| Level | Grid Size | Total Pieces | Piece Size | Difficulty |
|-------|-----------|--------------|------------|-----------|
| **Easy** | 3×3 | 9 pieces | 200×200 px | ⭐ Beginner |
| **Medium** | 4×4 | 16 pieces | 150×150 px | ⭐⭐ Intermediate |
| **Hard** | 5×5 | 25 pieces | 120×120 px | ⭐⭐⭐ Advanced |

## 🎮 Controls

### Current Keyboard Controls

#### Main Menu
- **'W' or 'w'** - Select Webcam Mode
- **'F' or 'f'** - Select File Mode
- **'ESC'** - Exit Game

#### Webcam Capture
- **SPACE** - Capture current frame
- **ESC** - Cancel and go back to menu

#### Difficulty Selection
- **'3'** - Easy (3×3 Grid)
- **'4'** - Medium (4×4 Grid)
- **'5'** - Hard (5×5 Grid)
- **'ESC'** - Go back to main menu

#### During Puzzle Display
- **Any Key** - Continue to next step

### 🚧 Hand Gestures (Coming Soon)
- **Pinch (Thumb + Index)** - Select/Grab piece
- **Move Hand** - Drag piece
- **Release Pinch** - Drop piece
- **Open Palm** - Reset puzzle
- **Swipe Left** - Return to menu

## 🏗️ Project Structure

```
RealTime-Frame-Puzzle/
├── main.py              # Main entry point and game logic
│   ├── FrameCapture    # Webcam & image loading class
│   ├── PuzzlePiece     # Individual puzzle piece class
│   ├── PuzzleGrid      # Grid management class
│   ├── show_menu()     # Main menu function
│   ├── select_difficulty() # Difficulty selection
│   └── main()          # Main game loop
├── README.md            # Project documentation (this file)
├── requirements.txt     # Python dependencies
└── .gitignore          # Git ignore rules
```

### Class Overview

**FrameCapture**
- `capture_from_webcam()` - Captures frame from webcam with live preview
- `load_from_file(filepath)` - Loads image from file path
- `preprocess_frame(frame)` - Resizes and prepares frame (600×600)
- `release()` - Cleanup webcam resources

**PuzzlePiece**
- Stores: piece ID, image data, positions, rendering rectangle
- `is_correct_position()` - Checks if piece is in correct location

**PuzzleGrid**
- `create_pieces()` - Splits image into N×N grid pieces
- `draw_grid()` - Renders puzzle with borders and info
- `get_piece_info()` - Returns grid statistics

## 🔧 Development Roadmap

### ✅ Completed
- [x] **Commit 1:** Project setup and basic structure
  - Created folder structure
  - Added main.py, README.md, requirements.txt, .gitignore
  - Initialized project with proper imports and path configuration

- [x] **Commit 2:** Webcam capture & frame processing
  - Implemented FrameCapture class
  - Webcam capture with live preview
  - File loading functionality
  - Frame preprocessing (600×600 with aspect ratio preservation)
  - Menu system for input source selection
  - Brightness quality checks

- [x] **Commit 3:** Puzzle grid creation
  - Created PuzzlePiece class
  - Created PuzzleGrid class
  - Difficulty selection menu (3×3, 4×4, 5×5)
  - Image splitting into grid pieces
  - Grid rendering with borders and piece numbers
  - Grid information display

### 🚧 In Progress
- [ ] **Commit 4:** Puzzle shuffling logic
- [ ] **Commit 5:** Hand gesture integration
- [ ] **Commit 6:** Piece selection & snap mechanism
- [ ] **Commit 7:** Drag & drop functionality
- [ ] **Commit 8:** Piece swapping logic
- [ ] **Commit 9:** Win condition & validation
- [ ] **Commit 10:** UI enhancements & menu
- [ ] **Commit 11:** Visual polish & effects
- [ ] **Commit 12:** Documentation & final testing

## � Example Output

When you run the program, you'll see console output like this:

```
================================================================================
🧩 Real-Time Frame Puzzle - Starting...
================================================================================

[MENU] Waiting for user input...
[MENU] Press 'W' for Webcam, 'F' for File, 'ESC' to Exit
[INFO] FrameCapture initialized

[INFO] Webcam capture mode selected

[INFO] Webcam opened successfully
[INFO] Press SPACE to capture, ESC to exit
[SUCCESS] Frame captured!
[INFO] Webcam resources released

[INFO] Preprocessing frame...
[INFO] Original frame size: 640x480
[INFO] Frame brightness: 110.37
[SUCCESS] Frame preprocessed to: 600x600

[MENU] Select difficulty level...
[INFO] Medium mode selected (4×4)

[INFO] Creating puzzle pieces...
[INFO] Grid size: 4×4
[INFO] Piece dimensions: 150×150 pixels
[SUCCESS] Created 16 puzzle pieces!

============================================================
PUZZLE GRID INFORMATION
============================================================
Grid Size:      4×4
Total Pieces:   16
Piece Size:     150×150 pixels
Canvas Size:    700×700 pixels
============================================================

[SUCCESS] Puzzle grid created successfully!
```

### Visual Windows Displayed:
1. **Main Menu** - Input source selection
2. **Webcam Preview** - Live feed with capture instructions
3. **Puzzle Source Image** - Captured/loaded image
4. **Difficulty Selection** - Grid size options
5. **Puzzle Grid** - Generated puzzle with piece numbers

## 🔧 Troubleshooting

### Webcam Not Opening
**Problem:** `[ERROR] Could not access webcam!`

**Solutions:**
- Check if webcam is connected and working
- Close other applications using the webcam (Skype, Teams, etc.)
- Try changing webcam index in code: `cv2.VideoCapture(0)` → `cv2.VideoCapture(1)`
- Check webcam permissions in Windows Settings

### Image File Not Loading
**Problem:** `[ERROR] File not found` or `[ERROR] Failed to load image`

**Solutions:**
- Verify the file path is correct (use absolute path)
- Check file format is supported (JPG, PNG, BMP)
- Ensure the image file is not corrupted
- Try using forward slashes: `C:/path/to/image.jpg`

### Display Issues
**Problem:** Windows not showing or appearing blank

**Solutions:**
- Update OpenCV: `pip install --upgrade opencv-python`
- Check if display is available (required for cv2.imshow)
- Press any key if window seems frozen
- Try running with administrator privileges

### Low Frame Quality
**Problem:** `[WARNING] Frame is very dark/bright`

**Solutions:**
- Adjust room lighting for webcam mode
- Use higher quality source images for file mode
- Clean webcam lens
- Adjust image brightness before loading

### Dependencies Not Installing
**Problem:** Error during `pip install -r requirements.txt`

**Solutions:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Install packages individually
pip install opencv-python
pip install numpy
pip install mediapipe

# Or use specific versions
pip install opencv-python==4.8.0 numpy==1.24.0 mediapipe==0.10.0
```
## ✅ Testing & Verification

### Commit 1 - Project Setup
```bash
# Should print startup message and exit cleanly
python main.py
```
Expected: Initialization messages display successfully

### Commit 2 - Webcam & Frame Processing
**Test Webcam Mode:**
1. Run program → Press 'W'
2. Webcam opens with live preview
3. Press SPACE to capture
4. Frame displays at 600×600 resolution

**Test File Mode:**
1. Run program → Press 'F'
2. Enter valid image path
3. Image loads and displays at 600×600

**Expected Output:**
- Webcam opens successfully
- Frame captured with green border
- Brightness check displays
- No errors in preprocessing

### Commit 3 - Puzzle Grid Creation
**Test All Difficulties:**
1. Capture/load image
2. Try each difficulty (3, 4, 5)
3. Verify piece counts: 9, 16, 25

**Verification Checklist:**
- ✅ Difficulty menu displays correctly
- ✅ 3×3 creates 9 pieces (200×200 px each)
- ✅ 4×4 creates 16 pieces (150×150 px each)
- ✅ 5×5 creates 25 pieces (120×120 px each)
- ✅ Piece numbers visible in corners
- ✅ White borders between pieces
- ✅ Grid info overlay shows correct data

**Expected Console Output:**
```
[INFO] Creating puzzle pieces...
[INFO] Grid size: 4×4
[INFO] Piece dimensions: 150×150 pixels
[DEBUG] Piece 1: pos(0,0), rect(50, 50, 150, 150)
...
[SUCCESS] Created 16 puzzle pieces!
```
## �👤 Author

**ANUBHAV YADAV**  
B. Tech Student  
Date: March 10, 2026

## 📄 License

All rights reserved. This project is part of the Gesture Control Interface suite.

## 🤝 Contributing

This is a personal project. For inquiries, please contact the author.

---

*Part of the Gesture Control Interface Project*


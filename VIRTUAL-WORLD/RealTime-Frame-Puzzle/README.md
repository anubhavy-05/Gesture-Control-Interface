# 🧩 Real-Time Frame Puzzle

An interactive puzzle game that converts live webcam feed or static photos into solvable puzzles, controlled entirely by hand gestures using computer vision technology.

## 📝 Description

This project combines computer vision, hand tracking, and game development to create an immersive puzzle-solving experience. Capture a frame from your webcam or load an image, and watch it transform into an interactive puzzle that you can solve using natural hand gestures—no mouse or keyboard required!

## ✨ Features

- **📸 Live Webcam Frame Capture** - Capture any moment from your webcam to create a unique puzzle
- **🖼️ Image to Puzzle Conversion** - Transform photos into scrambled puzzle pieces
- **🖐️ Hand Gesture Drag & Drop** - Use natural hand gestures to move puzzle pieces
- **🎯 Multiple Difficulty Levels** - Choose from 3x3 (Easy), 4x4 (Medium), or 5x5 (Hard) grids
- **🏆 Win Detection** - Automatic detection when puzzle is solved
- **⏱️ Performance Tracking** - Track your time and number of moves
- **🎨 Visual Feedback** - Real-time visual effects and smooth animations

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

```bash
# Run the puzzle game
python main.py
```

### Game Modes
*(To be implemented)*

1. **Webcam Mode** - Capture a live frame from your webcam
2. **Image Mode** - Load an existing image file

### Difficulty Levels
*(To be implemented)*

- **Easy (3x3)** - 9 puzzle pieces
- **Medium (4x4)** - 16 puzzle pieces
- **Hard (5x5)** - 25 puzzle pieces

## 🎮 Controls

*(Controls will be detailed as features are implemented)*

### Hand Gestures
- **TBD** - Piece selection
- **TBD** - Drag piece
- **TBD** - Drop piece
- **TBD** - Reset puzzle
- **TBD** - Return to menu

## 🏗️ Project Structure

```
RealTime-Frame-Puzzle/
├── main.py              # Main entry point
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── (modules to be added)
```

## 🔧 Development Roadmap

- [x] **Commit 1:** Project setup and basic structure
- [ ] **Commit 2:** Webcam capture & frame processing
- [ ] **Commit 3:** Puzzle grid creation
- [ ] **Commit 4:** Puzzle shuffling logic
- [ ] **Commit 5:** Hand gesture integration
- [ ] **Commit 6:** Piece selection & snap mechanism
- [ ] **Commit 7:** Drag & drop functionality
- [ ] **Commit 8:** Piece swapping logic
- [ ] **Commit 9:** Win condition & validation
- [ ] **Commit 10:** UI enhancements & menu
- [ ] **Commit 11:** Visual polish & effects
- [ ] **Commit 12:** Documentation & final testing

## 👤 Author

**ANUBHAV YADAV**  
B. Tech Student  
Date: March 10, 2026

## 📄 License

All rights reserved. This project is part of the Gesture Control Interface suite.

## 🤝 Contributing

This is a personal project. For inquiries, please contact the author.

---

*Part of the Gesture Control Interface Project*

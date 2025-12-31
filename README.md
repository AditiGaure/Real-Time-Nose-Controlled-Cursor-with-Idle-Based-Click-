# Real-Time-Nose-Controlled-Cursor-with-Idle-Based-Click-
🔹Project Title

Real-Time Nose-Controlled Cursor with Idle-Based Click


🔹Description

A real-time computer vision–based accessibility system that enables hands-free mouse control using facial landmark detection.

The system tracks the nose tip to control cursor movement and uses an idle-based auto-click mechanism to prevent unintended clicks.

Designed to improve human–computer interaction for users with limited mobility.


🔹Key Features

-Real-time nose-tip tracking using MediaPipe FaceMesh

-Hands-free cursor movement through facial landmark detection

-Idle-based auto-click system (click triggers only after cursor remains stable for a fixed duration)

-Support for multiple mouse actions:

-Left click

-Right click

-Toggle-based click activation to enable or disable clicking anytime

-Clicks are triggered only within defined regions to avoid accidental actions

-Fully real-time processing using live webcam input


🔹Technologies Used

-Python

-OpenCV

-MediaPipe FaceMesh

-Computer Vision

-Real-Time Video Processing


🔹Project Structure

-nose_controlled_cursor.py – Main implementation file containing:

-Face landmark detection

-Cursor movement logic

-Idle-based click automation

-Toggle-based click control


🔹How It Works

1.Captures live video from the webcam.

2.Detects facial landmarks using MediaPipe FaceMesh.

3.Tracks the nose-tip position to move the mouse cursor.

4.Monitors cursor stability:

5.Mouse click is triggered only if the cursor remains idle for a fixed duration.

6.Toggle zones allow enabling or disabling click actions dynamically.


🔹Note

-The trained model file is not included in this repository due to size constraints and ownership concerns.

-The complete architecture, logic, and inference code are provided for understanding and reproduction.



🔹Author

Aditi Gaure

Computer Science and Engineering Student




🔹Disclaime:

This project and its source code are original work developed solely by the author. Any unauthorized copying, redistribution, reproduction, or use of this code or its implementation—in full or in part—is strictly prohibited without prior written permission.


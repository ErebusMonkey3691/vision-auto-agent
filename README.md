# Vision-Driven Autonomous Framework
### State-Machine Automation via Chromatic Perception

> **Development Note:** This repository represents a finalized, template-agnostic version 
> of a vision-based automation tool developed in ~[Aug/2025]. This version has been 
> specifically refactored to remove proprietary assets and focus on the underlying 
> computer vision logic and Win32 API integration.

## Project Overview
This project implements a non-intrusive autonomous agent designed to interact with graphical user interfaces (GUIs) through **Computer Vision (CV)** and the **Win32 API**. By utilizing real-time screen sampling and RGB color-space analysis, the agent can perceive application states and execute context-aware actions.

The framework is built to be robust against UI shifts by employing a Euclidean distance threshold for visual verification rather than relying on static coordinate clicks.



## Ethical Compliance & Design Philosophy
To respect Intellectual Property and adhere to the **Terms of Service (ToS)** of third-party software:
* **Template-Agnostic Design**: Proprietary assets and game-specific templates are **not included** in this repository. 
* **Framework Orientation**: This project is presented as a general-purpose automation tool for **Human-Computer Interaction (HCI)** research.
* **User-Provided Assets**: Users must generate their own reference templates for their specific application environment.

## Technical Architecture

### 1. The Autonomous Loop (`vision_agent.py`)
This is the primary execution engine. It manages the lifecycle of the agent:
* **Asynchronous Safety Thread**: Implements a `threading` listener for a hardware "Kill Switch" (ESC key) to ensure immediate script termination.
* **Chromatic State Detection**: Instead of pixel-matching, the agent uses a custom `average_color` function to calculate the mean RGB value of a Region of Interest (ROI). This method provides resilience against anti-aliasing and minor rendering variances.
* **Validation Logic**: Uses a multi-stage conditional check with a defined threshold: 
  $$all(abs(a - b) < \text{threshold} \text{ for } a, b \text{ in zip(screenshot, reference)})$$
* **Position Restoration**: Captures the initial cursor position (`og_pos`) and returns the mouse to the user after task completion to minimize interference.

### 2. The Capture Utility (`capture_utils.py`)
A low-level utility for generating high-fidelity reference templates:
* **GDI+ Integration**: Directly interfaces with the Windows Graphics Device Interface via `ctypes.windll.user32.PrintWindow`.
* **Direct Bitmap Manipulation**: Captures the device context (DC) of a specific window handle (`hwnd`), allowing for standardized screenshots regardless of window focus or scaling.

## System Workflow
1. **Calibration**: `vision_agent.py` is used to capture the standard UI state.
2. **Initialization**: `capture_utils.py` standardizes the target window to an $800 \times 600$ coordinate space.
3. **Perception**: The agent crops specific UI regions and compares their chromatic profile to reference templates.
4. **Decision**: If a match is verified (even with positional offsets), the agent dispatches input events.
5. **Termination**: The loop breaks once a "final state" (e.g., combat completion) is visually detected.

## Installation & Requirements
* **OS**: Windows (Required for `pywin32` and `GDI` calls).
* **Dependencies**: `pyautogui`, `Pillow`, `keyboard`, `pywin32`.
* **Setup**: Place custom reference templates (`reference_button.png`, etc.) in the root directory before execution.

# WinPet

WinPet is a lightweight Windows desktop companion application.
It displays an animated character that lives on your desktop, stays on top of other windows, and can be freely moved and customized through a system tray interface.

The application is designed to be simple for users while remaining easy to extend and modify for developers.

---

## Features

* Animated desktop companion rendered using Qt (PySide6)
* Always-on-top, frameless window
* Smooth frame-based animation
* Click-and-drag movement
* Multiple companion “looks” (animation sets)
* Live switching between looks
* Automatic detection of newly added companions
* System tray menu for all controls
* Persistent configuration between launches
* Fully packaged standalone Windows executable

---

## System Requirements

* Windows 10 or newer

---

## Download

Download the latest Windows executable from the
[GitHub Releases](https://github.com/<your-username>/<repo-name>/releases) page.

---

# User Guide

## Getting Started

1. Download `WinPet.exe`
2. Run the executable
3. The companion appears on your desktop
4. A tray icon appears in the system tray

WinPet runs in the background and does not display a console window.

---

## Interacting with the Companion

* **Move:** Click and drag the companion anywhere on the screen
* **Pick up state:** While dragging, the companion switches to a “picked” animation
* **Idle state:** When released, the companion returns to idle animation

---

## Managing Companion Looks

### Switching Looks

1. Right-click the WinPet tray icon
2. Open **Current Look**
3. Select a look from the list

The companion updates immediately.

---

### Adding New Looks

1. Right-click the tray icon
2. Select **Open Library Folder**
3. Create a new folder for the companion
4. Add animation frames following the required format
5. Use **Refresh Looks** from the tray menu

### Companion Folder Format

```
CompanionName/
├─ idle/
│  ├─ 0.png
│  ├─ 1.png
│  └─ ...
└─ picked/
   ├─ 0.png
   ├─ 1.png
   └─ ...
```

### Requirements

* Filenames must be numeric and sequential
* Supported image formats: `.png`, `.jpg`, `.jpeg`
* Both `idle` and `picked` folders must exist
* Invalid companions are ignored automatically

---

### Removing Looks

* Delete the companion’s folder from the library
* Use **Refresh Looks** to update the menu

---

## Closing the Application

* Right-click the tray icon
* Select **Quit WinPet**

The application exits fully and leaves no background processes running.

---

# Developer Guide

## Overview

WinPet is built around three core systems:

1. **Companion Window**

   * Frameless Qt window
   * Renders animation frames using QPixmap
   * Handles user interaction and movement

2. **System Tray Controller**

   * Built with pystray
   * Provides menu-based controls
   * Manages look switching and shutdown

3. **Library & Configuration System**

   * Companion looks stored as folders
   * Active look stored in a JSON config file
   * Automatic detection of library changes

---

## Animation System

* Frames are loaded as QPixmaps
* Animations are driven by a timer at a configurable FPS
* Frame order is determined by numeric filenames
* Separate animation sequences for idle and picked states

---

## Configuration

* Configuration is stored in `config.json`
* Stores the active companion name and path
* Loaded at startup and saved on changes or exit

---

## File Locations (Runtime)

At runtime, WinPet creates and uses:

```
WinPet/
├─ data/
│  └─ config.json
└─ library/
   ├─ CompanionA/
   └─ CompanionB/
```

The exact base location depends on the system, but the application manages this automatically.

---

## Project Structure

```
WindowPet/
├─ assets/         # Bundled application assets
├─ companion/      # Companion window and animation logic
├─ core/           # App state, config, utilities
├─ tray/           # Tray menu and helpers
├─ main.py         # Application entry point
├─ WinPet.spec     # PyInstaller build file
├─ requirements.txt
└─ README.md
```

---

## Running from Source

### Requirements

* Python 3.10+
* Windows

### Setup

```bash
pip install -r requirements.txt
python main.py
```

---

## Building the Executable

WinPet is packaged using PyInstaller.

```bash
pip install pyinstaller
pyinstaller WinPet.spec --clean
```

The executable will be generated in:

```
dist/WinPet.exe
```

---

## License

This project is licensed under the MIT License with the Commons Clause.

- Non-commercial use, modification, and redistribution are permitted
- Commercial resale or paid distribution is not permitted
- Attribution to the original author is required


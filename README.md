# WinPet

WinPet is a lightweight Windows desktop companion application.

It displays an animated character that lives on your desktop, stays on top of other windows, reacts to user interaction, and idles with time-based behaviors.
All interaction and configuration is handled through a system tray interface.

WinPet is designed to be:

- Simple and intuitive for users
- Easy to extend and maintain for developers

---

## Key Highlights

- Animated desktop companion (desktop pet)
- Frameless, always-on-top window
- Smooth frame-based animations
- Click-and-drag interaction with physics
- Multiple companion looks (animation sets)
- Live look switching without restart
- Automatic detection of new companions
- Time-based idle behavior system
- State-driven animation engine
- Persistent configuration
- Standalone Windows executable (no Python required)

---

## System Requirements

- Windows 10 or newer

---

## Download

Download the latest Windows executable from the GitHub Releases page
No installation is required. Simply run the executable.

---

# User Guide

## Getting Started

1. Download `WinPet.exe`
2. Run the executable
3. A companion appears on your desktop
4. A tray icon appears in the system tray

WinPet runs quietly in the background and does not open a console window.

---

## Interacting with the Companion

### Move / Drag

- Click and drag the companion anywhere on the screen
- While dragging, the companion switches to the `picked` animation state

### Release

- Releasing the mouse drops the companion
- The companion smoothly returns to idle behavior

---

## Idle Behavior System

WinPet supports time-based idle states.

When the companion is not interacted with, it automatically transitions through idle animations based on how long it has been left alone.

### Default Idle States

| State Name    | Description                          |
| ------------- | ------------------------------------ |
| `idle`        | Default idle animation               |
| `idle_medium` | Triggered after a short idle period  |
| `idle_long`   | Triggered after a longer idle period |

### Behavior Rules

- Idle states transition automatically over time
- `idle_long` can repeat multiple times before resetting
- All states are optional except `idle`
- If a state folder does not exist, it is skipped automatically
- User interaction instantly resets the idle cycle

This system allows companions to feel more dynamic and alive without requiring configuration.

---

## Managing Companion Looks

### Switching Looks

1. Right-click the WinPet tray icon
2. Open **Current Look**
3. Select a look from the list

The companion updates immediately.

---

### Adding New Companion Looks

1. Right-click the tray icon
2. Select **Open Library Folder**
3. Create a new folder for the companion
4. Add animation frames following the required format
5. Select **Refresh Looks** from the tray menu

---

### Companion Folder Structure

```
CompanionName/
├─ idle/
│  ├─ 0.png
│  ├─ 1.png
│  └─ ...
├─ idle_medium/        (optional)
│  ├─ 0.png
│  └─ ...
├─ idle_long/          (optional)
│  ├─ 0.png
│  └─ ...
└─ picked/
   ├─ 0.png
   ├─ 1.png
   └─ ...
```

---

### Companion Rules

- Filenames must be numeric and sequential
- Supported image formats:
  - `.png`
  - `.jpg`
  - `.jpeg`

- The `idle` folder is required
- All other state folders are optional
- Invalid companions are ignored automatically

---

### Removing Companion Looks

- Delete the companion folder from the library
- Use **Refresh Looks** from the tray menu

---

## Closing WinPet

1. Right-click the tray icon
2. Select **Quit WinPet**

The application exits cleanly and leaves no background processes running.

---

# Developer Guide

## Architecture Overview

WinPet is built around three main systems.

---

### Companion Window

- Frameless `QWidget`
- Always-on-top
- Transparent background
- Renders animations using `QPixmap`
- Handles:
  - user input
  - movement
  - physics
  - animation state transitions

---

### Animation and State System

WinPet uses a state-driven animation model.

Each animation state corresponds to a folder on disk.

#### Built-in States

| State         | Purpose                         |
| ------------- | ------------------------------- |
| `idle`        | Default idle animation          |
| `idle_medium` | Medium idle duration            |
| `idle_long`   | Long idle duration (repeatable) |
| `picked`      | Active while dragging           |

#### Key Properties

- States are discovered dynamically
- No hardcoded assumptions about available states
- Missing states are skipped safely
- Active states are protected from accidental overrides
- Time-based transitions are handled by a scheduler

This design allows new states to be added without modifying core logic.

---

### System Tray Controller

- Built with `pystray`
- Provides:
  - look switching
  - size control
  - FPS control
  - enable or disable toggle
  - graceful shutdown

- Tray menu updates live when the library changes

---

### Library and Configuration System

- Companion assets are stored as folders
- Active companion data is saved in `config.json`
- Configuration persists across restarts
- The companion library is monitored and refreshed automatically

---

## Runtime File Locations

At runtime, WinPet creates and manages the following structure:

```
WinPet/
├─ data/
│  └─ config.json
└─ library/
   ├─ CompanionA/
   └─ CompanionB/
```

The base directory is platform-appropriate and managed automatically.

---

## Project Structure

```
WinPet/
├─ assets/         # Bundled application assets
├─ companion/      # Companion window and animation logic
├─ core/           # Configuration, state, and utilities
├─ tray/           # System tray menu and helpers
├─ main.py         # Application entry point
├─ WinPet.spec     # PyInstaller build configuration
├─ requirements.txt
└─ README.md
```

---

## Running From Source

### Requirements

- Python 3.10 or newer
- Windows

### Run

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

The executable will be generated at:

```
dist/WinPet.exe
```

---

## Extending WinPet

WinPet is designed with extensibility in mind.

Common extensions include:

- Adding new animation states
- Creating custom idle behavior rules
- Adding metadata per companion
- Modifying physics behavior
- Implementing emotion or context-based states

The animation and state system requires no refactoring to support new states.

---

## License

This project is licensed under the MIT License with the Commons Clause.

- Non-commercial use, modification, and redistribution are permitted
- Commercial resale or paid distribution is not permitted
- Attribution to the original author is required

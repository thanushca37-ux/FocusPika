# FocusPika ⚡

**FocusPika** is a nostalgic pixel-art Pikachu desktop productivity companion for Windows 10 and Windows 11. Inspired by the classic aesthetic of Pokémon FireRed and LeafGreen, FocusPika sits cheerfully on your desktop near the taskbar, helping you focus, manage tasks, prevent digital distractions, stay hydrated, and track daily progress.

![FocusPika Overview](assets/backgrounds/pallet_town.png)

---

## 🎨 Visual Identity & Color System

The application faithfully recreates the warm yellow-and-cream retro aesthetic:

- **Pikachu Primary Yellow**: `#FFD83D`
- **Button Yellow**: `#FFC928`
- **Title Bar Yellow**: `#FFE36E`
- **Main Cream Background**: `#FFF6CC`
- **Secondary Cream / Card Background**: `#FFF0A3`
- **Selection Highlight**: `#FFE58A`
- **Main Text**: `#202018`
- **Secondary Text**: `#655F48`
- **Dark Olive/Brown Outlines**: `#4A4329`
- **Success Green**: `#76C66E`
- **Water Blue**: `#55BDEB`
- **Error Red**: `#ED5A51`

---

## ✨ Features

### 1. Floating Desktop Companion (Pikachu)
- **Frameless & Transparent**: Only Pikachu and its cute speech bubbles are visible on the desktop.
- **Always-on-Top & Draggable**: Smoothly drag Pikachu anywhere on your screens; edge-clamping keeps it safe above the taskbar.
- **Position Persistence**: Remembers its exact screen coordinates across launches in `%LOCALAPPDATA%\FocusPika\focuspika.db`.
- **Mood Reactions**: Reacts to focus sessions (determined headband), breaks (sleeping), completed tasks (celebration sparkle), hydration (drinking glass), and friendly clicks (hearts).
- **Cute Speech Bubbles**: Occasional encouraging messages (*"Focus time!"*, *"Stay hydrated, trainer!"*, *"Pika!"*).
- **Context Menu & Double-Click**: Right-click Pikachu for quick feature access or double-click to toggle the main menu.

### 2. Focus Timer (Pomodoro System)
- Large retro digital countdown in `PressStart2P` pixel font.
- Centered Pikachu mascot reflecting current session state.
- Start, Pause, Resume, and Reset controls.
- Configurable focus (default 25 min), short break (5 min), and long break (15 min) durations.
- Visual cycle indicators (e.g. `1/4 🟡 ⚪ ⚪ ⚪`) for Pomodoro rounds.
- Monotonic clock timekeeping: completely immune to UI lag, system sleep, or minimization.
- Session recovery state stored in SQLite to recover interrupted sessions cleanly.
- Synthesized 8-bit retro audio chimes upon completion.

### 3. Tasks & Notes Manager
- **Tasks Tab**:
  - Add, edit, check off, and delete tasks.
  - Custom pixel-art checkboxes with green checkmark and strikethrough styling for completed tasks.
  - Priority levels (*High*, *Medium*, *Low*).
  - Completing a task triggers level-up chime and Pikachu celebration.
- **Notes Tab**:
  - Live search across titles and note contents.
  - Clean cream editor with automatic debounced saving (1s idle save + instant save on switch/close).
  - Last-edited timestamps.

### 4. Website Blocker & Distraction Monitor
- Master toggle switch with retro pill indicator.
- Configurable domain allowances (e.g. YouTube, Instagram, TikTok, X/Twitter, Reddit).
- Active foreground window monitoring: tracks active browser time without invasive browser extensions or system proxy modifications.
- Alerts user when daily allowance is reached.

### 5. Water Reminder & Hydration Tracker
- Visual progress bar and glasses counter (e.g. `3 / 8 glasses today`).
- Pikachu drinking sprite with *"Pika!"* reaction.
- Quick logging (+250 ml, +150 ml, +500 ml) and undo feature.
- Periodic hydration reminders respecting quiet hours.

### 6. Statistics & Progress Dashboard
- 4 Metric cards matching the 2x2 grid: Focus Time, Sessions, Water, Tasks Done.
- 7-Day retro bar chart in yellow and dark olive.
- Daily focus streak calculation.
- JSON data export for full backup and privacy.

### 7. Native Windows Integration
- System tray icon with quick actions menu and desktop notifications.
- Optional *Start with Windows* registry integration (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`), reversible anytime.
- Multi-monitor and DPI scaling support.
- Optional nostalgic Pallet Town desktop wallpaper toggle.

---

## 🚀 Installation & Running

### Requirements
- Windows 10 or Windows 11 (64-bit)
- Python 3.11+ (if running from source)

### Run from Source
```bash
git clone https://github.com/FocusPika/FocusPika.git
cd FocusPika

# Install dependencies
python -m pip install -r requirements.txt

# Run automated tests
python -m pytest tests/

# Launch FocusPika
python main.py
```

---

## 📦 Building Standalone `FocusPika.exe`

To package FocusPika into a standalone executable that runs on any compatible Windows 10/11 machine without Python:

1. Double-click **`build.bat`**, or run in terminal:
```cmd
build.bat
```
2. PyInstaller will compile all source files, bundle assets, and generate:
```
FocusPika\dist\FocusPika.exe
```
3. Copy `FocusPika.exe` to any Windows computer and double-click to run!

---

## 🔒 Privacy & Local Storage

- All user data (tasks, notes, sessions, water logs, settings) is stored locally at:
  `%LOCALAPPDATA%\FocusPika\focuspika.db`
- FocusPika is 100% offline, private, and has zero tracking, advertising, or cloud telemetry.

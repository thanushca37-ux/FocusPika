"""
FocusPika - Main Application Entry Point
Pixel-Art Pikachu Desktop Productivity Companion for Windows
"""
import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from app.config import (
    APP_NAME, APP_VERSION, ORG_NAME, init_fonts, get_asset_path
)
from app.database import Database
from app.sound_manager import SoundManager
from app.desktop_pet import DesktopPet
from app.main_window import MainMenuWindow
from app.focus_timer import FocusTimerWindow
from app.task_manager import TasksAndNotesWindow
from app.website_blocker import WebsiteBlockerWindow
from app.water_reminder import WaterReminderWindow
from app.statistics import StatisticsWindow
from app.settings import SettingsWindow
from app.system_tray import SystemTray

class FocusPikaApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(APP_NAME)
        self.app.setApplicationVersion(APP_VERSION)
        self.app.setOrganizationName(ORG_NAME)

        # Application Icon
        icon_path = get_asset_path("pikachu", "app_icon.png")
        if os.path.exists(icon_path):
            self.app.setWindowIcon(QIcon(icon_path))

        # Initialize Pixel Fonts
        init_fonts()

        # Database & Audio
        self.db = Database()
        self.sound = SoundManager.get_instance()
        self.sound.set_enabled(self.db.get_setting("sound_enabled", True))

        # Feature Windows Dictionary
        self.windows = {}

        # Initialize Components
        self._init_windows()
        self._init_pet()
        self._init_tray()
        self._connect_signals()

        # Display initial windows
        self.pet.show()
        # Default: show main menu or timer initially
        self.show_window("menu")

    def _init_windows(self):
        self.windows["menu"] = MainMenuWindow()
        self.windows["timer"] = FocusTimerWindow(self.db)
        self.windows["tasks"] = TasksAndNotesWindow(self.db)
        self.windows["blocker"] = WebsiteBlockerWindow(self.db)
        self.windows["water"] = WaterReminderWindow(self.db)
        self.windows["stats"] = StatisticsWindow(self.db)
        self.windows["settings"] = SettingsWindow(self.db)

    def _init_pet(self):
        self.pet = DesktopPet(self.db)

    def _init_tray(self):
        self.tray = SystemTray()

    def _connect_signals(self):
        # Main Menu navigation
        self.windows["menu"].navigate_requested.connect(self._handle_navigation)

        # Pet interactions
        self.pet.open_feature_requested.connect(self.show_window)
        self.pet.quit_requested.connect(self.quit_app)

        # Tray interactions
        self.tray.feature_activated.connect(self.show_window)
        self.tray.toggle_pet_requested.connect(self._toggle_pet)
        self.tray.quit_requested.connect(self.quit_app)

        # Timer reactions
        timer_win = self.windows["timer"]
        timer_win.timer_started.connect(self.pet.react_focus_start)
        timer_win.session_completed.connect(self._on_session_completed)

        # Task completion reactions
        tasks_win = self.windows["tasks"]
        tasks_win.task_completed.connect(lambda title: self.pet.react_task_completed())
        tasks_win.task_completed.connect(self.windows["stats"].reload_statistics)

        # Water logging reactions
        water_win = self.windows["water"]
        water_win.water_logged.connect(lambda ml: self.pet.react_water_logged())
        water_win.water_logged.connect(self.windows["stats"].reload_statistics)

        # Website blocker alert
        blocker_win = self.windows["blocker"]
        blocker_win.limit_breached.connect(self._on_website_limit_breached)

        # Settings changed
        settings_win = self.windows["settings"]
        settings_win.settings_changed.connect(self._on_settings_updated)

    def _handle_navigation(self, key: str):
        if key == "quit":
            self.quit_app()
        else:
            self.show_window(key)

    def show_window(self, key: str):
        if key not in self.windows:
            return

        win = self.windows[key]
        if win.isVisible():
            win.raise_()
            win.activateWindow()
        else:
            # Place window nicely on screen
            win.show()
            win.raise_()
            win.activateWindow()

        # Update menu selection state
        self.windows["menu"].set_active_item(key)

    def _toggle_pet(self):
        if self.pet.isVisible():
            self.pet.hide()
        else:
            self.pet.show()

    def _on_session_completed(self, session_type: str, minutes: int):
        self.windows["stats"].reload_statistics()
        if session_type == "focus":
            self.tray.show_notification(
                f"{APP_NAME} - Focus Completed!",
                f"Great job, trainer! Completed a {minutes}-minute focus session!"
            )
            self.pet.react_break_start(is_long=False)
        elif session_type == "long_break":
            self.tray.show_notification(
                f"{APP_NAME} - Long Break Finished",
                "Ready for the next productive adventure!"
            )
            self.pet.set_mood(self.pet.animator._current_mood.IDLE)
        else:
            self.tray.show_notification(
                f"{APP_NAME} - Break Finished",
                "Time to get back in the zone!"
            )

    def _on_website_limit_breached(self, site_name: str):
        self.tray.show_notification(
            f"{APP_NAME} - Time Limit Reached",
            f"You have reached your daily allowance for {site_name}!"
        )
        self.pet.say(f"Time limit for {site_name} reached!", duration_ms=5000)

    def _on_settings_updated(self):
        self.sound.set_enabled(self.db.get_setting("sound_enabled", True))
        scale = self.db.get_setting("pet_scale", 1.0)
        self.pet.animator.set_scale(scale)
        self.pet._update_window_size()
        self.pet.animator.set_animation_enabled(self.db.get_setting("pet_animation_enabled", True))
        self.pet._speech_enabled = self.db.get_setting("speech_bubbles_enabled", True)

        # Update timer durations
        timer_win = self.windows["timer"]
        timer_win.focus_duration = self.db.get_setting("focus_duration_mins", 25) * 60
        timer_win.short_break_duration = self.db.get_setting("short_break_mins", 5) * 60
        timer_win.long_break_duration = self.db.get_setting("long_break_mins", 15) * 60
        timer_win.auto_start_next = self.db.get_setting("auto_start_transitions", False)

        # Update water goal
        water_win = self.windows["water"]
        water_win.daily_goal_ml = self.db.get_setting("water_goal_ml", 2000)
        water_win.reload_water_stats()

    def quit_app(self):
        timer_win = self.windows["timer"]
        if timer_win.is_running and self.db.get_setting("confirm_quit_during_session", True):
            ans = QMessageBox.question(
                None, "Active Focus Session",
                "A focus session is currently running! Are you sure you want to quit FocusPika?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if ans != QMessageBox.Yes:
                return

        self.pet._save_position()
        self.app.quit()

    def run(self) -> int:
        return self.app.exec()


def main():
    app = FocusPikaApp()
    sys.exit(app.run())

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Microphone Volume Keeper - Advanced Version
Advanced version with configurable settings:
- Audio device selection
- Adjustable sampling rate
- Adjustable target volume
- Persistent saved settings
"""

import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import pystray
from PIL import Image, ImageDraw
import logging
import subprocess
import json
import os

# Logging konfigurieren - NUR in Datei, KEIN Terminal-Output mehr!
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('microphone_keeper.log')
        # StreamHandler entfernt für Silent-Modus
    ]
)

class SettingsDialog:
    """Dialog for program settings"""

    def __init__(self, parent, current_settings):
        self.parent = parent
        self.result = None
        self.current_settings = current_settings.copy()

        # Create and hide main tkinter root
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window

        # Create dialog
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title("🎤 Microphone Volume Keeper - Settings")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")

        self.create_widgets()

    def create_widgets(self):
        """Creates the dialog widgets"""

        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="🎤 Microphone Volume Keeper",
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Audio-Device Auswahl
        ttk.Label(main_frame, text="Audio Device:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5))

        self.device_var = tk.StringVar(value=self.current_settings.get('device', 'Standard'))
        self.device_combo = ttk.Combobox(main_frame, textvariable=self.device_var,
                                        width=40, state="readonly")
        self.device_combo.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        # Load available devices
        self.load_audio_devices()

        # Ziel-Lautstärke
        ttk.Label(main_frame, text="Target Volume:", font=("Arial", 10, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5))

        volume_frame = ttk.Frame(main_frame)
        volume_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        self.volume_var = tk.IntVar(value=self.current_settings.get('target_volume', 100))
        self.volume_scale = ttk.Scale(volume_frame, from_=1, to=100,
                                     variable=self.volume_var, orient=tk.HORIZONTAL)
        self.volume_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        self.volume_label = ttk.Label(volume_frame, text="100%")
        self.volume_label.grid(row=0, column=1)

        # Scale update callback
        self.volume_scale.configure(command=self.update_volume_label)
        self.update_volume_label(self.volume_var.get())

        # Abtastrate
        ttk.Label(main_frame, text="Sampling Rate:", font=("Arial", 10, "bold")).grid(
            row=5, column=0, sticky=tk.W, pady=(0, 5))

        rate_frame = ttk.Frame(main_frame)
        rate_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        self.rate_var = tk.DoubleVar(value=self.current_settings.get('check_interval', 0.5))
        self.rate_scale = ttk.Scale(rate_frame, from_=0.1, to=5.0,
                                   variable=self.rate_var, orient=tk.HORIZONTAL)
        self.rate_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        self.rate_label = ttk.Label(rate_frame, text="0.5s")
        self.rate_label.grid(row=0, column=1)

        # Rate-Update-Callback
        self.rate_scale.configure(command=self.update_rate_label)
        self.update_rate_label(self.rate_var.get())

        # Info-Text
        info_text = ("💡 Tips:\n"
                    "• Lower sampling rate = Faster response\n"
                    "• Default device = Automatic detection\n"
                    "• Settings are automatically saved")

        info_label = ttk.Label(main_frame, text=info_text,
                              font=("Arial", 9), foreground="gray")
        info_label.grid(row=7, column=0, columnspan=2, pady=(10, 20), sticky=tk.W)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=(10, 0))

        ttk.Button(button_frame, text="✅ OK", command=self.ok_clicked).grid(
            row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="❌ Cancel", command=self.cancel_clicked).grid(
            row=0, column=1)

        # Grid configuration
        main_frame.columnconfigure(0, weight=1)
        volume_frame.columnconfigure(0, weight=1)
        rate_frame.columnconfigure(0, weight=1)

    def load_audio_devices(self):
        """Loads available audio devices"""
        devices = ["Default (Automatic)"]

        try:
            # Versuche AudioDeviceCmdlets zu verwenden
            result = subprocess.run([
                'powershell', '-Command',
                'Import-Module AudioDeviceCmdlets -ErrorAction SilentlyContinue; '
                'Get-AudioDevice -List | Where-Object {$_.Type -eq "Recording"} | '
                'Select-Object -ExpandProperty Name'
            ], capture_output=True, text=True, timeout=10, encoding='utf-8',
            creationflags=subprocess.CREATE_NO_WINDOW)

            if result.returncode == 0 and result.stdout.strip():
                device_names = [line.strip() for line in result.stdout.strip().split('\n')
                               if line.strip()]
                devices.extend(device_names)

        except Exception as e:
            logging.warning(f"Konnte Audio-Geräte nicht laden: {e}")

        self.device_combo['values'] = devices

        # Aktuelles Gerät auswählen falls vorhanden
        current_device = self.current_settings.get('device', 'Default (Automatic)')
        if current_device in devices:
            self.device_var.set(current_device)
        else:
            self.device_var.set("Default (Automatic)")

    def update_volume_label(self, value):
        """Updates the volume label"""
        self.volume_label.config(text=f"{int(float(value))}%")

    def update_rate_label(self, value):
        """Updates the sampling rate label"""
        self.rate_label.config(text=f"{float(value):.1f}s")

    def ok_clicked(self):
        """OK button clicked"""
        self.result = {
            'device': self.device_var.get(),
            'target_volume': int(self.volume_var.get()),
            'check_interval': round(float(self.rate_var.get()), 1)
        }
        self.dialog.destroy()
        self.root.quit()  # Beende die tkinter-Hauptschleife

    def cancel_clicked(self):
        """Cancel button clicked"""
        self.result = None
        self.dialog.destroy()
        self.root.quit()  # Beende die tkinter-Hauptschleife

    def show(self):
        """Shows the dialog and waits for result"""
        self.dialog.wait_window()
        self.root.destroy()  # Zerstöre das Root-Fenster komplett
        return self.result


class MicrophoneVolumeKeeperAdvanced:
    """Advanced version with configurable settings"""

    def __init__(self):
        # Default settings
        self.default_settings = {
            'device': 'Default (Automatic)',
            'target_volume': 100,
            'check_interval': 0.5
        }

        # Load settings
        self.settings = self.load_settings()

        # Applicable settings
        self.target_volume = self.settings['target_volume']
        self.check_interval = self.settings['check_interval']
        self.selected_device = self.settings['device']

        # System variables
        self.running = False
        self.icon = None
        self.monitor_thread = None
        self.audio_method = None

        # For intelligent logging
        self.last_volume = None
        self.correction_count = 0
        self.last_log_time = 0

        # Status history for tray menu (letzte 5 Ereignisse)
        self.status_history = []

        # Icon status for color coding
        self.icon_status = "unknown"

        # Test available audio methods
        self.detect_audio_method()

    def load_settings(self):
        """Loads settings from file"""
        settings_file = "microphone_keeper_settings.json"

        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)

                # Merge with default settings
                settings = self.default_settings.copy()
                settings.update(loaded_settings)

                logging.info(f"Settings loaded: {settings}")
                return settings
        except Exception as e:
            logging.warning(f"Could not load settings: {e}")

        # Fallback to default settings
        return self.default_settings.copy()

    def save_settings(self):
        """Saves current settings to file"""
        settings_file = "microphone_keeper_settings.json"

        current_settings = {
            'device': self.selected_device,
            'target_volume': self.target_volume,
            'check_interval': self.check_interval
        }

        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(current_settings, f, indent=2, ensure_ascii=False)

            logging.info(f"Settings saved: {current_settings}")
            self.add_status_event("SETTINGS", "Settings saved")

        except Exception as e:
            logging.error(f"Could not save settings: {e}")

    def show_settings_dialog(self, icon=None, item=None):
        """Shows the settings dialog"""
        try:
            # Current status for dialog
            current_settings = {
                'device': self.selected_device,
                'target_volume': self.target_volume,
                'check_interval': self.check_interval
            }

            # Dialog anzeigen
            dialog = SettingsDialog(None, current_settings)
            result = dialog.show()

            if result:
                # Apply new settings
                old_settings = current_settings.copy()

                self.selected_device = result['device']
                self.target_volume = result['target_volume']
                self.check_interval = result['check_interval']

                # Einstellungen speichern
                self.save_settings()

                # Add status event
                changes = []
                if old_settings['target_volume'] != self.target_volume:
                    changes.append(f"Target: {self.target_volume}%")
                if old_settings['check_interval'] != self.check_interval:
                    changes.append(f"Rate: {self.check_interval}s")
                if old_settings['device'] != self.selected_device:
                    device_short = self.selected_device[:20] + "..." if len(self.selected_device) > 20 else self.selected_device
                    changes.append(f"Device: {device_short}")

                if changes:
                    self.add_status_event("CONFIG", ", ".join(changes))

                # Update menu
                self.update_menu()

                # Info dialog
                messagebox.showinfo(
                    "✅ Settings Saved",
                    f"New Settings:\n\n"
                    f"🎤 Device: {self.selected_device}\n"
                    f"🎯 Target Volume: {self.target_volume}%\n"
                    f"⏱️ Sampling Rate: {self.check_interval}s\n\n"
                    f"Changes are active immediately!"
                )

        except Exception as e:
            logging.error(f"Error in settings dialog: {e}")
            messagebox.showerror(
                "❌ Fehler",
                f"Could not open settings dialog:\n{e}"
            )

    def detect_audio_method(self):
        """Detects which audio method is available"""
        logging.info("Detecting available audio methods...")

        # Method 1: AudioDeviceCmdlets PowerShell module
        if self.test_audio_device_cmdlets():
            self.audio_method = "AudioDeviceCmdlets"
            self.icon_status = "active"  # Grün - Echte API
            logging.info("OK: AudioDeviceCmdlets PowerShell module available")
            return

        # Fallback: Simulation
        self.audio_method = "Simulation"
        self.icon_status = "simulation"  # Gelb - Simulation
        logging.warning("WARNING: No real audio API available - using simulation")

    def test_audio_device_cmdlets(self):
        """Tests if AudioDeviceCmdlets is available"""
        try:
            result = subprocess.run([
                'powershell', '-Command',
                'Get-Module -ListAvailable AudioDeviceCmdlets | Select-Object -First 1'
            ], capture_output=True, text=True, timeout=5, encoding='utf-8',
            creationflags=subprocess.CREATE_NO_WINDOW)

            return result.returncode == 0 and 'AudioDeviceCmdlets' in result.stdout
        except:
            return False

    def get_microphone_volume(self):
        """Gets the current microphone volume"""
        if self.audio_method == "AudioDeviceCmdlets":
            return self.get_volume_audio_device_cmdlets()
        else:
            return self.get_volume_simulation()

    def set_microphone_volume(self, volume):
        """Sets the microphone volume"""
        if self.audio_method == "AudioDeviceCmdlets":
            return self.set_volume_audio_device_cmdlets(volume)
        else:
            return self.set_volume_simulation(volume)

    def get_volume_audio_device_cmdlets(self):
        """AudioDeviceCmdlets method with device selection - SIMPLE FIX"""
        try:
            # Base command
            if self.selected_device == "Default (Automatic)":
                cmd = 'Import-Module AudioDeviceCmdlets -ErrorAction SilentlyContinue; Get-AudioDevice -RecordingVolume'
            else:
                # Select specific device - Verwende ID direkt
                cmd = f'''
                Import-Module AudioDeviceCmdlets -ErrorAction SilentlyContinue
                $device = Get-AudioDevice -List | Where-Object {{$_.Name -eq "{self.selected_device}" -and $_.Type -eq "Recording"}} | Select-Object -First 1
                if ($device) {{
                    Set-AudioDevice -ID $device.ID
                }}
                Get-AudioDevice -RecordingVolume
                '''

            result = subprocess.run([
                'powershell', '-Command', cmd
            ], capture_output=True, text=True, timeout=10, encoding='utf-8',
            creationflags=subprocess.CREATE_NO_WINDOW)

            if result.returncode == 0 and result.stdout.strip():
                output = result.stdout.strip()

                # Parse the output - search for the last line mit nur Zahlen und %
                lines = output.split('\n')
                for line in reversed(lines):
                    line = line.strip()
                    if line and line.replace('%', '').isdigit():
                        volume_str = line.replace('%', '')
                        return int(volume_str)

                # Fallback: Try to parse entire output
                logging.warning(f"Could not extract volume from output: '{output[:100]}...'")

        except Exception as e:
            logging.error(f"AudioDeviceCmdlets error: {e}")
        return None

    def set_volume_audio_device_cmdlets(self, volume):
        """AudioDeviceCmdlets method with device selection - CORRECTED"""
        try:
            if self.selected_device == "Default (Automatic)":
                cmd = f'Import-Module AudioDeviceCmdlets -ErrorAction SilentlyContinue; Set-AudioDevice -RecordingVolume {volume}'
            else:
                # Select specific device - Clean command
                cmd = f'''
                Import-Module AudioDeviceCmdlets -ErrorAction SilentlyContinue
                $device = Get-AudioDevice -List | Where-Object {{$_.Name -eq "{self.selected_device}" -and $_.Type -eq "Recording"}} | Select-Object -First 1
                if ($device) {{
                    Set-AudioDevice -ID $device.ID
                    Set-AudioDevice -RecordingVolume {volume}
                    Write-Output "OK"
                }} else {{
                    Set-AudioDevice -RecordingVolume {volume}
                    Write-Output "OK"
                }}
                '''

            result = subprocess.run([
                'powershell', '-Command', cmd
            ], capture_output=True, text=True, timeout=10, encoding='utf-8',
            creationflags=subprocess.CREATE_NO_WINDOW)

            return result.returncode == 0

        except Exception as e:
            logging.error(f"AudioDeviceCmdlets Set Fehler: {e}")
        return False

    def get_volume_simulation(self):
        """Simulation for demo purposes"""
        import random
        if not hasattr(self, '_sim_volume'):
            self._sim_volume = self.target_volume

        # Simulate occasional volume changes
        if random.random() < 0.1:  # 10% Chance
            possible_volumes = [int(self.target_volume * 0.8), int(self.target_volume * 0.75),
                               int(self.target_volume * 0.9), self.target_volume]
            self._sim_volume = random.choice(possible_volumes)

        return self._sim_volume

    def set_volume_simulation(self, volume):
        """Simulation for demo purposes"""
        self._sim_volume = volume
        return True

    def add_status_event(self, event_type, message):
        """Adds an event to status history"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        event = f"{timestamp} - {event_type}: {message}"

        # Add at the beginning
        self.status_history.insert(0, event)

        # Keep only the last 5 events
        if len(self.status_history) > 5:
            self.status_history = self.status_history[:5]

    def monitor_volume(self):
        """Continuously monitors microphone volume"""
        logging.info(f"Volume monitoring started (Methode: {self.audio_method}, Device: {self.selected_device})")

        while self.running:
            try:
                current_volume = self.get_microphone_volume()

                if current_volume is not None:
                    # Intelligent logging - only on changes
                    volume_changed = (self.last_volume is None or
                                    abs(current_volume - self.last_volume) > 1)

                    # Check if volume deviates from target
                    if abs(current_volume - self.target_volume) > 2:  # 2% Toleranz
                        # Correct volume
                        if self.set_microphone_volume(self.target_volume):
                            self.correction_count += 1

                            # Only log if important
                            current_time = time.time()
                            should_log = (
                                self.correction_count == 1 or  # Erste Correction
                                volume_changed or  # Volume changed
                                self.correction_count % 10 == 0 or  # Jede 10. Correction
                                (current_time - self.last_log_time) > 60  # Every 60 seconds
                            )

                            if should_log:
                                if self.correction_count == 1:
                                    msg = f"First correction: {current_volume}% -> {self.target_volume}%"
                                    logging.info(msg)
                                    self.add_status_event("CORRECTION", f"{current_volume}% -> {self.target_volume}%")
                                elif self.correction_count % 10 == 0:
                                    msg = f"Correction #{self.correction_count}: {current_volume}% -> {self.target_volume}% (running stable)"
                                    logging.info(msg)
                                    self.add_status_event("STABLE", f"#{self.correction_count} Correctionen")
                                else:
                                    msg = f"Volume corrected: {current_volume}% -> {self.target_volume}%"
                                    logging.info(msg)
                                    self.add_status_event("CORRECTION", f"{current_volume}% -> {self.target_volume}%")

                                self.last_log_time = current_time
                        else:
                            logging.warning(f"Could not correct volume: {current_volume}%")

                    elif volume_changed and current_volume == self.target_volume:
                        # Volume is correct and has changed
                        logging.info(f"Volume is correct: {current_volume}%")

                    # Save last volume
                    self.last_volume = current_volume

                time.sleep(self.check_interval)

            except Exception as e:
                logging.error(f"Error in monitoring loop: {e}")
                time.sleep(self.check_interval)

    def start_monitoring(self):
        """Starts volume monitoring"""
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self.monitor_volume, daemon=True)
            self.monitor_thread.start()
            logging.info("Monitoring started")
            self.add_status_event("START", f"Monitoring started ({self.target_volume}%, {self.check_interval}s)")
            self.update_icon()
            self.update_menu()

    def stop_monitoring(self):
        """Stops volume monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        logging.info("Monitoring stopped")
        self.add_status_event("STOP", "Monitoring stopped")
        self.update_icon()
        self.update_menu()

    def create_icon_image(self):
        """Creates a color-coded icon for the system tray"""
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)

        # Determine main color based on status
        if not self.running:
            main_color = 'red'  # Red - Off/Error
        elif self.icon_status == "active":
            main_color = 'green'  # Green - Active and productive
        elif self.icon_status == "simulation":
            main_color = 'orange'  # Yellow/Orange - Simulation/Mockup
        else:
            main_color = 'red'  # Red - Unknown/Error

        # Draw microphone in main color
        draw.ellipse([20, 15, 44, 35], fill=main_color)  # Microphone head
        draw.rectangle([30, 35, 34, 50], fill=main_color)  # Stem
        draw.arc([25, 45, 39, 55], start=0, end=180, fill=main_color, width=3)  # Base

        # Small black outline for better visibility
        draw.ellipse([20, 15, 44, 35], outline='black', width=1)
        draw.rectangle([30, 35, 34, 50], outline='black', width=1)

        # Status text as small dot
        if self.running and self.correction_count > 0:
            # Small white dot shows activity
            draw.ellipse([50, 50, 58, 58], fill='white', outline='black')

        return image

    def show_status(self, icon=None, item=None):
        """Shows the current status"""
        current_vol = self.get_microphone_volume()

        status = "🟢 Active" if self.running else "🔴 Stopped"
        method_info = {
            'AudioDeviceCmdlets': '🔵 AudioDeviceCmdlets (Best Quality)',
            'Simulation': '⚪ Simulation (Demo)'
        }

        device_display = self.selected_device if len(self.selected_device) <= 30 else self.selected_device[:27] + "..."

        if current_vol is not None:
            messagebox.showinfo(
                "🎤 Microphone Volume Keeper - Advanced",
                f"Status: {status}\n"
                f"Audio Method: {method_info.get(self.audio_method, self.audio_method)}\n"
                f"Selected Device: {device_display}\n"
                f"Current Volume: {current_vol}%\n"
                f"Target Volume: {self.target_volume}%\n"
                f"Sampling Rate: {self.check_interval}s\n"
                f"Correctionen: {self.correction_count}\n\n"
                f"💡 Linksklick: Status anzeigen\n"
                f"💡 Rechtsklick: Menü mit Einstellungen"
            )
        else:
            messagebox.showerror(
                "❌ Microphone Volume Keeper",
                f"Error: Cannot retrieve microphone volume!\n\n"
                f"Current Method: {self.audio_method}\n"
                f"Selected Device: {device_display}\n\n"
                f"Suggested Solutions:\n"
                f"• Install AudioDeviceCmdlets:\n"
                f"  Install-Module AudioDeviceCmdlets\n"
                f"• Choose different device in settings\n"
                f"• Run as administrator"
            )

    def toggle_monitoring(self, icon, item):
        """Starts/Stops monitoring"""
        if self.running:
            self.stop_monitoring()
        else:
            self.start_monitoring()

    def update_menu(self):
        """Updates the tray menu with status history and settings"""
        status_text = "Stop" if self.running else "Start"

        # Status icon based on icon status
        if not self.running:
            status_icon = "🔴"
        elif self.icon_status == "active":
            status_icon = "🟢"
        elif self.icon_status == "simulation":
            status_icon = "🟡"
        else:
            status_icon = "🔴"

        # Create menu items
        menu_items = [
            pystray.MenuItem(f"📊 Show Status", self.show_status),
            pystray.MenuItem("─" * 30, None, enabled=False),
            pystray.MenuItem(f"{status_icon} {status_text}", self.toggle_monitoring),
            pystray.MenuItem(f"⚙️ Settings...", self.show_settings_dialog),
            pystray.MenuItem("─" * 30, None, enabled=False),
            pystray.MenuItem(f"🔧 {self.audio_method}", None, enabled=False),
            pystray.MenuItem(f"🎤 {self.selected_device[:25]}{'...' if len(self.selected_device) > 25 else ''}", None, enabled=False),
            pystray.MenuItem(f"🎯 Target: {self.target_volume}% | ⏱️ Rate: {self.check_interval}s", None, enabled=False),
        ]

        # Add status history
        if self.status_history:
            menu_items.append(pystray.MenuItem("─" * 30, None, enabled=False))
            menu_items.append(pystray.MenuItem("📋 Recent Events:", None, enabled=False))

            for event in self.status_history:
                # Shorten long events
                display_event = event if len(event) <= 40 else event[:37] + "..."
                menu_items.append(pystray.MenuItem(f"  {display_event}", None, enabled=False))

        menu_items.extend([
            pystray.MenuItem("─" * 30, None, enabled=False),
            pystray.MenuItem("❌ Exit", self.quit_application)
        ])

        menu = pystray.Menu(*menu_items)

        if self.icon:
            self.icon.menu = menu

    def update_icon(self):
        """Updates the tray icon"""
        if self.icon:
            self.icon.icon = self.create_icon_image()

    def quit_application(self, icon, item):
        """Exits the application"""
        self.stop_monitoring()
        if self.icon:
            self.icon.stop()

    def run_tray(self):
        """Starts the system tray icon"""
        image = self.create_icon_image()

        self.icon = pystray.Icon(
            "microphone_keeper_advanced",
            image,
            f"Microphone Volume Keeper Advanced"
        )

        # Left click shows status
        self.icon.default_action = self.show_status

        self.update_menu()

        # Start monitoring automatically
        self.start_monitoring()

        # Show tray icon
        self.icon.run()


def main():
    """Main function - Silent Professional Mode"""
    try:
        # Completely silent - no terminal output
        keeper = MicrophoneVolumeKeeperAdvanced()

        # Start system tray directly
        keeper.run_tray()

    except KeyboardInterrupt:
        # Silent exit
        pass
    except Exception as e:
        # Only log critical errors
        logging.error(f"Critical Error: {e}")
        # Show errors only for critical problems
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Microphone Volume Keeper - Critical Error",
            f"The program could not be started:\n\n{e}\n\n"
            f"Check the log file: microphone_keeper.log"
        )

if __name__ == "__main__":
    main()

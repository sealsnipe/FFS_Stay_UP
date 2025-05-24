# 📥 Installation Instructions

## 🚀 Professional Installer (Recommended)

1. **Download** `MicrophoneVolumeKeeper_Professional_v2.0.zip`
2. **Extract** the ZIP file to a temporary folder
3. **Right-click** on `INSTALL.bat` → **"Run as administrator"**
4. **Follow** the installation wizard prompts
5. **Done!** Program will appear in system tray

**Features:**
- Automatic Windows integration
- Desktop and Start Menu shortcuts
- Optional autostart with Windows
- Clean uninstallation available

## 📱 Portable Executable

1. **Download** `MicrophoneVolumeKeeper.exe`
2. **Save** to any folder (Desktop, Documents, etc.)
3. **Double-click** to run
4. **Done!** Program appears in system tray

**Features:**
- No installation required
- Run from USB drive or any location
- Single file solution

## 📦 Portable Package (For Python Users)

1. **Download** `MicrophoneVolumeKeeper_Portable.zip`
2. **Extract** to desired folder
3. **Double-click** `START.bat`
4. **Follow** automatic setup prompts
5. **Done!** Program appears in system tray

**Features:**
- Automatic Python dependency installation
- Source code included
- Customizable and extensible

## 💻 Source Code (For Developers)

1. **Download** `MicrophoneVolumeKeeper_Source_v2.0.0.zip`
2. **Extract** to development folder
3. **Install** dependencies: `pip install -r requirements.txt`
4. **Run** with: `python src/microphone_volume_keeper.py`

**Features:**
- Complete source code
- Build scripts included
- Customization and development

## 🔧 Troubleshooting

### Program doesn't start
- Ensure Windows Defender isn't blocking the file
- Try running as Administrator
- Check that PowerShell is available

### No volume control
- Install AudioDeviceCmdlets: `Install-Module AudioDeviceCmdlets -Force`
- Run PowerShell as Administrator for installation
- Restart the program after installation

### Tray icon not visible
- Check Windows system tray settings
- Look in the "hidden icons" area
- Try restarting the program

### Device not detected
- Verify microphone is working in Windows Sound settings
- Use "Default (Automatic)" in settings as fallback
- Check Windows microphone permissions

## 📞 Support

- **Issues:** Report on GitHub Issues
- **Logs:** Check `microphone_keeper.log` for details
- **Documentation:** See README.md for complete guide

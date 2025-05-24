#!/usr/bin/env python3
"""
Creates final release packages for Microphone Volume Keeper
Uses the current, corrected EXE and creates all deployment packages
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_final_release():
    """Creates the final release packages"""
    
    print("🚀 Creating Final Release Packages for Microphone Volume Keeper v2.0.0")
    print("=" * 80)
    
    # Create releases directory
    releases_dir = "releases"
    if os.path.exists(releases_dir):
        shutil.rmtree(releases_dir)
    os.makedirs(releases_dir)
    
    # Check if current EXE exists
    if not os.path.exists("dist/MicrophoneVolumeKeeper.exe"):
        print("❌ Current EXE not found! Please build first.")
        return
    
    print("✅ Found current EXE: dist/MicrophoneVolumeKeeper.exe")
    
    # 1. Copy standalone EXE
    shutil.copy("dist/MicrophoneVolumeKeeper.exe", f"{releases_dir}/MicrophoneVolumeKeeper.exe")
    print("✅ Standalone EXE copied to releases/")
    
    # 2. Copy Professional Package (if exists)
    if os.path.exists("MicrophoneVolumeKeeper_Professional_v2.0.zip"):
        shutil.copy("MicrophoneVolumeKeeper_Professional_v2.0.zip", 
                   f"{releases_dir}/MicrophoneVolumeKeeper_Professional_v2.0.zip")
        print("✅ Professional Package copied to releases/")
    
    # 3. Copy Portable Package (if exists)
    if os.path.exists("MicrophoneVolumeKeeper_Portable.zip"):
        shutil.copy("MicrophoneVolumeKeeper_Portable.zip", 
                   f"{releases_dir}/MicrophoneVolumeKeeper_Portable.zip")
        print("✅ Portable Package copied to releases/")
    
    # 4. Create Source Code ZIP
    print("📦 Creating source code package...")
    source_files = [
        "src/microphone_volume_keeper.py",
        "build/",
        "docs/",
        "README.md",
        "requirements.txt",
        ".gitignore",
        "start_silent.pyw"
    ]
    
    with zipfile.ZipFile(f"{releases_dir}/MicrophoneVolumeKeeper_Source_v2.0.0.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in source_files:
            if os.path.exists(item):
                if os.path.isfile(item):
                    zipf.write(item, item)
                else:
                    for root, dirs, files in os.walk(item):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arc_name = os.path.relpath(file_path, ".")
                            zipf.write(file_path, arc_name)
    
    print("✅ Source code package created")
    
    # 5. Create Release Notes
    release_notes = f"""# 🎤 Microphone Volume Keeper v2.0.0 - Professional Edition

**Release Date:** {datetime.now().strftime("%Y-%m-%d")}

## 📦 Download Options

### 🚀 Professional Installer (Recommended)
**File:** `MicrophoneVolumeKeeper_Professional_v2.0.zip`
- Full Windows integration with installer
- Desktop shortcuts and autostart options
- Complete documentation included
- **Size:** ~15 MB

### 📱 Portable Executable
**File:** `MicrophoneVolumeKeeper.exe`
- Single executable file
- No installation required
- Run from any location
- **Size:** ~25 MB

### 📦 Portable Package
**File:** `MicrophoneVolumeKeeper_Portable.zip`
- Includes Python source and launcher
- Automatic dependency installation
- Detailed setup instructions
- **Size:** ~50 KB

### 💻 Source Code
**File:** `MicrophoneVolumeKeeper_Source_v2.0.0.zip`
- Complete source code
- Build scripts included
- For developers and customization
- **Size:** ~100 KB

## ✨ What's New in v2.0.0

### 🎛️ Advanced Configuration
- **Audio Device Selection** - Choose specific microphones (Elgato Wave:3, Blue Yeti, etc.)
- **Adjustable Target Volume** - Set any volume from 1% to 100%
- **Configurable Sampling Rate** - 0.1s to 5.0s response time
- **Persistent Settings** - Automatic save/load of all configurations

### 🎨 Professional Interface
- **Color-coded System Tray** - 🟢 Active | 🟡 Simulation | 🔴 Stopped
- **Status History** - Track last 5 volume corrections
- **Silent Operation** - No terminal windows or PowerShell popups
- **Professional Dialogs** - Clean, user-friendly interface

### 🔧 Technical Improvements
- **Silent PowerShell Execution** - No more blue command windows
- **Robust Error Handling** - Automatic fallbacks and recovery
- **Multi-Device Support** - Works with all Windows microphones
- **Performance Optimized** - Minimal system resource usage

## 🎯 Perfect For

- **Content Creators** - Consistent levels for streaming/recording
- **Business Professionals** - Reliable audio for video calls
- **Gamers** - Stable voice chat volume
- **Podcasters** - Professional audio control

## 📋 System Requirements

- Windows 10/11
- PowerShell (included with Windows)
- AudioDeviceCmdlets PowerShell module (recommended)

### Installing AudioDeviceCmdlets
```powershell
# Run PowerShell as Administrator
Install-Module AudioDeviceCmdlets -Force
```

## 🚀 Quick Start

1. **Download** your preferred package above
2. **Extract** (if ZIP file) and run
3. **Look** for microphone icon in system tray
4. **Right-click** icon → "⚙️ Settings..." to configure

---

**Built with ❤️ using [Augment Code](https://www.augmentcode.com)**

*If this tool helps you, please ⭐ star the repository!*
"""
    
    with open(f"{releases_dir}/RELEASE_NOTES.md", "w", encoding="utf-8") as f:
        f.write(release_notes)
    
    print("✅ Release notes created")
    
    # 6. Create installation instructions
    install_instructions = """# 📥 Installation Instructions

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
"""
    
    with open(f"{releases_dir}/INSTALLATION.md", "w", encoding="utf-8") as f:
        f.write(install_instructions)
    
    print("✅ Installation instructions created")
    
    # Summary
    print("\n" + "=" * 80)
    print("🎉 FINAL RELEASE PACKAGES CREATED!")
    print("=" * 80)
    print(f"📁 All files in: {releases_dir}/")
    print()
    
    # List all files
    for file in os.listdir(releases_dir):
        file_path = os.path.join(releases_dir, file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            size_mb = size / (1024 * 1024)
            print(f"📦 {file:<50} ({size_mb:.1f} MB)")
    
    print("\n🚀 Ready for GitHub Release!")
    print("📋 Upload all files from releases/ folder to GitHub")

if __name__ == "__main__":
    create_final_release()

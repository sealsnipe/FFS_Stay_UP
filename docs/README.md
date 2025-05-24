# 🎤 Microphone Volume Keeper - Advanced

Professional microphone volume control with advanced configuration options.

## ✨ Features

### 🎛️ **Fully Configurable**
- **Audio Device Selection** - Dropdown with all available microphones
- **Adjustable Target Volume** - 1% to 100% (not just 100%)
- **Adjustable Sampling Rate** - 0.1s to 5.0s for optimal performance
- **Persistent Settings** - Automatic loading on startup

### 🎨 **Professional User Interface**
- **Color-coded Tray Icon**: 🟢 Green (active), 🟡 Yellow (simulation), 🔴 Red (off/error)
- **Extended Status Display** with all configuration details
- **Settings Dialog** with user-friendly sliders
- **Status History** of the last 5 events in right-click menu

### 🔇 **Silent Professional Mode**
- **Completely Silent** - No terminal output
- **File Logging Only** for debugging
- **Professional Background Operation**

## 🚀 Quick Start

1. **Start**: Double-click `start_microphone_keeper_advanced.bat`
2. **Settings**: Right-click on tray icon → "⚙️ Settings..."
3. **Check Status**: Left-click on tray icon

## ⚙️ Settings Dialog

### 🎤 **Audio Device**
- **Default (Automatic)** - Uses Windows default microphone
- **Specific Devices** - Choose from all available recording devices
- **Automatic Detection** - Loads all available microphones

### 🎯 **Target Volume**
- **Range**: 1% - 100%
- **Default**: 100%
- **Real-time Display** during adjustment
- **Immediate Application** after saving

### ⏱️ **Sampling Rate**
- **Range**: 0.1s - 5.0s
- **Default**: 0.5s
- **Recommendation**: 
  - 0.1s - 0.5s for maximum response speed
  - 1.0s - 2.0s for normal usage
  - 3.0s - 5.0s for minimal system load

## 🎮 Usage

### 📱 **Tray Icon**
- **Color shows status**:
  - 🟢 **Green** = Active with real audio API
  - 🟡 **Yellow** = Simulation/Demo mode
  - 🔴 **Red** = Stopped or error

### 🖱️ **Mouse Interaction**
- **Left Click** → Detailed status dialog
- **Right Click** → Complete menu with:
  - Show status
  - Start/Stop
  - ⚙️ **Settings...**
  - Current configuration
  - Last 5 events
  - Exit

### 📋 **Status History**
The right-click menu shows the last 5 events:
- `22:30:15 - CORRECTION: 80% -> 95%`
- `22:30:10 - START: Monitoring started (95%, 0.5s)`
- `22:29:45 - CONFIG: Target: 95%, Rate: 0.5s`

## 💾 **Settings File**

All settings are automatically saved in `microphone_keeper_settings.json`:

```json
{
  "device": "Elgato Wave:3",
  "target_volume": 95,
  "check_interval": 0.3
}
```

## 🔧 **Advanced Features**

### 🎤 **Multi-Device Support**
- Supports all Windows-compatible microphones
- USB microphones (Elgato Wave:3, Blue Yeti, etc.)
- Bluetooth headsets
- Built-in laptop microphones
- Audio interfaces

### ⚡ **Performance Optimization**
- **Intelligent Logging** - Only on changes
- **Adaptive Sampling Rate** - Configurable as needed
- **Minimal Resource Usage**
- **Efficient Audio API Usage**

### 🛡️ **Robust Error Handling**
- **Automatic Fallbacks** for API problems
- **Device Change Detection**
- **Connection Loss Recovery**
- **Detailed Error Logging**

## 📊 **Monitoring & Logging**

### 📝 **Log File**: `microphone_keeper.log`
```
2024-05-24 22:30:15 - INFO - Settings loaded: {'device': 'Elgato Wave:3', 'target_volume': 95, 'check_interval': 0.5}
2024-05-24 22:30:16 - INFO - Volume monitoring started (Method: AudioDeviceCmdlets, Device: Elgato Wave:3)
2024-05-24 22:30:20 - INFO - First correction: 80% -> 95%
```

## 🎯 **Use Cases**

### 🎙️ **Content Creator**
```
Device: Elgato Wave:3
Target Volume: 100%
Sampling Rate: 0.2s
→ Maximum quality, instant response
```

### 💼 **Business Calls**
```
Device: Bluetooth Headset
Target Volume: 85%
Sampling Rate: 1.0s
→ Stable volume, moderate system load
```

### 🎮 **Gaming**
```
Device: Gaming Headset
Target Volume: 90%
Sampling Rate: 0.5s
→ Consistent voice chat quality
```

## 🔄 **Migration from Standard Version**

The Advanced Version is fully compatible. Simply start and:

1. **First Run** → Uses default settings (100%, 0.5s)
2. **Adjust Settings** → Right-click → "⚙️ Settings..."
3. **Automatic Saving** → Settings persist

## 🏆 **Why Advanced Version?**

| Feature | Standard | **Advanced** |
|---------|----------|-------------|
| Target Volume | Only 100% | **1% - 100%** |
| Sampling Rate | Fixed 0.5s | **0.1s - 5.0s** |
| Audio Device | Automatic | **Selectable** |
| Settings | Hardcoded | **GUI + Persistent** |
| Status Info | Basic | **Extended** |
| User Experience | Good | **Excellent** |

**The Advanced Version is the ultimate solution for professional microphone control! 🎤✨**

## 📋 **Requirements**

- Windows 10/11
- PowerShell (included with Windows)
- AudioDeviceCmdlets PowerShell module (recommended)

### Installing AudioDeviceCmdlets
```powershell
# Run PowerShell as Administrator
Install-Module AudioDeviceCmdlets -Force
```

## 🛠️ **Installation**

### Option 1: Portable
1. Download the latest release
2. Extract the ZIP file
3. Run `start_microphone_keeper_advanced.bat`

### Option 2: Professional Installer
1. Download `MicrophoneVolumeKeeper_Professional_v2.0.zip`
2. Extract and run `INSTALL.bat` as Administrator
3. Follow the installation wizard

## 📞 **Support**

- **Log File**: Check `microphone_keeper.log` for detailed information
- **Issues**: Report bugs on GitHub Issues
- **Documentation**: See included README files

## 📄 **License**

MIT License - See LICENSE file for details.

---

**Developed with ❤️ using Augment Code**

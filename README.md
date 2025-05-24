# 🎤 Microphone Volume Keeper

Professional microphone volume control tool with advanced configuration options.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎛️ **Audio Device Selection** - Choose from all available microphones
- 🎯 **Adjustable Target Volume** - Set any volume from 1% to 100%
- ⏱️ **Configurable Sampling Rate** - 0.1s to 5.0s response time
- 🎨 **Color-coded System Tray** - Visual status indication
- 💾 **Persistent Settings** - Automatic configuration saving
- 🔇 **Silent Operation** - Professional background mode
- 📊 **Status History** - Track recent volume corrections

## 🚀 Quick Start

### Option 1: Download Release (Recommended)
1. **Download** the latest release from [Releases](../../releases)
2. **Extract** the ZIP file
3. **Run** `MicrophoneVolumeKeeper.exe` or use the installer

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/yourusername/microphone-volume-keeper.git
cd microphone-volume-keeper

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/microphone_volume_keeper.py
```

## 🎮 Usage

1. **System Tray Icon** - The application runs in the system tray
2. **Left Click** - Show detailed status
3. **Right Click** - Access settings and menu
4. **Color Coding**:
   - 🟢 **Green** - Active with real audio API
   - 🟡 **Yellow** - Simulation mode
   - 🔴 **Red** - Stopped or error

## ⚙️ Configuration

Right-click the tray icon and select "⚙️ Settings..." to configure:

- **Audio Device** - Select your microphone
- **Target Volume** - Set desired volume (1-100%)
- **Sampling Rate** - Adjust response time (0.1-5.0s)

Settings are automatically saved and restored on startup.

## 🎯 Use Cases

- **Content Creators** - Consistent microphone levels for streaming/recording
- **Business Professionals** - Reliable audio for video calls
- **Gamers** - Stable voice chat volume
- **Podcasters** - Professional audio quality

## 📋 Requirements

- Windows 10/11
- Python 3.8+ (if running from source)
- PowerShell (included with Windows)
- AudioDeviceCmdlets PowerShell module (recommended)

### Installing AudioDeviceCmdlets
```powershell
# Run PowerShell as Administrator
Install-Module AudioDeviceCmdlets -Force
```

## 🛠️ Development

### Building from Source
```bash
# Install build dependencies
pip install pyinstaller

# Build executable
python build/build_executable.py

# Create installer package
python build/create_installer.py

# Create portable package
python build/create_portable.py
```

### Project Structure
```
microphone-volume-keeper/
├── src/                    # Source code
│   └── microphone_volume_keeper.py
├── build/                  # Build scripts
├── docs/                   # Documentation
├── releases/               # Release packages
├── tests/                  # Unit tests
└── assets/                 # Icons and resources
```

## 📦 Releases

Download the latest version from the [Releases](../../releases) page:

- **🚀 Professional Installer** - Full Windows integration with autostart
- **📦 Portable Version** - No installation required, run anywhere
- **💻 Source Code** - For developers and customization

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🐛 Troubleshooting

### Common Issues

**Application doesn't start**
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`

**No volume control**
- Install AudioDeviceCmdlets: `Install-Module AudioDeviceCmdlets -Force`
- Run PowerShell as Administrator for installation
- Check Windows microphone permissions

**Tray icon not visible**
- Check Windows system tray settings
- Ensure the application isn't blocked by antivirus
- Try running as Administrator

**Device not detected**
- Verify the microphone is recognized by Windows
- Use "Default (Automatic)" in settings as fallback
- Check Windows Sound settings

For detailed logs, check `microphone_keeper.log` in the application directory.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](docs/LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Augment Code](https://www.augmentcode.com)
- Uses [AudioDeviceCmdlets](https://github.com/frgnca/AudioDeviceCmdlets) PowerShell module
- System tray functionality powered by [pystray](https://github.com/moses-palmer/pystray)
- GUI components built with tkinter

## 📞 Support

- **Issues**: Report bugs on [GitHub Issues](../../issues)
- **Documentation**: See [docs/README.md](docs/README.md) for detailed documentation
- **Logs**: Check `microphone_keeper.log` for troubleshooting

---

**⭐ If this project helps you, please give it a star!**

**Made with ❤️ for content creators, professionals, and anyone who needs reliable microphone control.**

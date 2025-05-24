#!/usr/bin/env python3
"""
Silent starter for Microphone Volume Keeper
.pyw extension prevents terminal window
"""

import subprocess
import sys
import os

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Start the main application without terminal
subprocess.Popen([sys.executable, "src/microphone_volume_keeper.py"], 
                 creationflags=subprocess.CREATE_NO_WINDOW)

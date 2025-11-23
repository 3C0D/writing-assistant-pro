"""
Test script to verify crash logging functionality
"""

import os
import subprocess
import sys
from pathlib import Path

from src.core import setup_exception_handler, setup_root_logger

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Fix for Windows console encoding (emojis)
os.environ["PYTHONIOENCODING"] = "utf-8"
if os.name == "nt":
    subprocess.run(["chcp", "65001"], shell=True, capture_output=True)
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except AttributeError:
    pass


# Setup logger and exception handler
setup_root_logger(debug=True, log_filename="logs/crash_test.log")
setup_exception_handler()

print("🧪 Testing crash logging functionality...")
print("📁 Crash log should be created at: logs/crash_run_dev.log")
print("\n💥 Triggering intentional crash...\n")

# Trigger an intentional crash
raise RuntimeError("This is an intentional crash for testing!")

import sys
from pathlib import Path

from src.core.autostart_manager import AutostartManager
from src.core.lifecycle_manager import LifecycleManager

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def verify_autostart():
    print("Verifying AutostartManager...")

    # Check initial state
    initial_state = AutostartManager.check_autostart()
    print(f"Initial autostart state: {initial_state}")

    # Enable
    print("Enabling autostart...")
    if AutostartManager.set_autostart(True):
        print("Successfully enabled autostart")
    else:
        print("Failed to enable autostart")

    # Check state
    new_state = AutostartManager.check_autostart()
    print(f"New autostart state: {new_state}")

    if not new_state:
        print("ERROR: Autostart should be enabled but check returned False")

    # Disable (restore)
    print("Disabling autostart...")
    if AutostartManager.set_autostart(False):
        print("Successfully disabled autostart")
    else:
        print("Failed to disable autostart")

    # Check state
    final_state = AutostartManager.check_autostart()
    print(f"Final autostart state: {final_state}")

    if final_state:
        print("ERROR: Autostart should be disabled but check returned True")


def verify_lifecycle():
    print("\nVerifying LifecycleManager...")
    if hasattr(LifecycleManager, "restart_app"):
        print("LifecycleManager.restart_app exists")
    else:
        print("ERROR: LifecycleManager.restart_app missing")


if __name__ == "__main__":
    verify_autostart()
    verify_lifecycle()

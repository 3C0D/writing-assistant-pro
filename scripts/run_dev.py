"""
Script de développement - Lance main.py avec l'argument --debug

Utilisation:
    uv run python scripts/run_dev.py
"""

import subprocess
from pathlib import Path

print("Starting in DEV mode...")
print("-" * 50)

# Lancer main.py avec l'argument --debug
main_path = Path(__file__).parent.parent / "main.py"
subprocess.run(["uv", "run", "python", str(main_path), "--debug"])

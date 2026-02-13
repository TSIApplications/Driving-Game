from __future__ import annotations

import subprocess
import sys


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    run([sys.executable, "scripts/generate_starter_maps.py"])
    run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--name",
            "WorldExplorer",
            "--onefile",
            "--windowed",
            "--add-data",
            "maps;maps",
            "--add-data",
            "data;data",
            "--paths",
            "src",
            "main.py",
        ]
    )
    print("Build complete. Find executable in dist/WorldExplorer.exe")

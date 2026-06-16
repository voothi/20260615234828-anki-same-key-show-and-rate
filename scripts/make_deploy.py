#!/usr/bin/env python3
"""Main developer entry point to deploy the Anki addon locally.

Delegates execution to scripts/packaging/deploy.py.
"""

import sys
import subprocess
from pathlib import Path


def main():
    script_dir = Path(__file__).resolve().parent
    deploy_script = script_dir / "packaging" / "deploy.py"
    
    if not deploy_script.exists():
        print(f"Error: Deploy script not found at {deploy_script}")
        sys.exit(1)

    import configparser
    config_path = script_dir / "packaging" / "packaging.ini"
    
    python_interpreter = sys.executable
    if config_path.exists():
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8")
        configured_interpreter = config.get("release", "python_interpreter", fallback="").strip()
        if configured_interpreter:
            python_interpreter = configured_interpreter

    cmd = [python_interpreter, str(deploy_script)] + sys.argv[1:]
    sys.exit(subprocess.call(cmd))


if __name__ == "__main__":
    main()

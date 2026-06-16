import os
import sys
import shutil
import platform
import argparse
import subprocess
import zipfile
import tempfile
import configparser
from pathlib import Path

# Import the package builder from create_addon_zip
from create_addon_zip import create_addon_package, load_config


def get_default_anki_addons_path(addon_name: str) -> Path:
    system = platform.system().lower()
    if system == "windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            base_dir = Path(appdata) / "Anki2" / "addons21"
        else:
            base_dir = Path.home() / "AppData" / "Roaming" / "Anki2" / "addons21"
    elif system == "darwin":  # macOS
        base_dir = Path.home() / "Library" / "Application Support" / "Anki2" / "addons21"
    else:  # Linux / FreeDesktop standard
        base_dir = Path.home() / ".local" / "share" / "Anki2" / "addons21"
        
    return base_dir / addon_name


def ensure_absent(path: Path, force: bool) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if not force:
        raise FileExistsError(f"Target path already exists at '{path}'. Re-run with --force to replace/overwrite it.")

    print(f"🗑️  Removing existing target at: {path}")
    try:
        if path.is_symlink():
            path.unlink()
        elif path.is_dir():
            try:
                os.rmdir(path)  # Safely deletes Windows junction/symlink directory without touching contents
            except OSError:
                shutil.rmtree(path)  # Recursively deletes actual directories
        else:
            path.unlink()
    except Exception as e:
        print(f"❌ Error removing target '{path}': {e}")
        sys.exit(1)


def create_junction(source: Path, target: Path) -> None:
    if platform.system().lower() != "windows":
        raise NotImplementedError("Junction mode is only supported on Windows.")
        
    print(f"🔗 Creating directory junction...")
    print(f"   Source: {source}")
    print(f"   Target: {target}")
    
    res = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(target), str(source)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if res.returncode != 0:
        print(f"❌ Failed to create junction: {res.stderr.strip()}")
        sys.exit(res.returncode)


def main():
    config = load_config()
    addon_name = config.get("release", "addon_name", fallback="anki-same-key-show-and-rate").strip()
    
    parser = argparse.ArgumentParser(description="Deploy Same-Key Show and Rate addon locally for development.")
    parser.add_argument(
        "--target",
        type=Path,
        default=get_default_anki_addons_path(addon_name),
        help="Target addon directory path.",
    )
    parser.add_argument(
        "--mode",
        choices=("copy", "junction"),
        default="copy",
        help="Deploy mode: 'copy' files or 'junction' directory link (Windows only).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing deployment folder.",
    )
    args = parser.parse_args()
    
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    target = args.target.resolve()
    
    if args.mode == "junction":
        if platform.system().lower() != "windows":
            print("❌ Error: Junction mode is Windows-only. Please use 'copy' mode on macOS/Linux.")
            sys.exit(1)
            
        ensure_absent(target, args.force)
        target.parent.mkdir(parents=True, exist_ok=True)
        create_junction(project_root, target)
        print("✅ Directory junction deployed successfully!")
        
    else:  # copy mode
        ensure_absent(target, args.force)
        target.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Deploying to target: {target}")
        with tempfile.TemporaryDirectory(prefix="anki-deploy-") as tmpdir:
            # Build addon package in the temp directory
            addon_zip_path = create_addon_package(output_dir=tmpdir)
            
            # Extract the package directly into the target directory
            with zipfile.ZipFile(addon_zip_path, 'r') as zf:
                zf.extractall(target)
                
        # Clean up sidecar checksum generated in temp directory (it's automatically deleted with the tempdir)
        print("✅ Files deployed successfully!")


if __name__ == "__main__":
    main()

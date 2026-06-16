import os
import sys
import shutil
import platform
import argparse
import subprocess
import configparser
from pathlib import Path


def load_config():
    config = configparser.ConfigParser()
    config_path = Path(__file__).resolve().parent / "packaging.ini"
    config.read(config_path, encoding="utf-8")
    return config


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


def copy_addon_files(source_dir: Path, target_dir: Path, excluded_dirs: set, excluded_files: set) -> None:
    print(f"📁 Copying addon files...")
    print(f"   Source: {source_dir}")
    print(f"   Target: {target_dir}")
    
    target_dir.mkdir(parents=True, exist_ok=True)
    
    for root, dirs, files in os.walk(source_dir):
        # Filter directories in-place (prevents traversing excluded folders)
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        for file in files:
            full_path = Path(root) / file
            relative_path = full_path.relative_to(source_dir)
            rel_path_str = relative_path.as_posix()
            
            # Skip excluded root files
            if rel_path_str in excluded_files:
                continue
                
            # Skip sensitive files safety net
            if len(relative_path.parts) == 1 and file in {"credentials.json", "settings.json"}:
                 continue

            # Skip compiler artifacts
            if file.endswith(".pyc") or file.endswith(".pyo"):
                continue
                
            dest_path = target_dir / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(full_path, dest_path)


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
    project_root = script_dir.parent.parent
    
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
        excluded_root_files_str = config.get("exclusions", "root_files", fallback="meta.json")
        excluded_root_files = set(p.strip() for p in excluded_root_files_str.split("\n") if p.strip())
        
        excluded_dir_names_str = config.get("exclusions", "dir_names", fallback="user_files\n__pycache__\n.git")
        excluded_dir_names = set(p.strip() for p in excluded_dir_names_str.split("\n") if p.strip())
        
        ensure_absent(target, args.force)
        copy_addon_files(project_root, target, excluded_dir_names, excluded_root_files)
        print("✅ Files copied successfully!")


if __name__ == "__main__":
    main()

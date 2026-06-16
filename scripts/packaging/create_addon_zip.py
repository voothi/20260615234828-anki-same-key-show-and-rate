import os
import sys
import zipfile
import argparse
import configparser
from datetime import datetime
from pathlib import Path


def load_config():
    config = configparser.ConfigParser()
    config_path = Path(__file__).resolve().parent / "packaging.ini"
    config.read(config_path, encoding="utf-8")
    return config


def create_addon_package(output_dir: str = None):
    config = load_config()
    
    addon_name = config.get("release", "addon_name", fallback="anki-same-key-show-and-rate").strip()
    
    excluded_root_files_str = config.get("exclusions", "root_files", fallback="meta.json")
    excluded_root_files = set(p.strip() for p in excluded_root_files_str.split("\n") if p.strip())
    
    excluded_dir_names_str = config.get("exclusions", "dir_names", fallback="user_files\n__pycache__\n.git")
    excluded_dir_names = set(p.strip() for p in excluded_dir_names_str.split("\n") if p.strip())

    # Determine paths
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    addon_source_dir = project_root
    
    if not addon_source_dir.exists():
        print(f"Error: Addon source directory not found at {addon_source_dir}")
        sys.exit(1)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}-{addon_name}.ankiaddon"
    
    if output_dir:
        output_path = Path(output_dir) / filename
    else:
        output_path = project_root / filename

    print(f"📦 Packaging addon...")
    print(f"   Source: {addon_source_dir}")
    print(f"   Dest:   {output_path}")

    # Create ZIP
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(addon_source_dir):
                # 1. Directory Exclusion (In-place modification)
                # This prevents descending into user_files, __pycache__, tests, scripts, etc.
                dirs[:] = [d for d in dirs if d not in excluded_dir_names]
                
                for file in files:
                    full_path = Path(root) / file
                    relative_path = full_path.relative_to(addon_source_dir)
                    rel_path_str = relative_path.as_posix()
                    
                    # 2. Specific Root File Exclusions
                    # e.g. meta.json, pytest.ini, README.md, etc.
                    if rel_path_str in excluded_root_files:
                        print(f"   Skipping root file: {rel_path_str}")
                        continue
                    
                    # 3. Block sensitive files if they somehow appear in root (safety net)
                    if len(relative_path.parts) == 1 and file in {"credentials.json", "settings.json"}:
                         print(f"   Skipping sensitive file at root: {rel_path_str}")
                         continue

                    # 4. General Safety: Skip .pyc files everywhere
                    if file.endswith(".pyc") or file.endswith(".pyo"):
                        continue

                    # 5. WARN about sensitive-looking files that are being INCLUDED (e.g. inside vendor)
                    if file in {"credentials.json", "settings.json", "meta.json"}:
                        print(f"⚠️  NOTICE: Including potentially sensitive file (found in subfolder): {rel_path_str}")

                    zf.write(full_path, arcname=rel_path_str)
                    
        print(f"✅ Package created successfully!")
        
        # Verify exclusions
        print("🔍 Verifying package content...")
        with zipfile.ZipFile(output_path, 'r') as zf:
            file_list = zf.namelist()
            issues_found = False
            for f in file_list:
                # Check strict forbidden dirs
                for forbidden_dir in excluded_dir_names:
                    if f.startswith(f"{forbidden_dir}/") or f == forbidden_dir:
                        print(f"❌ WARNING: Forbidden directory found in zip: {f}")
                        issues_found = True
                
                # Check root files
                if f in excluded_root_files:
                     print(f"❌ WARNING: Excluded root file found: {f}")
                     issues_found = True

            if not issues_found:
                print("✅ Verification passed: Sensitive paths excluded.")
                
                # Generate SHA256 sidecar checksum
                import hashlib
                checksum_path = output_path.with_name(f"{output_path.name}.sha256")
                digest = hashlib.sha256()
                with open(output_path, "rb") as f:
                    for chunk in iter(lambda: f.read(1024 * 1024), b""):
                        digest.update(chunk)
                checksum_path.write_text(f"{digest.hexdigest()} *{output_path.name}\n", encoding="utf-8")
                print(f"✅ Sidecar checksum created: {checksum_path.name}")
            else:
                print("⚠️  Verification failed! Check the output.")

    except Exception as e:
        print(f"❌ Error creating package: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package Same-Key Show and Rate addon for Anki.")
    parser.add_argument("--out", type=str, help="Optional output directory for the .ankiaddon file")
    
    args = parser.parse_args()
    create_addon_package(args.out)

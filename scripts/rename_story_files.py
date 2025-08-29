#!/usr/bin/env python3
"""
Script to rename existing story files to use branch_name-based naming convention.

This script:
1. Scans all story files in the backlog directory
2. Extracts the branch_name from YAML frontmatter
3. Renames files to match their branch_name (branch_name.md format)
4. Updates file_path references in PRIORITIZATION.json
"""

import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Tuple

def extract_frontmatter(content: str) -> Dict[str, Any]:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}

    # Find the end of frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}

    try:
        frontmatter = yaml.safe_load(parts[1])
        return frontmatter if isinstance(frontmatter, dict) else {}
    except yaml.YAMLError:
        return {}

def rename_story_file(file_path: Path, branch_name: str) -> Tuple[bool, str]:
    """Rename a story file to use branch_name.md format."""
    new_filename = f"{branch_name}.md"
    new_path = file_path.parent / new_filename

    if file_path == new_path:
        return True, f"Already correctly named: {file_path.name}"

    if new_path.exists():
        return False, f"Target file already exists: {new_path}"

    try:
        file_path.rename(new_path)
        return True, f"Renamed: {file_path.name} → {new_filename}"
    except Exception as e:
        return False, f"Error renaming {file_path.name}: {str(e)}"

def update_prioritization_json(old_path: str, new_path: str) -> None:
    """Update file_path references in PRIORITIZATION.json."""
    pri_file = Path("backlog/PRIORITIZATION.json")

    if not pri_file.exists():
        return

    try:
        with open(pri_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Update file_path in all stories
        updated = False
        for story in data.get("backlog", []):
            if story.get("file_path") == old_path:
                story["file_path"] = new_path
                updated = True

        if updated:
            with open(pri_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"Warning: Could not update PRIORITIZATION.json: {e}")

def main():
    """Main function to rename story files."""
    backlog_dir = Path("backlog")
    renamed_count = 0
    error_count = 0

    print("🔄 Scanning story files for renaming...")

    # Find all markdown files in backlog subdirectories
    for md_file in backlog_dir.rglob("*.md"):
        # Skip README files and other non-story files
        if md_file.name.lower() in ['readme.md', 'prioritization.md']:
            continue

        try:
            # Read file content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter
            frontmatter = extract_frontmatter(content)

            if not frontmatter or 'branch_name' not in frontmatter:
                print(f"⚠️  Skipping {md_file.name} - no branch_name found")
                continue

            branch_name = frontmatter['branch_name'].strip()
            if not branch_name:
                print(f"⚠️  Skipping {md_file.name} - empty branch_name")
                continue

            # Rename the file
            success, message = rename_story_file(md_file, branch_name)

            if success:
                print(f"✅ {message}")
                renamed_count += 1

                # Update PRIORITIZATION.json
                old_path = f"backlog/{md_file.relative_to(backlog_dir)}".replace("\\", "/")
                new_path = f"backlog/{md_file.parent.relative_to(backlog_dir)}/{branch_name}.md".replace("\\", "/")
                update_prioritization_json(old_path, new_path)
            else:
                print(f"❌ {message}")
                error_count += 1

        except Exception as e:
            print(f"❌ Error processing {md_file.name}: {e}")
            error_count += 1

    print("\n📊 Summary:")
    print(f"   ✅ Renamed: {renamed_count} files")
    print(f"   ❌ Errors: {error_count} files")

    if renamed_count > 0:
        print("\n🔄 Updating COMPLETE_BACKLOG.json...")
        os.system("python scripts/generate_complete_backlog.py")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Complete Backlog JSON Generator

Scans all backlog story files and generates a comprehensive JSON
with status tracking for all stories.
"""

import os
import re
import yaml
import json
from pathlib import Path
from datetime import datetime

def extract_story_from_file(file_path):
    """Extract story metadata from a markdown file."""
    
    if file_path.name.startswith("_") or file_path.name == "README.md" or file_path.name == "index.md":
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None
    
    # Extract YAML frontmatter if present
    frontmatter = {}
    if content.startswith("---\n"):
        try:
            yaml_end = content.find("\n---\n", 4)
            if yaml_end != -1:
                yaml_content = content[4:yaml_end]
                frontmatter = yaml.safe_load(yaml_content) or {}
        except:
            pass
    
    # Extract story ID from filename or content
    story_id = None
    if frontmatter.get("id"):
        story_id = frontmatter["id"]
    elif match := re.search(r'([A-Z]+-\d+)', file_path.name):
        story_id = match.group(1)
    elif match := re.search(r'([A-Z]\d+)', file_path.name):
        story_id = match.group(1)
    else:
        # Use filename as ID for legacy stories
        story_id = file_path.stem.upper()
    
    # Extract title
    title = frontmatter.get("title")
    if not title:
        if match := re.search(r'^#\s*(.+)$', content, re.MULTILINE):
            title = match.group(1).strip()
            # Clean up title if it includes story ID
            title = re.sub(r'^[A-Z]+-\d+:\s*', '', title)
        else:
            title = file_path.stem.replace('_', ' ').replace('-', ' ').title()
    
    # Generate branch name from title/filename
    branch_name = frontmatter.get("branch_name")
    if not branch_name:
        if story_id and title:
            # Create kebab-case branch name
            clean_title = re.sub(r'[^\w\s-]', '', title.lower())
            clean_title = re.sub(r'\s+', '-', clean_title)
            clean_title = clean_title[:50]  # Limit length
            branch_name = f"{story_id.lower()}-{clean_title}"
        else:
            branch_name = file_path.stem.lower()
    
    # Determine epic from path
    epic = frontmatter.get("epic", "unknown")
    if epic == "unknown":
        path_parts = file_path.parts
        if "infrastructure" in path_parts:
            epic = "infrastructure"
        elif "models" in path_parts:
            epic = "models" 
        elif "ui" in path_parts:
            epic = "ui"
        elif "llm" in path_parts:
            if "ingestion" in path_parts:
                epic = "llm_ingestion"
            elif "modeling" in path_parts:
                epic = "llm_modeling"
            elif "quality" in path_parts:
                epic = "llm_quality"
            elif "explain" in path_parts:
                epic = "llm_explain"
            elif "infra" in path_parts:
                epic = "llm_infra"
            else:
                epic = "llm_backlog"
        elif "social_media" in path_parts:
            epic = "social_media"
    
    # Extract estimate
    estimate = frontmatter.get("estimate", "TBD")
    if estimate == "TBD":
        if match := re.search(r'estimate[:\s]*(\d+\.?\d*\s*(?:sp|story points?|days?|weeks?))', content, re.IGNORECASE):
            estimate = match.group(1)
    
    # Extract dependencies
    dependencies = frontmatter.get("dependencies", [])
    if not dependencies and "dependencies" in content.lower():
        if match := re.search(r'dependencies[:\s]*\[([^\]]*)\]', content, re.IGNORECASE):
            deps_str = match.group(1)
            dependencies = [dep.strip().strip('"\'') for dep in deps_str.split(',') if dep.strip()]
    
    # Extract labels/tags
    labels = frontmatter.get("labels", frontmatter.get("tags", []))
    if not labels:
        # Auto-generate labels based on epic and content
        labels = [epic.replace("_", "-")]
        if "ui" in epic or "interface" in title.lower():
            labels.append("ui")
        if "data" in title.lower():
            labels.append("data")
        if "monitor" in title.lower():
            labels.append("monitoring")
    
    story = {
        "id": story_id,
        "title": title,
        "branch_name": branch_name,
        "file_path": str(file_path).replace("\\", "/"),
        "status": frontmatter.get("status", "backlog"),
        "priority": 99,  # Will be set later based on PRIORITIZATION.md
        "estimate": estimate,
        "epic": epic,
        "dependencies": dependencies,
        "labels": labels,
        "owner": frontmatter.get("owner", "Neo Starlord of Thunder"),
        "created": str(frontmatter.get("created", datetime.now().strftime('%Y-%m-%d'))),
        "last_updated": str(frontmatter.get("last_updated", datetime.now().strftime('%Y-%m-%d')))
    }
    
    return story

def generate_complete_backlog():
    """Generate complete backlog JSON from all story files."""
    
    backlog_dir = Path("backlog")
    stories = []
    
    # Scan all markdown files in backlog directory
    for md_file in backlog_dir.rglob("*.md"):
        story = extract_story_from_file(md_file)
        if story:
            stories.append(story)
    
    # Sort by epic and story ID
    stories.sort(key=lambda x: (x["epic"], x["id"]))
    
    # Create the JSON structure
    backlog_json = {
        "metadata": {
            "last_updated": datetime.now().strftime('%Y-%m-%d'),
            "total_backlog_stories": len(stories),
            "format_version": "2.0",
            "generated_by": "Strategic Nexus Prime"
        },
        "backlog": stories
    }
    
    return backlog_json

if __name__ == "__main__":
    print("🤖 Strategic Nexus Prime generating complete backlog JSON...")
    
    backlog_data = generate_complete_backlog()
    
    # Save to file
    output_file = Path("backlog/COMPLETE_BACKLOG.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(backlog_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated complete backlog with {backlog_data['metadata']['total_backlog_stories']} stories")
    print(f"📄 Saved to: {output_file}")
    
    # Show epic breakdown
    epics = {}
    for story in backlog_data["backlog"]:
        epic = story["epic"]
        epics[epic] = epics.get(epic, 0) + 1
    
    print("\n📊 Epic Breakdown:")
    for epic, count in sorted(epics.items()):
        print(f"  {epic}: {count} stories")

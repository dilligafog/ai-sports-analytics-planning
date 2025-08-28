#!/usr/bin/env python3
"""
Simple JSON Updater for Neo Starlord of Thunder

Updates story status and branch info in PRIORITIZATION.json
Usage examples:
  python update_story.py INF-009 --status active --branch inf-009-adhoc-story-file-storage
  python update_story.py LLM-005 --status completed
  python update_story.py INF-006 --status blocked
"""

import sys
import os
# Set UTF-8 encoding for Windows terminal compatibility
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer)

import json
import argparse
from datetime import datetime
from pathlib import Path

def load_backlog():
    """Load the backlog JSON file."""
    json_file = Path("backlog/PRIORITIZATION.json")
    if not json_file.exists():
        print(f"❌ JSON file not found: {json_file}")
        return None
        
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_backlog(data):
    """Save the backlog JSON file."""
    json_file = Path("backlog/PRIORITIZATION.json")
    
    # Update metadata
    data["metadata"]["last_updated"] = datetime.now().strftime('%Y-%m-%d')
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Updated: {json_file}")

def update_story(story_id, status=None, branch_name=None, owner=None):
    """Update a story's status, branch, or owner."""
    
    data = load_backlog()
    if not data:
        return False
    
    # Find the story
    story = None
    for item in data["backlog"]:
        if item["id"] == story_id:
            story = item
            break
    
    if not story:
        print(f"❌ Story not found: {story_id}")
        available_ids = [item["id"] for item in data["backlog"]]
        print(f"Available stories: {', '.join(available_ids)}")
        return False
    
    # Update fields
    updated_fields = []
    if status:
        story["status"] = status
        updated_fields.append(f"status → {status}")
    
    if branch_name:
        story["branch_name"] = branch_name
        updated_fields.append(f"branch_name → {branch_name}")
    
    if owner:
        story["owner"] = owner
        updated_fields.append(f"owner → {owner}")
    
    if not updated_fields:
        print(f"⚠️  No updates specified for {story_id}")
        return False
    
    # Save changes
    save_backlog(data)
    print(f"✅ Updated {story_id}: {', '.join(updated_fields)}")
    return True

def list_stories(show_all=False):
    """List stories in the backlog."""
    data = load_backlog()
    if not data:
        return
    
    if show_all:
        print(f"\n📋 All Backlog Stories ({data['metadata']['total_backlog_stories']}):")
        print("=" * 80)
        
        stories = data["backlog"]
    else:
        # Show only ready-to-start stories (no dependencies or dependencies completed)
        ready_stories = []
        for story in data["backlog"]:
            if story["status"] == "backlog" and (not story["dependencies"] or all(dep in ["COMPLETED", "ACCEPTED"] for dep in story["dependencies"])):
                ready_stories.append(story)
        
        print(f"\n🚀 Ready to Start Stories ({len(ready_stories)}):")
        print("=" * 80)
        stories = ready_stories[:10]  # Show top 10
    
    for story in stories:
        status_emoji = {
            "backlog": "📝",
            "active": "🚀", 
            "completed": "✅",
            "blocked": "❌"
        }.get(story["status"], "❓")
        
        priority_display = story.get("priority", 99)
        if priority_display == 99:
            priority_display = "⚪"
        
        print(f"{status_emoji} {story['id']} | {story['status']} | P{priority_display} | {story['estimate']}")
        print(f"   {story['title']}")
        print(f"   Epic: {story['epic']} | Branch: {story['branch_name']}")
        if story["dependencies"]:
            print(f"   Dependencies: {', '.join(story['dependencies'])}")
        print()
    
    if not show_all and len(data["backlog"]) > 10:
        print(f"... and {len(data['backlog']) - 10} more stories. Use --all to see everything.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update story status and branch info for Neo Starlord of Thunder"
    )
    parser.add_argument("story_id", nargs="?", help="Story ID to update (e.g., INF-009)")
    parser.add_argument("--status", choices=["backlog", "active", "completed", "blocked"], 
                       help="New status for the story")
    parser.add_argument("--branch", help="Branch name for the story")
    parser.add_argument("--owner", help="Owner of the story")
    parser.add_argument("--list", action="store_true", help="List ready-to-start stories")
    parser.add_argument("--all", action="store_true", help="List all stories (use with --list)")
    
    args = parser.parse_args()
    
    if args.list or not args.story_id:
        list_stories(show_all=args.all)
    else:
        update_story(args.story_id, args.status, args.branch, args.owner)

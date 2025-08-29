#!/usr/bin/env python3
"""
Priority Management Script for AI Sports Analytics Planning

Automates priority reordering, new story ingestion, and backlog refinement.
Provides interactive tools for strategic backlog management.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class PriorityManager:
    def __init__(self, json_file: str = "backlog/PRIORITIZATION.json"):
        self.json_file = Path(json_file)
        self.data = self._load_json()
        
    def _load_json(self) -> Dict[str, Any]:
        """Load and parse the prioritization JSON file."""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.json_file} not found!")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {self.json_file}: {e}")
            sys.exit(1)
    
    def _save_json(self):
        """Save the updated data back to JSON file."""
        # Update metadata
        self.data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"✅ Updated {self.json_file}")
    
    def get_stories_by_priority(self) -> Dict[int, List[Dict[str, Any]]]:
        """Group stories by priority level."""
        priority_groups = {}
        for story in self.data["backlog"]:
            priority = story.get("priority", 99)
            if priority not in priority_groups:
                priority_groups[priority] = []
            priority_groups[priority].append(story)
        return priority_groups
    
    def list_priorities(self, show_all: bool = False):
        """Display current priority structure."""
        priority_groups = self.get_stories_by_priority()
        
        print("\n📋 Current Priority Structure")
        print("=" * 50)
        
        # Show strategic priorities (1-20) or top priorities based on flag
        max_priority = 99 if show_all else 20
        
        for priority in sorted(priority_groups.keys()):
            if priority > max_priority:
                if not show_all:
                    continue
            
            stories = priority_groups[priority]
            count = len(stories)
            
            if priority == 99:
                print(f"\n🔄 Unprocessed (Priority {priority}): {count} stories")
                if not show_all:
                    print("   Use --all to see these stories")
                    continue
            else:
                print(f"\n⭐ Priority {priority}: {count} stories")
            
            for story in stories:
                status_emoji = {
                    "ready": "🟢",
                    "active": "🔵", 
                    "completed": "✅",
                    "accepted": "✅",
                    "blocked": "🔴",
                    "draft": "⚪"
                }.get(story.get("status", "draft"), "⚪")
                
                epic_tag = f"[{story.get('epic', 'unknown')}]"
                print(f"   {status_emoji} {story['id']}: {story['title']} {epic_tag}")
    
    def shift_priorities(self, from_priority: int, positions: int, dry_run: bool = False):
        """
        Shift stories at a priority level down by specified positions.
        
        Args:
            from_priority: Starting priority level to shift
            positions: Number of positions to shift down (positive = down, negative = up)
            dry_run: If True, just show what would change
        """
        affected_stories = []
        
        for story in self.data["backlog"]:
            current_priority = story.get("priority", 99)
            if current_priority >= from_priority and current_priority != 99:
                new_priority = current_priority + positions
                if new_priority < 1:
                    new_priority = 1
                
                affected_stories.append({
                    "story": story,
                    "old_priority": current_priority,
                    "new_priority": new_priority
                })
        
        if dry_run:
            print(f"\n🔍 Dry Run: Shifting priorities {from_priority}+ down by {positions}")
            print("=" * 60)
            for item in affected_stories:
                story = item["story"]
                print(f"   {story['id']}: {item['old_priority']} → {item['new_priority']}")
            print(f"\nTotal affected stories: {len(affected_stories)}")
            return
        
        # Apply changes
        for item in affected_stories:
            item["story"]["priority"] = item["new_priority"]
        
        self._save_json()
        print(f"✅ Shifted {len(affected_stories)} stories down by {positions} positions")
    
    def set_priority(self, story_id: str, new_priority: int):
        """Set specific priority for a story."""
        story = self._find_story(story_id)
        if not story:
            print(f"❌ Story {story_id} not found!")
            return False
        
        old_priority = story.get("priority", 99)
        story["priority"] = new_priority
        story["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        
        self._save_json()
        print(f"✅ {story_id}: Priority {old_priority} → {new_priority}")
        return True
    
    def insert_at_priority(self, story_ids: List[str], start_priority: int, shift_existing: bool = True):
        """
        Insert stories at specific priority levels, optionally shifting existing stories.
        
        Args:
            story_ids: List of story IDs to prioritize
            start_priority: Starting priority number
            shift_existing: Whether to shift existing stories down
        """
        if shift_existing:
            # Calculate how many positions to shift
            positions_needed = len(story_ids)
            self.shift_priorities(start_priority, positions_needed, dry_run=False)
        
        # Assign new priorities
        for i, story_id in enumerate(story_ids):
            new_priority = start_priority + i
            self.set_priority(story_id, new_priority)
    
    def auto_prioritize_ready_stories(self, max_priority: int = 10):
        """Automatically prioritize ready stories based on business value."""
        ready_stories = [
            story for story in self.data["backlog"]
            if story.get("status") == "ready" and story.get("priority", 99) == 99
        ]
        
        if not ready_stories:
            print("ℹ️  No ready stories found with priority 99")
            return
        
        print(f"\n🤖 Auto-prioritizing {len(ready_stories)} ready stories")
        print("=" * 50)
        
        # Simple scoring algorithm
        def calculate_score(story):
            score = 0
            epic = story.get("epic", "")
            
            # Epic-based scoring
            epic_scores = {
                "core": 10,      # Core LLM functionality
                "modeling": 8,   # ML models
                "ingestion": 7,  # Data ingestion
                "ui": 6,         # User interface
                "quality": 5,    # Quality assurance
                "infrastructure": 4,  # Infrastructure
                "adhoc": 1       # Ad-hoc tasks
            }
            score += epic_scores.get(epic, 3)
            
            # Dependency bonus (stories with no dependencies are easier)
            if not story.get("dependencies", []):
                score += 2
            
            # Owner bonus (assigned stories)
            if story.get("owner"):
                score += 1
            
            return score
        
        # Sort by score and assign priorities
        ready_stories.sort(key=calculate_score, reverse=True)
        
        # Find next available priority slot
        current_priorities = {story.get("priority") for story in self.data["backlog"]}
        next_priority = max_priority + 1
        while next_priority in current_priorities:
            next_priority += 1
        
        for i, story in enumerate(ready_stories[:10]):  # Top 10 ready stories
            priority = next_priority + i
            self.set_priority(story["id"], priority)
            print(f"   ⭐ {story['id']}: Priority {priority} (Score: {calculate_score(story)})")
    
    def _find_story(self, story_id: str) -> Optional[Dict[str, Any]]:
        """Find a story by ID."""
        for story in self.data["backlog"]:
            if story["id"] == story_id:
                return story
        return None
    
    def quick_reorder(self):
        """Interactive priority reordering interface."""
        print("\n🎯 Quick Priority Reorder")
        print("=" * 30)
        
        while True:
            print("\nOptions:")
            print("1. View current priorities")
            print("2. Move story to new priority")
            print("3. Insert stories at priority (shift others)")
            print("4. Shift priority range down")
            print("5. Auto-prioritize ready stories")
            print("6. Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                self.list_priorities()
            
            elif choice == "2":
                story_id = input("Story ID: ").strip().upper()
                try:
                    priority = int(input("New priority: "))
                    self.set_priority(story_id, priority)
                except ValueError:
                    print("❌ Invalid priority number")
            
            elif choice == "3":
                story_ids = input("Story IDs (comma-separated): ").strip().upper().split(",")
                story_ids = [sid.strip() for sid in story_ids if sid.strip()]
                try:
                    start_priority = int(input("Starting priority: "))
                    shift = input("Shift existing stories? (y/n): ").strip().lower() == "y"
                    self.insert_at_priority(story_ids, start_priority, shift)
                except ValueError:
                    print("❌ Invalid priority number")
            
            elif choice == "4":
                try:
                    from_priority = int(input("From priority: "))
                    positions = int(input("Shift down by positions: "))
                    dry_run = input("Dry run first? (y/n): ").strip().lower() == "y"
                    self.shift_priorities(from_priority, positions, dry_run)
                except ValueError:
                    print("❌ Invalid numbers")
            
            elif choice == "5":
                try:
                    max_priority = int(input("Max existing priority (default 10): ") or "10")
                    self.auto_prioritize_ready_stories(max_priority)
                except ValueError:
                    print("❌ Invalid priority number")
            
            elif choice == "6":
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid option")


def main():
    parser = argparse.ArgumentParser(
        description="AI Sports Analytics Priority Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View current priority structure
  python scripts/manage_priorities.py --list
  
  # View all stories including unprocessed
  python scripts/manage_priorities.py --list --all
  
  # Set specific story priority
  python scripts/manage_priorities.py --set LLM-001 --priority 5
  
  # Insert stories at priority 1, shift others down
  python scripts/manage_priorities.py --insert RSS-001,RSS-002 --at 1 --shift
  
  # Shift priorities 5+ down by 2 positions (dry run)
  python scripts/manage_priorities.py --shift-from 5 --positions 2 --dry-run
  
  # Auto-prioritize ready stories
  python scripts/manage_priorities.py --auto-prioritize
  
  # Interactive mode
  python scripts/manage_priorities.py --interactive
        """
    )
    
    # Display options
    parser.add_argument("--list", action="store_true", help="List current priorities")
    parser.add_argument("--all", action="store_true", help="Show all stories including unprocessed")
    
    # Single story operations
    parser.add_argument("--set", type=str, help="Story ID to set priority for")
    parser.add_argument("--priority", type=int, help="New priority value")
    
    # Batch operations
    parser.add_argument("--insert", type=str, help="Comma-separated story IDs to insert")
    parser.add_argument("--at", type=int, help="Priority position to insert at")
    parser.add_argument("--shift", action="store_true", help="Shift existing stories when inserting")
    
    # Range operations
    parser.add_argument("--shift-from", type=int, help="Starting priority to shift")
    parser.add_argument("--positions", type=int, help="Number of positions to shift")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    
    # Automation
    parser.add_argument("--auto-prioritize", action="store_true", help="Auto-prioritize ready stories")
    parser.add_argument("--max-priority", type=int, default=10, help="Max existing priority for auto-prioritize")
    
    # Interactive mode
    parser.add_argument("--interactive", action="store_true", help="Interactive priority management")
    
    # File path
    parser.add_argument("--file", type=str, default="backlog/PRIORITIZATION.json", 
                       help="Path to prioritization JSON file")
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = PriorityManager(args.file)
    
    # Execute commands
    if args.list:
        manager.list_priorities(show_all=args.all)
    
    elif args.set and args.priority is not None:
        manager.set_priority(args.set, args.priority)
    
    elif args.insert and args.at is not None:
        story_ids = [sid.strip().upper() for sid in args.insert.split(",")]
        manager.insert_at_priority(story_ids, args.at, args.shift)
    
    elif args.shift_from is not None and args.positions is not None:
        manager.shift_priorities(args.shift_from, args.positions, args.dry_run)
    
    elif args.auto_prioritize:
        manager.auto_prioritize_ready_stories(args.max_priority)
    
    elif args.interactive:
        manager.quick_reorder()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

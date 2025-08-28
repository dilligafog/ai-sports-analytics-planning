#!/usr/bin/env python3
"""
Priority Assignment Script

Assigns strategic priorities to all backlog stories based on:
- Epic importance
- Business value
- Dependencies
- Implementation readiness
"""

import json
import yaml
from pathlib import Path
from datetime import datetime

def get_epic_priority_weight(epic):
    """Return priority weight for epic (lower = higher priority)."""
    epic_priorities = {
        # Core business value - highest priority
        "core": 1,
        "modeling": 2,
        "data_sources": 3,
        
        # Infrastructure and foundation - medium-high priority
        "infrastructure": 4,
        "ingestion": 5,
        "infra": 6,
        
        # Feature expansion - medium priority
        "ui": 7,
        "training": 8,
        "social_media": 9,
        
        # AI/LLM capabilities - medium priority
        "llm_backlog": 10,
        
        # Maintenance and ad-hoc - lower priority
        "adhoc": 11,
        "unknown": 12,
    }
    return epic_priorities.get(epic, 10)

def get_status_priority_modifier(status):
    """Return priority modifier based on story status."""
    status_modifiers = {
        "ready": 0,      # Ready to implement - no delay
        "backlog": 1,    # In backlog - slight delay
        "blocked": 5,    # Blocked - significant delay
        "accepted": 10,  # Already done - lowest priority
    }
    return status_modifiers.get(status, 2)

def calculate_story_priority(story, story_index, total_stories):
    """Calculate priority for a story based on multiple factors."""
    
    # Base priority from epic
    epic_weight = get_epic_priority_weight(story["epic"])
    
    # Status modifier
    status_modifier = get_status_priority_modifier(story["status"])
    
    # Position within epic (stories later in file get slightly lower priority)
    position_factor = (story_index / total_stories) * 2
    
    # Special high-priority patterns in title
    title_lower = story["title"].lower()
    title_boost = 0
    if any(keyword in title_lower for keyword in ["critical", "urgent", "blocker", "foundation", "core"]):
        title_boost = -3
    elif any(keyword in title_lower for keyword in ["setup", "config", "install"]):
        title_boost = -1
    elif any(keyword in title_lower for keyword in ["nice-to-have", "future", "maybe"]):
        title_boost = 3
    
    # Calculate final priority (round to integer)
    final_priority = max(1, int(epic_weight + status_modifier + position_factor + title_boost))
    
    return final_priority

def assign_priorities():
    """Assign priorities to all stories in the backlog."""
    
    # Load the complete backlog
    backlog_file = Path("backlog/COMPLETE_BACKLOG.json")
    if not backlog_file.exists():
        print("❌ COMPLETE_BACKLOG.json not found. Run generate_complete_backlog.py first.")
        return
    
    with open(backlog_file, 'r', encoding='utf-8') as f:
        backlog_data = json.load(f)
    
    stories = backlog_data["backlog"]
    total_stories = len(stories)
    
    print(f"🎯 Assigning priorities to {total_stories} stories...")
    
    # Assign priorities
    for i, story in enumerate(stories):
        new_priority = calculate_story_priority(story, i, total_stories)
        story["priority"] = new_priority
        story["last_updated"] = datetime.now().strftime('%Y-%m-%d')
    
    # Sort by priority (ascending - lower numbers = higher priority)
    stories.sort(key=lambda x: (x["priority"], x["epic"], x["id"]))
    
    # Update metadata
    backlog_data["metadata"]["last_updated"] = datetime.now().strftime('%Y-%m-%d')
    backlog_data["metadata"]["priority_assigned"] = True
    backlog_data["metadata"]["priority_method"] = "strategic_business_value"
    
    # Save updated complete backlog
    with open(backlog_file, 'w', encoding='utf-8') as f:
        json.dump(backlog_data, f, indent=2, ensure_ascii=False)
    
    # Also save prioritization JSON
    prioritization_file = Path("backlog/PRIORITIZATION.json")
    with open(prioritization_file, 'w', encoding='utf-8') as f:
        json.dump(backlog_data, f, indent=2, ensure_ascii=False)
    
    # Generate prioritization markdown
    generate_prioritization_md(stories)
    
    # Show priority distribution
    show_priority_distribution(stories)
    
    print(f"✅ Priorities assigned and saved to {backlog_file}")
    print(f"✅ Prioritization list saved to {prioritization_file}")

def generate_prioritization_md(stories):
    """Generate human-readable prioritization markdown."""
    
    md_content = [
        "# Backlog Prioritization",
        "",
        f"*Last updated: {datetime.now().strftime('%Y-%m-%d')}*",
        "",
        "## Priority Rankings",
        "",
        "Stories ordered by strategic priority (1 = highest priority):",
        "",
        "| Priority | Story ID | Title | Epic | Status |",
        "|----------|----------|-------|------|--------|"
    ]
    
    for story in stories:
        status_emoji = {
            "ready": "🟢",
            "backlog": "🟡", 
            "blocked": "🔴",
            "accepted": "✅"
        }.get(story["status"], "⚪")
        
        md_content.append(
            f"| {story['priority']} | {story['id']} | {story['title']} | {story['epic']} | {status_emoji} {story['status']} |"
        )
    
    md_content.extend([
        "",
        "## Epic Priority Weights",
        "",
        "1. **Core** - Core business functionality",
        "2. **Modeling** - ML model development", 
        "3. **Data Sources** - Data integration",
        "4. **Infrastructure** - Platform foundation",
        "5. **Ingestion** - Data pipeline",
        "6. **Infra** - Infrastructure support",
        "7. **UI** - User interface",
        "8. **Training** - Model training",
        "9. **Social Media** - Social features",
        "10. **LLM Backlog** - AI capabilities",
        "11. **Adhoc** - Maintenance tasks",
        "12. **Unknown** - Uncategorized",
        "",
        "## Status Legend",
        "",
        "- 🟢 **Ready** - Ready for implementation",
        "- 🟡 **Backlog** - In backlog, needs refinement",
        "- 🔴 **Blocked** - Blocked by dependencies",
        "- ✅ **Accepted** - Completed and accepted",
    ])
    
    prioritization_md = Path("backlog/PRIORITIZATION.md")
    with open(prioritization_md, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_content))
    
    print(f"✅ Prioritization markdown saved to {prioritization_md}")

def show_priority_distribution(stories):
    """Show distribution of priorities by epic."""
    
    print("\n📊 Priority Distribution by Epic:")
    
    epic_priorities = {}
    for story in stories:
        epic = story["epic"]
        priority = story["priority"]
        if epic not in epic_priorities:
            epic_priorities[epic] = []
        epic_priorities[epic].append(priority)
    
    for epic in sorted(epic_priorities.keys()):
        priorities = epic_priorities[epic]
        avg_priority = sum(priorities) / len(priorities)
        min_priority = min(priorities)
        max_priority = max(priorities)
        count = len(priorities)
        
        print(f"  {epic:15s}: {count:2d} stories, avg priority {avg_priority:4.1f} (range {min_priority}-{max_priority})")

if __name__ == "__main__":
    print("🤖 Strategic Nexus Prime assigning story priorities...")
    assign_priorities()

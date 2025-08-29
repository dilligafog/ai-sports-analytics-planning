#!/usr/bin/env python3
"""
Story Ingestion System for AI Sports Analytics Planning

Processes new stories from staging area into the main backlog with proper
ID assignment, validation, and JSON updates.
"""

import json
import yaml
import csv
import re
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import shutil

class StoryIngestor:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.staging_path = self.base_path / "staging"
        self.backlog_path = self.base_path / "backlog"
        self.templates_path = self.base_path / "templates"
        
        # Epic directories mapping
        self.epic_dirs = {
            "core": "core",
            "modeling": "modeling", 
            "ingestion": "ingestion",
            "ui": "ui",
            "quality": "quality",
            "infra": "infrastructure",
            "infrastructure": "infrastructure",
            "adhoc": "adhoc",
            "social_media": "social_media",
            "explain": "explain",
            "models": "models"
        }
        
        # Load existing data
        self.prioritization_data = self._load_prioritization_json()
        
    def _load_prioritization_json(self) -> Dict[str, Any]:
        """Load the current prioritization JSON."""
        json_file = self.backlog_path / "PRIORITIZATION.json"
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {json_file} not found. Creating new structure.")
            return {"metadata": {}, "backlog": []}
    
    def _save_prioritization_json(self):
        """Save updated prioritization JSON."""
        json_file = self.backlog_path / "PRIORITIZATION.json"
        
        # Update metadata
        self.prioritization_data["metadata"].update({
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "total_backlog_stories": len(self.prioritization_data["backlog"])
        })
        
        # Ensure all dates are strings for JSON serialization
        for story in self.prioritization_data["backlog"]:
            if "created" in story and hasattr(story["created"], "strftime"):
                story["created"] = story["created"].strftime("%Y-%m-%d")
            if "last_updated" in story and hasattr(story["last_updated"], "strftime"):
                story["last_updated"] = story["last_updated"].strftime("%Y-%m-%d")
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.prioritization_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Updated {json_file}")
    
    def _get_next_story_id(self, epic: str) -> str:
        """Generate next available story ID for an epic."""
        # Epic prefix mapping
        epic_prefixes = {
            "core": "LLM",
            "modeling": "MOD", 
            "ingestion": "ING",
            "ui": "UI",
            "quality": "QA",
            "infra": "INF",
            "infrastructure": "INF",
            "adhoc": "ADH",
            "social_media": "SOC",
            "explain": "EXP",
            "models": "MOD"
        }
        
        prefix = epic_prefixes.get(epic, "GEN")
        
        # Find highest existing number for this prefix
        existing_numbers = []
        for story in self.prioritization_data["backlog"]:
            story_id = story.get("id", "")
            if story_id.startswith(prefix + "-"):
                try:
                    number = int(story_id.split("-")[1])
                    existing_numbers.append(number)
                except (IndexError, ValueError):
                    continue
        
        next_number = max(existing_numbers, default=0) + 1
        return f"{prefix}-{next_number:03d}"
    
    def _create_branch_name(self, story_id: str, title: str) -> str:
        """Create git branch name from story ID and title."""
        # Convert title to kebab-case
        clean_title = re.sub(r'[^\w\s-]', '', title.lower())
        clean_title = re.sub(r'[\s_]+', '-', clean_title)
        clean_title = clean_title.strip('-')
        
        # Combine with story ID
        branch_name = f"{story_id.lower()}-{clean_title}"
        
        # Limit length
        if len(branch_name) > 50:
            branch_name = branch_name[:47] + "..."
        
        return branch_name
    
    def _validate_story(self, story_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate a story has required fields and format."""
        errors = []
        
        # Required fields
        required_fields = ["title", "epic"]
        for field in required_fields:
            if not story_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Epic validation
        epic = story_data.get("epic", "")
        if epic and epic not in self.epic_dirs:
            errors.append(f"Invalid epic '{epic}'. Valid epics: {list(self.epic_dirs.keys())}")
        
        # Title validation
        title = story_data.get("title", "")
        if len(title) < 10:
            errors.append("Title too short (minimum 10 characters)")
        if len(title) > 100:
            errors.append("Title too long (maximum 100 characters)")
        
        return len(errors) == 0, errors
    
    def _parse_markdown_story(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse a markdown story file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split frontmatter and content
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    markdown_content = parts[2].strip()
                else:
                    print(f"Warning: Invalid frontmatter in {file_path}")
                    return None
            else:
                print(f"Warning: No frontmatter found in {file_path}")
                return None
            
            # Extract user story and acceptance criteria from content
            user_story_match = re.search(r'\*\*As a\*\*.*?\*\*So that\*\*[^#]*', markdown_content, re.DOTALL)
            if user_story_match:
                frontmatter['user_story'] = user_story_match.group(0).strip()
            
            # Extract acceptance criteria
            criteria_matches = re.findall(r'- \[ \] (.+)', markdown_content)
            if criteria_matches:
                frontmatter['acceptance_criteria'] = criteria_matches
            
            return frontmatter
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def _process_single_story(self, story_data: Dict[str, Any], source_file: Optional[Path] = None) -> bool:
        """Process a single story into the backlog."""
        # Validate story
        is_valid, errors = self._validate_story(story_data)
        if not is_valid:
            print(f"❌ Story validation failed:")
            for error in errors:
                print(f"   - {error}")
            return False
        
        # Generate story ID if not provided or temporary
        if not story_data.get("id") or story_data["id"].startswith("TEMP-"):
            story_data["id"] = self._get_next_story_id(story_data["epic"])
        
        # Generate branch name
        story_data["branch_name"] = self._create_branch_name(story_data["id"], story_data["title"])
        
        # Set defaults
        story_data.setdefault("status", "backlog")
        story_data.setdefault("priority", 99)
        story_data.setdefault("estimate", "TBD")
        story_data.setdefault("dependencies", [])
        story_data.setdefault("labels", [])
        story_data.setdefault("created", datetime.now().strftime("%Y-%m-%d"))
        story_data.setdefault("last_updated", datetime.now().strftime("%Y-%m-%d"))
        story_data.setdefault("author", "story-ingestor")
        story_data.setdefault("owner", "")
        
        # Determine target directory
        epic = story_data["epic"]
        target_dir = self.backlog_path / self.epic_dirs[epic]
        target_dir.mkdir(exist_ok=True)
        
        # Create target filename
        clean_title = re.sub(r'[^\w\s-]', '', story_data["title"])
        clean_title = re.sub(r'\s+', '_', clean_title.strip())
        target_filename = f"{story_data['id']}-{clean_title}.md"
        target_path = target_dir / target_filename
        
        # Update file path in story data
        story_data["file_path"] = f"backlog/{self.epic_dirs[epic]}/{target_filename}"
        
        # Create the markdown file content
        content = self._create_story_markdown(story_data)
        
        # Write the story file
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Add to prioritization JSON
        self.prioritization_data["backlog"].append(story_data)
        
        print(f"✅ Created story: {story_data['id']} - {story_data['title']}")
        print(f"   📁 Location: {target_path}")
        
        # Archive source file if it exists
        if source_file and source_file.exists():
            archive_dir = self.staging_path / "processed"
            archive_dir.mkdir(exist_ok=True)
            archive_path = archive_dir / source_file.name
            shutil.move(str(source_file), str(archive_path))
            print(f"   📦 Archived: {archive_path}")
        
        return True
    
    def _create_story_markdown(self, story_data: Dict[str, Any]) -> str:
        """Create markdown content for a story."""
        # Prepare frontmatter
        frontmatter = {k: v for k, v in story_data.items() 
                      if k not in ['user_story', 'acceptance_criteria', 'description']}
        
        # Start with frontmatter
        content = "---\n"
        content += yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        content += "---\n\n"
        
        # Add title
        content += f"# {story_data['id']}: {story_data['title']}\n\n"
        
        # Add user story
        if story_data.get('user_story'):
            content += "## User Story\n"
            content += f"{story_data['user_story']}\n\n"
        else:
            content += "## User Story\n"
            content += "**As a** [user role]  \n"
            content += "**I want** [capability/feature]  \n"
            content += "**So that** [business value/outcome]\n\n"
        
        # Add acceptance criteria
        content += "## Acceptance Criteria\n"
        if story_data.get('acceptance_criteria'):
            for criterion in story_data['acceptance_criteria']:
                content += f"- [ ] {criterion}\n"
        else:
            content += "- [ ] [Add acceptance criteria]\n"
        content += "\n"
        
        # Add description if provided
        if story_data.get('description'):
            content += "## Description\n"
            content += f"{story_data['description']}\n\n"
        
        # Add standard sections
        content += "## Implementation Notes\n"
        content += "- [Technical considerations]\n"
        content += "- [Dependencies or prerequisites]\n\n"
        
        content += "## Definition of Done\n"
        content += "- [ ] Implementation complete\n"
        content += "- [ ] Tests written and passing\n"
        content += "- [ ] Documentation updated\n"
        content += "- [ ] Acceptance criteria verified\n"
        
        return content
    
    def process_markdown_files(self) -> int:
        """Process all markdown files in staging/new/."""
        new_dir = self.staging_path / "new"
        if not new_dir.exists():
            print(f"No staging directory found: {new_dir}")
            return 0
        
        processed_count = 0
        markdown_files = list(new_dir.glob("*.md"))
        
        if not markdown_files:
            print("No markdown files found in staging/new/")
            return 0
        
        print(f"\n📥 Processing {len(markdown_files)} markdown files...")
        
        for file_path in markdown_files:
            print(f"\n🔄 Processing: {file_path.name}")
            story_data = self._parse_markdown_story(file_path)
            
            if story_data:
                if self._process_single_story(story_data, file_path):
                    processed_count += 1
            else:
                print(f"❌ Failed to parse: {file_path.name}")
        
        return processed_count
    
    def process_json_files(self) -> int:
        """Process JSON bulk import files."""
        bulk_dir = self.staging_path / "bulk"
        if not bulk_dir.exists():
            return 0
        
        processed_count = 0
        json_files = list(bulk_dir.glob("*.json"))
        
        for file_path in json_files:
            print(f"\n🔄 Processing JSON: {file_path.name}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                stories = data.get("stories", [])
                for story_data in stories:
                    if self._process_single_story(story_data):
                        processed_count += 1
                
                # Archive the file
                archive_dir = self.staging_path / "processed"
                archive_dir.mkdir(exist_ok=True)
                shutil.move(str(file_path), str(archive_dir / file_path.name))
                
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
        
        return processed_count
    
    def interactive_story_creation(self):
        """Interactive CLI for creating a story."""
        print("\n🎯 Interactive Story Creation")
        print("=" * 40)
        
        story_data = {}
        
        # Basic info
        story_data["title"] = input("Story title: ").strip()
        if not story_data["title"]:
            print("❌ Title is required")
            return
        
        # Epic selection
        print(f"\nAvailable epics: {', '.join(self.epic_dirs.keys())}")
        story_data["epic"] = input("Epic: ").strip().lower()
        if story_data["epic"] not in self.epic_dirs:
            print(f"❌ Invalid epic. Choose from: {list(self.epic_dirs.keys())}")
            return
        
        # Priority
        priority_input = input("Priority (low/medium/high/critical) [medium]: ").strip().lower()
        priority_map = {"low": 20, "medium": 15, "high": 10, "critical": 5}
        story_data["priority"] = priority_map.get(priority_input, 99)
        
        # Estimate
        story_data["estimate"] = input("Estimate (e.g., '3sp', '2 days') [TBD]: ").strip() or "TBD"
        
        # User story
        print("\n📝 User Story (press Enter twice when done):")
        user_story_lines = []
        while True:
            line = input()
            if line == "" and user_story_lines and user_story_lines[-1] == "":
                break
            user_story_lines.append(line)
        
        if user_story_lines:
            story_data["user_story"] = "\n".join(user_story_lines[:-1])  # Remove last empty line
        
        # Acceptance criteria
        print("\n✅ Acceptance Criteria (one per line, empty line to finish):")
        criteria = []
        while True:
            criterion = input("- ").strip()
            if not criterion:
                break
            criteria.append(criterion)
        
        if criteria:
            story_data["acceptance_criteria"] = criteria
        
        # Labels
        labels_input = input("\nLabels (comma-separated): ").strip()
        if labels_input:
            story_data["labels"] = [label.strip() for label in labels_input.split(",")]
        
        # Process the story
        print(f"\n🔄 Creating story...")
        if self._process_single_story(story_data):
            print("✅ Story created successfully!")
        else:
            print("❌ Failed to create story")
    
    def create_quick_template(self, template_type: str, title: str, epic: str):
        """Create a quick story from template."""
        templates = {
            "basic": self.staging_path / "templates" / "basic_story.md",
            "technical": self.staging_path / "templates" / "technical_story.md", 
            "spike": self.staging_path / "templates" / "spike_story.md"
        }
        
        template_path = templates.get(template_type)
        if not template_path or not template_path.exists():
            print(f"❌ Template '{template_type}' not found")
            return
        
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace placeholders
        content = content.replace("[Quick Title Here]", title)
        content = content.replace("[Technical Implementation Title]", title)
        content = content.replace("[Research/Investigation Title]", title)
        content = re.sub(r'epic: \w+', f'epic: {epic}', content)
        
        # Create filename
        clean_title = re.sub(r'[^\w\s-]', '', title)
        clean_title = re.sub(r'\s+', '-', clean_title.strip())
        filename = f"TEMP-{datetime.now().strftime('%H%M%S')}-{clean_title}.md"
        
        # Write to staging
        staging_file = self.staging_path / "new" / filename
        staging_file.parent.mkdir(exist_ok=True)
        
        with open(staging_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created template story: {staging_file}")
        print(f"   Edit the file and run 'ingest_stories.py' to process it")


def main():
    parser = argparse.ArgumentParser(
        description="Story Ingestion System for AI Sports Analytics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all staged stories
  python scripts/ingest_stories.py
  
  # Interactive story creation
  python scripts/ingest_stories.py --interactive
  
  # Create story from template
  python scripts/ingest_stories.py --template basic --title "New Feature" --epic core
  
  # Process only markdown files
  python scripts/ingest_stories.py --markdown-only
        """
    )
    
    parser.add_argument("--interactive", action="store_true", 
                       help="Interactive story creation mode")
    
    parser.add_argument("--template", choices=["basic", "technical", "spike"],
                       help="Create story from template")
    parser.add_argument("--title", type=str, help="Story title for template")
    parser.add_argument("--epic", type=str, help="Epic for template story")
    
    parser.add_argument("--markdown-only", action="store_true",
                       help="Process only markdown files")
    parser.add_argument("--json-only", action="store_true", 
                       help="Process only JSON files")
    
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be processed without making changes")
    
    args = parser.parse_args()
    
    # Initialize ingestor
    ingestor = StoryIngestor()
    
    # Handle template creation
    if args.template:
        if not args.title or not args.epic:
            print("❌ --title and --epic are required with --template")
            sys.exit(1)
        ingestor.create_quick_template(args.template, args.title, args.epic)
        return
    
    # Handle interactive mode
    if args.interactive:
        ingestor.interactive_story_creation()
        return
    
    # Process staged stories
    total_processed = 0
    
    if not args.json_only:
        total_processed += ingestor.process_markdown_files()
    
    if not args.markdown_only:
        total_processed += ingestor.process_json_files()
    
    # Save updates if any stories were processed
    if total_processed > 0:
        ingestor._save_prioritization_json()
        print(f"\n🎉 Successfully processed {total_processed} stories!")
        print(f"   Run 'python scripts/generate_complete_backlog.py' to update COMPLETE_BACKLOG.json")
    else:
        print("\nℹ️  No stories found to process")


if __name__ == "__main__":
    main()

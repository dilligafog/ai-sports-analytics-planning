#!/usr/bin/env python3
"""
Migrate Accepted Stories to Standardized Backlog

This script migrates accepted stories to proper backlog structure with:
- Standardized filenames (EPIC-001-title-format.md)
- YAML frontmatter for stories that lack it
- Proper epic folder placement
- Updated JSON tracking

Usage: python scripts/migrate_accepted_stories.py [--dry-run]
"""

import sys
import os
# Set UTF-8 encoding for Windows terminal compatibility
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer)

import json
import re
import yaml
from pathlib import Path
from datetime import datetime
import argparse

def analyze_accepted_stories():
    """Analyze all accepted stories and categorize them"""
    accepted_dir = Path("accepted")
    stories = []
    
    # Track next available ID per epic to avoid collisions
    epic_counters = {}
    
    for file_path in accepted_dir.glob("*.md"):
        if file_path.name == "README.md":
            continue
            
        print(f"📄 Analyzing: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to extract YAML frontmatter
        frontmatter = None
        if content.startswith('---\n'):
            end_idx = content.find('\n---\n', 4)
            if end_idx != -1:
                try:
                    frontmatter = yaml.safe_load(content[4:end_idx])
                except yaml.YAMLError:
                    print(f"  ⚠️  Invalid YAML frontmatter")
        
        # Determine epic from filename/content
        epic = determine_epic(file_path.name, content, frontmatter)
        
        # Generate standardized ID and filename
        new_id, new_filename = generate_standard_naming(file_path.name, epic, frontmatter, epic_counters)
        
        stories.append({
            'original_path': file_path,
            'original_name': file_path.name,
            'has_frontmatter': frontmatter is not None,
            'frontmatter': frontmatter,
            'epic': epic,
            'new_id': new_id,
            'new_filename': new_filename,
            'new_path': f"backlog/{epic}/{new_filename}",
            'content': content
        })
        
        print(f"  📂 Epic: {epic}")
        print(f"  🆔 New ID: {new_id}")
        print(f"  📝 New filename: {new_filename}")
        print(f"  📍 Target: backlog/{epic}/{new_filename}")
    
    return stories

def determine_epic(filename, content, frontmatter):
    """Determine the epic category for a story"""
    
    # If frontmatter has epic, use it (with mapping)
    if frontmatter and 'epic' in frontmatter:
        epic_mapping = {
            'feature_store': 'infrastructure',
            'adhoc': 'adhoc',
            'infrastructure': 'infrastructure',
            'modeling': 'modeling',
            'ui': 'ui',
            'llm': 'core',
            'llm_backlog': 'core',  # Map old llm_backlog to core
            'evaluation': 'quality',
            'ingestion': 'ingestion'
        }
        return epic_mapping.get(frontmatter['epic'], 'adhoc')
    
    # Parse from existing ID format
    if filename.startswith(('ADH-', 'INF-', 'MOD-', 'UI-', 'LLM-', 'ING-', 'QLT-', 'EXP-', 'EVAL-')):
        prefix = filename.split('-')[0]
        prefix_mapping = {
            'ADH': 'adhoc',
            'INF': 'infrastructure', 
            'MOD': 'modeling',
            'UI': 'ui',
            'LLM': 'core',
            'ING': 'ingestion',
            'QLT': 'quality',
            'EXP': 'explain',
            'EVAL': 'quality'
        }
        return prefix_mapping.get(prefix, 'adhoc')
    
    # Heuristic based on filename/content
    filename_lower = filename.lower()
    content_lower = content.lower()
    
    if any(word in filename_lower for word in ['ui', 'web', 'interface', 'frontend']):
        return 'ui'
    elif any(word in filename_lower for word in ['model', 'prediction', 'training', 'backtesting']):
        return 'modeling'
    elif any(word in filename_lower for word in ['feature_store', 'gold', 'infrastructure', 'framework']):
        return 'infrastructure'
    elif any(word in filename_lower for word in ['llm', 'extraction', 'news']):
        return 'core'
    elif any(word in filename_lower for word in ['rss', 'ingestion', 'odds', 'data_source']):
        return 'ingestion'
    elif any(word in filename_lower for word in ['quality', 'eval', 'metrics']):
        return 'quality'
    elif any(word in filename_lower for word in ['social', 's01', 's02', 's07']):
        return 'social_media'
    else:
        return 'adhoc'

def generate_standard_naming(original_name, epic, frontmatter, epic_counters):
    """Generate standardized ID and filename"""
    
    # If already has proper ID, use it (but ensure no collision)
    if re.match(r'^[A-Z]{2,4}-\d{3}', original_name):
        parts = original_name.split('-', 2)
        if len(parts) >= 2:
            existing_id = f"{parts[0]}-{parts[1]}"
            # Verify the prefix matches the epic
            epic_prefixes = {
                'adhoc': 'ADH',
                'infrastructure': 'INF', 
                'modeling': 'MOD',
                'ui': 'UI',
                'core': 'LLM',
                'ingestion': 'ING',
                'quality': 'QLT',
                'explain': 'EXP',
                'social_media': 'SOC'
            }
            expected_prefix = epic_prefixes.get(epic, 'ADH')
            
            if parts[0] == expected_prefix:
                # Mark this ID as used
                num = int(parts[1])
                epic_counters.setdefault(epic, set()).add(num)
                return existing_id, original_name
    
    # Generate new ID based on epic
    epic_prefixes = {
        'adhoc': 'ADH',
        'infrastructure': 'INF', 
        'modeling': 'MOD',
        'ui': 'UI',
        'core': 'LLM',
        'ingestion': 'ING',
        'quality': 'QLT',
        'explain': 'EXP',
        'social_media': 'SOC'
    }
    
    prefix = epic_prefixes.get(epic, 'ADH')
    
    # Get next available number for this epic
    next_num = get_next_epic_number(epic, prefix, epic_counters)
    new_id = f"{prefix}-{next_num:03d}"
    
    # Generate filename from title
    if frontmatter and 'title' in frontmatter:
        title = frontmatter['title']
    else:
        # Extract title from filename or content
        title = extract_title_from_name(original_name)
    
    # Convert title to filename format
    filename_title = re.sub(r'[^\w\s-]', '', title).strip()
    filename_title = re.sub(r'[-\s]+', '-', filename_title).lower()
    
    new_filename = f"{new_id}-{filename_title}.md"
    
    return new_id, new_filename

def get_next_epic_number(epic, prefix, epic_counters):
    """Get next available number for an epic"""
    # Check existing backlog
    backlog_dir = Path("backlog")
    existing_numbers = epic_counters.setdefault(epic, set())
    
    # Check current backlog folder
    epic_dir = backlog_dir / epic
    if epic_dir.exists():
        for file_path in epic_dir.glob("*.md"):
            match = re.match(rf'^{prefix}-(\d+)', file_path.name)
            if match:
                existing_numbers.add(int(match.group(1)))
    
    # Check JSON tracking
    json_path = backlog_dir / "PRIORITIZATION.json"
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for story in data.get('stories', []):
                story_id = story.get('id', '')
                if story_id.startswith(f"{prefix}-"):
                    match = re.match(rf'^{prefix}-(\d+)', story_id)
                    if match:
                        existing_numbers.add(int(match.group(1)))
    
    # Return next available number
    if not existing_numbers:
        next_num = 1
    else:
        next_num = max(existing_numbers) + 1
    
    # Mark this number as used
    existing_numbers.add(next_num)
    return next_num

def extract_title_from_name(filename):
    """Extract a reasonable title from filename"""
    # Remove extension
    name = filename.replace('.md', '')
    
    # Handle existing format
    if '-' in name and not name.startswith(('ADH-', 'INF-', 'MOD-')):
        # Split on underscores and convert
        parts = name.replace('_', ' ').split()
        return ' '.join(word.capitalize() for word in parts)
    
    # Handle ID format
    if re.match(r'^[A-Z]{2,4}-\d{3}', name):
        parts = name.split('-', 2)
        if len(parts) >= 3:
            return parts[2].replace('_', ' ').replace('-', ' ').title()
    
    return name.replace('_', ' ').replace('-', ' ').title()

def add_yaml_frontmatter(story_info):
    """Add standardized YAML frontmatter to stories that lack it"""
    
    if story_info['has_frontmatter']:
        # Update existing frontmatter
        frontmatter = story_info['frontmatter'].copy()
        frontmatter.update({
            'id': story_info['new_id'],
            'status': 'accepted',
            'epic': story_info['epic'],
            'accepted_date': datetime.now().strftime('%Y-%m-%d')
        })
        
        # Find content after frontmatter
        content = story_info['content']
        end_idx = content.find('\n---\n', 4)
        if end_idx != -1:
            body_content = content[end_idx + 5:]
        else:
            body_content = content
    else:
        # Create new frontmatter
        title = extract_title_from_name(story_info['original_name'])
        
        frontmatter = {
            'id': story_info['new_id'],
            'title': title,
            'epic': story_info['epic'],
            'status': 'accepted',
            'priority': 'medium',
            'effort': 'TBD',
            'branch_name': generate_branch_name(story_info['new_id'], title),
            'labels': ['accepted'],
            'created': datetime.now().strftime('%Y-%m-%d'),
            'accepted_date': datetime.now().strftime('%Y-%m-%d'),
            'author': 'migration',
            'dependencies': []
        }
        body_content = story_info['content']
    
    # Generate new content
    yaml_content = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    new_content = f"---\n{yaml_content}---\n\n{body_content.strip()}\n"
    
    return new_content, frontmatter

def generate_branch_name(story_id, title):
    """Generate a git branch name from story ID and title"""
    clean_title = re.sub(r'[^\w\s-]', '', title).strip()
    clean_title = re.sub(r'[-\s]+', '-', clean_title).lower()
    return f"{story_id.lower()}-{clean_title}"

def migrate_stories(stories, dry_run=True):
    """Execute the migration"""
    
    if dry_run:
        print("\n🔍 DRY RUN - No files will be moved")
    else:
        print("\n🚀 EXECUTING MIGRATION")
    
    # Ensure target directories exist
    epic_dirs = set(story['epic'] for story in stories)
    for epic in epic_dirs:
        epic_path = Path(f"backlog/{epic}")
        if not dry_run:
            epic_path.mkdir(exist_ok=True)
        print(f"📁 {'Would create' if dry_run else 'Created'}: {epic_path}")
    
    # Process each story
    for story in stories:
        print(f"\n📄 Processing: {story['original_name']}")
        
        # Generate new content with frontmatter
        new_content, frontmatter = add_yaml_frontmatter(story)
        
        if dry_run:
            print(f"  📝 Would move: {story['original_path']} → {story['new_path']}")
            print(f"  🆔 Would assign ID: {story['new_id']}")
            print(f"  📋 {'Has' if story['has_frontmatter'] else 'Would add'} YAML frontmatter")
        else:
            # Write new file
            new_path = Path(story['new_path'])
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ Created: {new_path}")
            
            # Remove original
            story['original_path'].unlink()
            print(f"  🗑️  Removed: {story['original_path']}")
    
    print(f"\n📊 Migration Summary:")
    print(f"  📄 Total stories: {len(stories)}")
    print(f"  📁 Epic folders: {len(epic_dirs)}")
    print(f"  🆔 Stories needing frontmatter: {sum(1 for s in stories if not s['has_frontmatter'])}")

def main():
    parser = argparse.ArgumentParser(description='Migrate accepted stories to standardized backlog')
    parser.add_argument('--dry-run', action='store_true', default=True,
                        help='Show what would be done without making changes')
    parser.add_argument('--execute', action='store_true',
                        help='Actually execute the migration')
    args = parser.parse_args()
    
    # Override dry_run if execute is specified
    dry_run = not args.execute
    
    print("🤖 Strategic Nexus Prime - Accepted Stories Migration")
    print("=" * 60)
    
    if dry_run:
        print("🔍 Running in DRY RUN mode (use --execute to actually migrate)")
    
    # Analyze accepted stories
    print("\n📋 Analyzing accepted stories...")
    stories = analyze_accepted_stories()
    
    # Execute migration
    migrate_stories(stories, dry_run=dry_run)
    
    if not dry_run:
        print("\n✅ Migration complete!")
        print("📝 Run `python scripts/generate_complete_backlog.py` to update JSON tracking")

if __name__ == "__main__":
    main()

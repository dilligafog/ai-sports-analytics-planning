#!/usr/bin/env python3
"""
Script to update PRIORITIZATION.json file paths to match renamed files.
"""

import json

def main():
    # Load both JSON files
    with open('backlog/PRIORITIZATION.json', 'r') as f:
        pri_data = json.load(f)

    with open('backlog/COMPLETE_BACKLOG.json', 'r') as f:
        comp_data = json.load(f)

    # Create mapping from story ID to correct file path
    id_to_path = {story['id']: story['file_path'] for story in comp_data['backlog']}

    # Update PRIORITIZATION.json file paths
    updated = 0
    for story in pri_data['backlog']:
        story_id = story.get('id')
        if story_id in id_to_path:
            old_path = story.get('file_path', '')
            new_path = id_to_path[story_id]
            if old_path != new_path:
                story['file_path'] = new_path
                updated += 1

    # Save updated PRIORITIZATION.json
    with open('backlog/PRIORITIZATION.json', 'w') as f:
        json.dump(pri_data, f, indent=2, ensure_ascii=False)

    print(f'Updated {updated} file paths in PRIORITIZATION.json')

if __name__ == "__main__":
    main()

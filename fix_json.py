#!/usr/bin/env python3
"""Quick fix for corrupted PRIORITIZATION.json"""

import json
import re

# Read the backup and manually fix the JSON
with open('backlog/PRIORITIZATION.json.backup', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the last complete story entry
last_complete_match = re.search(r'(\{[^{}]*"file_path":[^{}]*\})\s*,?\s*\{\s*"id":\s*"LLM-019".*', content, re.DOTALL)

if last_complete_match:
    # Get everything up to the last complete entry
    prefix = content[:last_complete_match.start() + len(last_complete_match.group(1))]
    
    # Close the JSON properly
    fixed_content = prefix + '\n  ]\n}'
    
    with open('backlog/PRIORITIZATION.json', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("✅ Fixed PRIORITIZATION.json")
    
    # Verify it's valid JSON
    try:
        with open('backlog/PRIORITIZATION.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ JSON is valid with {len(data['backlog'])} stories")
    except Exception as e:
        print(f"❌ JSON still invalid: {e}")
else:
    print("❌ Could not find pattern to fix")

#!/usr/bin/env python3
"""
Backlog Structure Migration Script

Reorganizes the backlog folder structure to align with epic categories
and implements consistent naming conventions.
"""

import os
import json
import shutil
from pathlib import Path

def create_new_structure(dry_run=True):
    """Create the new folder structure."""
    
    base = Path("backlog")
    new_folders = [
        "infrastructure",
        "models", 
        "ui",
        "social_media",  # Already exists
        "ingestion",     # Clean - no llm_ prefix
        "modeling",      # Clean - no llm_ prefix
        "quality",       # Clean - no llm_ prefix
        "explain",       # Clean - no llm_ prefix
        "infra",         # Clean - no llm_ prefix  
        "core",          # Clean - no llm_ prefix
        "adhoc"
    ]
    
    for folder in new_folders:
        folder_path = base / folder
        if dry_run:
            if folder_path.exists():
                print(f"📁 Would use existing: {folder_path}")
            else:
                print(f"📁 Would create: {folder_path}")
        else:
            folder_path.mkdir(exist_ok=True)
            print(f"✅ Created: {folder_path}")

def get_migration_map():
    """Define the file migration mapping."""
    
    return {
        # Core stories (from backlog/llm/llm/ and root)
        "backlog/llm/05-injury-override-signal.md": "backlog/core/LLM-005-injury-override-signal.md",
        "backlog/llm/llm/01-feature-extraction-from-news.md": "backlog/core/LLM-001-feature-extraction-from-news.md",
        "backlog/llm/llm/02-evidence-citation-and-traceability.md": "backlog/core/LLM-002-evidence-citation-traceability.md", 
        "backlog/llm/llm/03-entity-resolution.md": "backlog/core/LLM-003-entity-resolution.md",
        "backlog/llm/llm/04-regime-change-detection.md": "backlog/core/LLM-004-regime-change-detection.md",
        "backlog/llm/llm/06-batch-processing-optimization.md": "backlog/core/LLM-006-batch-processing-optimization.md",
        "backlog/llm/llm/LLM-007-sales-pitch-personalization.md": "backlog/core/LLM-007-sales-pitch-personalization.md",
        
        # Ingestion (from backlog/llm/ingestion/)
        "backlog/llm/ingestion/02-article-dedup-enrich.md": "backlog/ingestion/ING-001-article-dedup-enrich.md",
        "backlog/llm/ingestion/04-pfr-scraper-week.md": "backlog/ingestion/ING-002-pfr-scraper-week.md",
        "backlog/llm/ingestion/05-content-quality-filtering.md": "backlog/ingestion/ING-003-content-quality-filtering.md",
        
        # Modeling (from backlog/llm/modeling/)
        "backlog/llm/modeling/01-base-ats-model.md": "backlog/modeling/MOD-001-base-ats-model.md",
        "backlog/llm/modeling/02-stacker-meta-model.md": "backlog/modeling/MOD-002-stacker-meta-model.md",
        "backlog/llm/modeling/03-probability-calibration.md": "backlog/modeling/MOD-003-probability-calibration.md",
        "backlog/llm/modeling/04-abstention-logic.md": "backlog/modeling/MOD-004-abstention-logic.md",
        "backlog/llm/modeling/06-calibration-monitoring.md": "backlog/modeling/MOD-005-calibration-monitoring.md",
        
        # Quality (from backlog/llm/quality/)
        "backlog/llm/quality/02-logging-and-monitoring.md": "backlog/quality/QLT-001-logging-monitoring.md",
        "backlog/llm/quality/03-feature-monitoring-drift.md": "backlog/quality/QLT-002-feature-monitoring-drift.md", 
        "backlog/llm/quality/04-production-data-quality-monitoring.md": "backlog/quality/QLT-003-production-data-quality-monitoring.md",
        
        # Explain (from backlog/llm/explain/)
        "backlog/llm/explain/01-llm-grounded-explanations.md": "backlog/explain/EXP-001-grounded-explanations.md",
        
        # Infra (from backlog/llm/infra/)
        "backlog/llm/infra/01-config-standards-yaml.md": "backlog/infra/INF-001-config-standards-yaml.md",
        "backlog/llm/infra/03-caching-ttl.md": "backlog/infra/INF-002-caching-ttl.md",
        "backlog/llm/infra/05-llm-provider-failover.md": "backlog/infra/INF-003-llm-provider-failover.md",
        
        # UI stories (from backlog/llm/ui/ to ui/)
        "backlog/llm/ui/01-landing-page-cards.md": "backlog/ui/UI-004-landing-page-cards.md",
        "backlog/llm/ui/02-game-detail-page.md": "backlog/ui/UI-005-game-detail-page.md",
    }

def migrate_files(dry_run=True):
    """Migrate files according to the migration map."""
    
    migration_map = get_migration_map()
    
    print(f"🤖 Strategic Nexus Prime migration analysis:")
    print(f"📁 Found {len(migration_map)} files to migrate")
    
    if dry_run:
        print("\n🔍 DRY RUN - Files that would be moved:")
        for old_path, new_path in migration_map.items():
            old_file = Path(old_path)
            if old_file.exists():
                print(f"  ✅ {old_path} → {new_path}")
            else:
                print(f"  ❌ {old_path} (not found)")
        return
    
    # Actual migration
    print("\n🚀 Executing migration:")
    for old_path, new_path in migration_map.items():
        old_file = Path(old_path)
        new_file = Path(new_path)
        
        if old_file.exists():
            # Create parent directory if needed
            new_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file
            shutil.move(str(old_file), str(new_file))
            print(f"  ✅ Moved: {old_path} → {new_path}")
        else:
            print(f"  ❌ Not found: {old_path}")

def update_json_file_paths():
    """Update file paths in PRIORITIZATION.json after migration."""
    
    json_file = Path("backlog/PRIORITIZATION.json")
    if not json_file.exists():
        print("❌ PRIORITIZATION.json not found")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    migration_map = get_migration_map()
    updates_made = 0
    
    for story in data["backlog"]:
        old_path = story["file_path"]
        if old_path in migration_map:
            new_path = migration_map[old_path]
            story["file_path"] = new_path
            updates_made += 1
            print(f"  📄 Updated JSON path: {old_path} → {new_path}")
    
    if updates_made > 0:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Updated {updates_made} file paths in PRIORITIZATION.json")
    else:
        print("ℹ️  No JSON path updates needed")

if __name__ == "__main__":
    import sys
    
    print("🤖 Strategic Nexus Prime - Backlog Structure Migration")
    print("=" * 60)
    
    if "--dry-run" in sys.argv or len(sys.argv) == 1:
        print("🔍 Running in DRY RUN mode (use --execute to actually migrate)")
        print("⚠️  Note: Some folders may have been created in previous 'dry' run! 😅")
        create_new_structure(dry_run=True)
        migrate_files(dry_run=True)
    elif "--execute" in sys.argv:
        print("🚀 EXECUTING MIGRATION")
        create_new_structure(dry_run=False)
        migrate_files(dry_run=False)
        update_json_file_paths()
        print("✅ Migration complete!")
    elif "--cleanup" in sys.argv:
        print("🧹 CLEANING UP empty folders from previous dry run...")
        # Add cleanup logic here if needed
    else:
        print("Usage: python migrate_backlog_structure.py [--dry-run|--execute|--cleanup]")

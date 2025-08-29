#!/usr/bin/env python3
"""
Data Cleanup Script for AI Sports Analytics Planning

Cleans up data quality issues, standardizes formats, and improves
the overall consistency of the story backlog data.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class DataCleaner:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.backlog_path = self.base_path / "backlog"
        
        # Standardized epic names mapping
        self.epic_standardization = {
            "adhoc": "adhoc",
            "core": "core", 
            "data_sources": "data-sources",
            "infra": "infrastructure",
            "infrastructure": "infrastructure",
            "ingestion": "ingestion",
            "llm_backlog": "llm",
            "modeling": "modeling",
            "social_media": "social",
            "training": "training",
            "ui": "ui",
            "unknown": "adhoc"  # Move unknown to adhoc
        }
        
        # Standard estimate values
        self.standard_estimates = {
            "1": "1sp", "2": "2sp", "3": "3sp", "5": "5sp", "8": "8sp", "13": "13sp",
            "1sp": "1sp", "2sp": "2sp", "3sp": "3sp", "5sp": "5sp", "8sp": "8sp", "13sp": "13sp",
            "small": "2sp", "medium": "5sp", "large": "8sp", "xl": "13sp",
            "s": "2sp", "m": "5sp", "l": "8sp"
        }
        
        # Default owners for epics
        self.epic_owners = {
            "adhoc": "Planning Team",
            "core": "AI Team",
            "data-sources": "Data Team", 
            "infrastructure": "DevOps Team",
            "ingestion": "Data Team",
            "llm": "AI Team",
            "modeling": "AI Team",
            "social": "Frontend Team",
            "training": "AI Team",
            "ui": "Frontend Team"
        }
    
    def load_prioritization_data(self) -> Dict[str, Any]:
        """Load current prioritization data."""
        json_file = self.backlog_path / "PRIORITIZATION.json"
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def clean_estimates(self, stories: List[Dict]) -> int:
        """Clean and standardize estimate values."""
        cleaned_count = 0
        
        for story in stories:
            estimate = story.get("estimate", "TBD")
            
            # Convert to string if it's a number
            if isinstance(estimate, (int, float)):
                estimate = str(estimate)
            
            if estimate == "TBD" or not estimate:
                # Auto-assign estimates based on epic and complexity indicators
                title = story.get("title", "").lower()
                epic = story.get("epic", "")
                
                if any(word in title for word in ["fix", "update", "cleanup", "refactor"]):
                    story["estimate"] = "2sp"  # Small maintenance tasks
                elif any(word in title for word in ["integration", "framework", "system"]):
                    story["estimate"] = "8sp"  # Large integration work
                elif any(word in title for word in ["api", "endpoint", "service"]):
                    story["estimate"] = "5sp"  # Medium API work
                elif epic in ["adhoc", "infra"]:
                    story["estimate"] = "3sp"  # Standard adhoc/infra work
                elif epic in ["core", "llm_backlog", "modeling"]:
                    story["estimate"] = "5sp"  # AI/ML work tends to be medium-large
                else:
                    story["estimate"] = "3sp"  # Default medium-small
                    
                cleaned_count += 1
            
            elif str(estimate).lower() in self.standard_estimates:
                story["estimate"] = self.standard_estimates[str(estimate).lower()]
                cleaned_count += 1
        
        return cleaned_count
    
    def clean_epics(self, stories: List[Dict]) -> int:
        """Standardize epic names."""
        cleaned_count = 0
        
        for story in stories:
            epic = story.get("epic", "unknown")
            if epic in self.epic_standardization:
                new_epic = self.epic_standardization[epic]
                if new_epic != epic:
                    story["epic"] = new_epic
                    cleaned_count += 1
        
        return cleaned_count
    
    def clean_owners(self, stories: List[Dict]) -> int:
        """Assign owners based on epic when missing."""
        cleaned_count = 0
        
        for story in stories:
            if not story.get("owner"):
                epic = story.get("epic", "adhoc")
                if epic in self.epic_owners:
                    story["owner"] = self.epic_owners[epic]
                    cleaned_count += 1
        
        return cleaned_count
    
    def clean_priorities(self, stories: List[Dict]) -> int:
        """Smart priority assignment for unprocessed stories."""
        cleaned_count = 0
        unprocessed = [s for s in stories if s.get("priority", 99) == 99]
        
        # Priority assignment logic
        for story in unprocessed:
            title = story.get("title", "").lower()
            epic = story.get("epic", "")
            status = story.get("status", "")
            
            # High priority indicators
            if any(word in title for word in ["critical", "urgent", "fix", "bug", "error"]):
                story["priority"] = 3
            elif any(word in title for word in ["integration", "core", "foundation"]):
                story["priority"] = 5
            elif epic in ["core", "infrastructure", "ingestion"]:
                story["priority"] = 7
            elif epic in ["llm", "modeling"]:
                story["priority"] = 10
            elif status in ["completed", "accepted"]:
                story["priority"] = 15  # Lower priority for completed work
            elif epic == "adhoc":
                story["priority"] = 20  # Adhoc work is typically lower priority
            else:
                story["priority"] = 12  # Default medium priority
            
            cleaned_count += 1
        
        return cleaned_count
    
    def clean_titles(self, stories: List[Dict]) -> int:
        """Clean up long titles and improve formatting."""
        cleaned_count = 0
        
        for story in stories:
            title = story.get("title", "")
            
            if len(title) > 60:
                # Shorten long titles
                words = title.split()
                if len(words) > 8:
                    # Keep first 8 words and add ellipsis if meaningful
                    short_title = " ".join(words[:8])
                    if len(short_title) < 50:
                        story["title"] = short_title
                        cleaned_count += 1
            
            # Remove redundant prefixes
            prefixes_to_remove = ["Story:", "Task:", "Feature:", "Epic:"]
            for prefix in prefixes_to_remove:
                if title.startswith(prefix):
                    story["title"] = title[len(prefix):].strip()
                    cleaned_count += 1
                    break
        
        return cleaned_count
    
    def clean_labels(self, stories: List[Dict]) -> int:
        """Add missing labels and standardize existing ones."""
        cleaned_count = 0
        
        for story in stories:
            labels = story.get("labels", [])
            
            if not labels:
                # Auto-generate labels based on epic and title
                epic = story.get("epic", "")
                title = story.get("title", "").lower()
                
                auto_labels = [epic]
                
                if any(word in title for word in ["api", "endpoint", "service"]):
                    auto_labels.append("api")
                if any(word in title for word in ["ui", "frontend", "interface"]):
                    auto_labels.append("frontend")
                if any(word in title for word in ["data", "dataset", "ingestion"]):
                    auto_labels.append("data")
                if any(word in title for word in ["ml", "ai", "model", "training"]):
                    auto_labels.append("ai-ml")
                if any(word in title for word in ["test", "testing", "validation"]):
                    auto_labels.append("testing")
                if any(word in title for word in ["doc", "documentation"]):
                    auto_labels.append("documentation")
                
                story["labels"] = auto_labels
                cleaned_count += 1
            
            # Standardize existing labels
            standardized_labels = []
            for label in labels:
                # Convert to lowercase and replace spaces/dashes
                clean_label = label.lower().replace(" ", "-").replace("_", "-")
                if clean_label not in standardized_labels:
                    standardized_labels.append(clean_label)
            
            if standardized_labels != labels:
                story["labels"] = standardized_labels
                cleaned_count += 1
        
        return cleaned_count
    
    def update_metadata(self, data: Dict[str, Any], changes: Dict[str, int]) -> None:
        """Update metadata with cleanup information."""
        data["metadata"].update({
            "last_cleaned": datetime.now().strftime("%Y-%m-%d"),
            "cleaned_by": "Strategic Nexus Prime - Data Cleanup",
            "cleanup_summary": {
                "estimates_cleaned": changes["estimates"],
                "epics_standardized": changes["epics"],
                "owners_assigned": changes["owners"],
                "priorities_assigned": changes["priorities"],
                "titles_cleaned": changes["titles"],
                "labels_added": changes["labels"],
                "total_improvements": sum(changes.values())
            }
        })
    
    def clean_all_data(self) -> Dict[str, Any]:
        """Perform comprehensive data cleanup."""
        print("🧹 Starting comprehensive data cleanup...")
        
        # Load data
        data = self.load_prioritization_data()
        stories = data["backlog"]
        
        print(f"📊 Processing {len(stories)} stories...")
        
        # Perform cleanup operations
        changes = {
            "estimates": self.clean_estimates(stories),
            "epics": self.clean_epics(stories),
            "owners": self.clean_owners(stories),
            "priorities": self.clean_priorities(stories),
            "titles": self.clean_titles(stories),
            "labels": self.clean_labels(stories)
        }
        
        # Update metadata
        self.update_metadata(data, changes)
        
        # Save cleaned data
        output_file = self.backlog_path / "PRIORITIZATION.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print("\n✅ Data cleanup completed!")
        print(f"📈 Improvements made:")
        for category, count in changes.items():
            if count > 0:
                print(f"   {category}: {count} items cleaned")
        
        print(f"\n🎯 Total improvements: {sum(changes.values())}")
        
        return data
    
    def generate_cleanup_report(self) -> str:
        """Generate a summary report of the cleanup."""
        data = self.load_prioritization_data()
        
        # Analyze cleaned data
        stories = data["backlog"]
        total_stories = len(stories)
        
        # Count quality metrics
        quality_metrics = {
            "with_estimates": len([s for s in stories if s.get("estimate") != "TBD"]),
            "with_owners": len([s for s in stories if s.get("owner")]),
            "prioritized": len([s for s in stories if s.get("priority", 99) != 99]),
            "with_labels": len([s for s in stories if s.get("labels")]),
            "proper_titles": len([s for s in stories if len(s.get("title", "")) <= 60])
        }
        
        # Epic distribution
        epic_dist = {}
        for story in stories:
            epic = story.get("epic", "unknown")
            epic_dist[epic] = epic_dist.get(epic, 0) + 1
        
        report = f"""
# 🧹 Data Cleanup Report

## 📊 Summary
- **Total Stories**: {total_stories}
- **Data Quality Score**: {round((sum(quality_metrics.values()) / (len(quality_metrics) * total_stories)) * 100, 1)}%

## 🎯 Quality Metrics
- **Stories with Estimates**: {quality_metrics['with_estimates']}/{total_stories} ({round((quality_metrics['with_estimates']/total_stories)*100, 1)}%)
- **Stories with Owners**: {quality_metrics['with_owners']}/{total_stories} ({round((quality_metrics['with_owners']/total_stories)*100, 1)}%)
- **Prioritized Stories**: {quality_metrics['prioritized']}/{total_stories} ({round((quality_metrics['prioritized']/total_stories)*100, 1)}%)
- **Stories with Labels**: {quality_metrics['with_labels']}/{total_stories} ({round((quality_metrics['with_labels']/total_stories)*100, 1)}%)
- **Proper Title Length**: {quality_metrics['proper_titles']}/{total_stories} ({round((quality_metrics['proper_titles']/total_stories)*100, 1)}%)

## 📈 Epic Distribution
"""
        
        for epic, count in sorted(epic_dist.items()):
            percentage = round((count/total_stories)*100, 1)
            report += f"- **{epic}**: {count} stories ({percentage}%)\n"
        
        cleanup_summary = data["metadata"].get("cleanup_summary", {})
        if cleanup_summary:
            report += f"""
## 🔧 Last Cleanup Results
- **Estimates Cleaned**: {cleanup_summary.get('estimates_cleaned', 0)}
- **Epics Standardized**: {cleanup_summary.get('epics_standardized', 0)}
- **Owners Assigned**: {cleanup_summary.get('owners_assigned', 0)}
- **Priorities Assigned**: {cleanup_summary.get('priorities_assigned', 0)}
- **Titles Cleaned**: {cleanup_summary.get('titles_cleaned', 0)}
- **Labels Added**: {cleanup_summary.get('labels_added', 0)}
- **Total Improvements**: {cleanup_summary.get('total_improvements', 0)}
"""
        
        return report


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean up AI Sports Analytics Planning data")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be cleaned without making changes")
    parser.add_argument("--report", action="store_true", help="Generate cleanup report")
    
    args = parser.parse_args()
    
    cleaner = DataCleaner()
    
    if args.report:
        report = cleaner.generate_cleanup_report()
        print(report)
        
        # Save report
        report_file = Path("reports") / f"data_cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n📄 Report saved to: {report_file}")
    
    elif args.dry_run:
        print("🔍 DRY RUN: Analyzing what would be cleaned...")
        # Load and analyze without saving
        data = cleaner.load_prioritization_data()
        stories = data["backlog"]
        
        print(f"📊 Found issues to clean:")
        print(f"   TBD estimates: {len([s for s in stories if s.get('estimate') == 'TBD'])}")
        print(f"   Missing owners: {len([s for s in stories if not s.get('owner')])}")
        print(f"   Unprocessed priorities: {len([s for s in stories if s.get('priority', 99) == 99])}")
        print(f"   Long titles: {len([s for s in stories if len(s.get('title', '')) > 60])}")
        print(f"   Missing labels: {len([s for s in stories if not s.get('labels')])}")
        
        print("\n💡 Run without --dry-run to perform cleanup")
    
    else:
        cleaned_data = cleaner.clean_all_data()
        print("\n🎉 Data cleanup completed successfully!")


if __name__ == "__main__":
    main()

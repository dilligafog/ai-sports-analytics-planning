#!/usr/bin/env python3
"""
Backlog Grooming Script
Systematically grooms the next 20 stories to ensure they are ready for implementation.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class BacklogGroomer:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.backlog_dir = self.repo_root / "backlog"
        self.prioritization_file = self.backlog_dir / "PRIORITIZATION.json"

        # Load current data
        with open(self.prioritization_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # ID format patterns
        self.id_patterns = {
            'adhoc': re.compile(r'^ADH-\d{3}$'),
            'core': re.compile(r'^LLM-\d{3}$'),
            'infra': re.compile(r'^INF-\d{3}$'),
            'ingestion': re.compile(r'^ING-\d{3}$'),
            'modeling': re.compile(r'^MOD-\d{3}$'),
            'ui': re.compile(r'^UI-\d{3}$'),
            'social': re.compile(r'^SOC-\d{3}$'),
            'quality': re.compile(r'^QLT-\d{3}$')
        }

        # Epic standardization mapping
        self.epic_mapping = {
            'data_sources': 'ingestion',
            'data_source_integration': 'ingestion',
            'llm_backlog': 'core',
            'infra': 'infrastructure',
            'training': 'modeling',
            'models': 'modeling'
        }

    def get_top_stories_to_groom(self, count: int = 20) -> List[Dict]:
        """Get the top N stories that need grooming, excluding completed ones."""
        stories = [
            s for s in self.data['backlog']
            if s['priority'] <= 20 and s['status'] in ['backlog', 'draft', 'ready', 'active', 'blocked']
        ]
        return sorted(stories, key=lambda x: x['priority'])[:count]

    def validate_story_id(self, story_id: str, epic: str) -> Tuple[bool, str]:
        """Validate and suggest corrected story ID format."""
        # Check if ID already follows proper format
        for epic_key, pattern in self.id_patterns.items():
            if pattern.match(story_id):
                return True, story_id

        # Generate proper ID based on epic
        if epic in ['core', 'llm_backlog']:
            # Find next available LLM ID
            existing_llm = [s['id'] for s in self.data['backlog'] if s['id'].startswith('LLM-')]
            next_num = max([int(s.split('-')[1]) for s in existing_llm] + [0]) + 1
            return False, f"LLM-{next_num:03d}"

        elif epic in ['infrastructure', 'infra']:
            existing_inf = [s['id'] for s in self.data['backlog'] if s['id'].startswith('INF-')]
            next_num = max([int(s.split('-')[1]) for s in existing_inf] + [0]) + 1
            return False, f"INF-{next_num:03d}"

        elif epic in ['ingestion', 'data_sources', 'data_source_integration']:
            existing_ing = [s['id'] for s in self.data['backlog'] if s['id'].startswith('ING-')]
            next_num = max([int(s.split('-')[1]) for s in existing_ing] + [0]) + 1
            return False, f"ING-{next_num:03d}"

        elif epic == 'ui':
            existing_ui = [s['id'] for s in self.data['backlog'] if s['id'].startswith('UI-')]
            next_num = max([int(s.split('-')[1]) for s in existing_ui] + [0]) + 1
            return False, f"UI-{next_num:03d}"

        elif epic == 'modeling':
            existing_mod = [s['id'] for s in self.data['backlog'] if s['id'].startswith('MOD-')]
            next_num = max([int(s.split('-')[1]) for s in existing_mod] + [0]) + 1
            return False, f"MOD-{next_num:03d}"

        elif epic == 'social_media':
            existing_soc = [s['id'] for s in self.data['backlog'] if s['id'].startswith('SOC-')]
            next_num = max([int(s.split('-')[1]) for s in existing_soc] + [0]) + 1
            return False, f"SOC-{next_num:03d}"

        else:  # Default to ADH for adhoc/unknown
            existing_adh = [s['id'] for s in self.data['backlog'] if s['id'].startswith('ADH-')]
            next_num = max([int(s.split('-')[1]) for s in existing_adh] + [0]) + 1
            return False, f"ADH-{next_num:03d}"

    def standardize_epic(self, epic: str) -> str:
        """Standardize epic names."""
        return self.epic_mapping.get(epic, epic)

    def find_duplicates(self) -> List[Tuple[str, List[Dict]]]:
        """Find stories with duplicate titles or similar content, excluding completed ones."""
        duplicates = []
        seen_titles = {}

        for story in self.data['backlog']:
            # Skip completed and accepted stories
            if story.get('status') in ['completed', 'accepted']:
                continue
                
            title = story['title'].lower().strip()
            if title in seen_titles:
                if seen_titles[title] not in duplicates:
                    duplicates.append((title, [seen_titles[title]]))
                duplicates[-1][1].append(story)
            else:
                seen_titles[title] = story

        return duplicates

    def groom_story_content(self, story: Dict) -> Dict:
        """Check and suggest improvements for story content."""
        issues = []

        # Check for placeholder text
        if any(placeholder in story['title'].lower() for placeholder in ['tbd', 'placeholder', 'template']):
            issues.append("Title contains placeholder text")

        # Check user story structure (if file exists)
        file_path = self.backlog_dir / story['file_path']
        if file_path.exists():
            with open(file_path, 'r') as f:
                content = f.read().lower()

            if 'as a' not in content or 'i want' not in content:
                issues.append("Missing proper user story format")

            if 'acceptance criteria' not in content:
                issues.append("Missing acceptance criteria")

            if len(content.split()) < 100:
                issues.append("Story content appears incomplete")

        return {
            'story': story,
            'issues': issues,
            'needs_grooming': len(issues) > 0
        }

    def generate_grooming_report(self) -> str:
        """Generate a comprehensive grooming report."""
        report = []
        report.append("# Backlog Grooming Report")
        report.append(f"**Generated:** {self.data['metadata']['last_updated']}")
        report.append("**Note:** Completed and accepted stories are excluded from grooming")
        report.append("")

        # Get top stories
        top_stories = self.get_top_stories_to_groom(20)

        report.append("## Top 20 Active Stories Ready for Grooming")
        report.append("")
        report.append("| # | Story ID | Epic | Status | Priority | Issues |")
        report.append("|---|----------|------|--------|----------|--------|")

        for i, story in enumerate(top_stories, 1):
            # Validate ID and epic
            id_valid, suggested_id = self.validate_story_id(story['id'], story['epic'])
            standardized_epic = self.standardize_epic(story['epic'])

            issues = []

            if not id_valid:
                issues.append(f"ID should be {suggested_id}")

            if standardized_epic != story['epic']:
                issues.append(f"Epic should be {standardized_epic}")

            # Check content
            content_check = self.groom_story_content(story)
            issues.extend(content_check['issues'])

            issues_str = "; ".join(issues) if issues else "Ready"

            report.append(f"| {i} | {story['id']} | {story['epic']} | {story['status']} | P{story['priority']} | {issues_str} |")

        # Check for duplicates
        duplicates = self.find_duplicates()
        if duplicates:
            report.append("")
            report.append("## Duplicate Stories Found")
            report.append("")
            for title, stories in duplicates:
                report.append(f"**{title.title()}:**")
                for story in stories:
                    report.append(f"  - {story['id']} ({story['epic']})")
                report.append("")

        # Summary
        total_stories = len([s for s in self.data['backlog'] if s['status'] in ['backlog', 'draft', 'ready', 'active', 'blocked']])
        ready_stories = len([s for s in self.data['backlog'] if s['status'] == 'ready'])
        completed_stories = len([s for s in self.data['backlog'] if s['status'] in ['completed', 'accepted']])

        report.append("## Summary")
        report.append(f"- **Total active stories needing grooming:** {total_stories}")
        report.append(f"- **Stories marked as ready:** {ready_stories}")
        if completed_stories > 0:
            report.append(f"- **Completed stories (excluded from grooming):** {completed_stories}")
        report.append(f"- **Top 20 priorities covered:** Yes")
        report.append(f"- **Duplicate stories found:** {len(duplicates)}")

        return "\n".join(report)

def main():
    groomer = BacklogGroomer(".")
    report = groomer.generate_grooming_report()

    # Save report
    with open("backlog_grooming_report.md", "w") as f:
        f.write(report)

    print("Grooming report generated: backlog_grooming_report.md")
    print("\n" + report)

if __name__ == "__main__":
    main()

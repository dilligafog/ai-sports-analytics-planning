#!/usr/bin/env python3
"""
Reporting Engine for AI Sports Analytics Planning

Generates comprehensive metrics, analytics, and dashboards for story
management, velocity tracking, and strategic planning insights.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re

class ReportGenerator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.backlog_path = self.base_path / "backlog"
        self.reports_path = self.base_path / "reports"
        self.reports_path.mkdir(exist_ok=True)
        
        # Load data
        self.prioritization_data = self._load_prioritization_json()
        self.complete_backlog = self._load_complete_backlog()
        
    def _load_prioritization_json(self) -> Dict[str, Any]:
        """Load prioritization data."""
        json_file = self.backlog_path / "PRIORITIZATION.json"
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"metadata": {}, "backlog": []}
    
    def _load_complete_backlog(self) -> Dict[str, Any]:
        """Load complete backlog data."""
        json_file = self.backlog_path / "COMPLETE_BACKLOG.json"
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"metadata": {}, "backlog": []}
    
    def generate_velocity_report(self) -> Dict[str, Any]:
        """Generate velocity and throughput metrics."""
        stories = self.prioritization_data.get("backlog", [])
        
        # Status breakdown
        status_counts = {}
        for story in stories:
            status = story.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Epic breakdown
        epic_counts = {}
        epic_completed = {}
        for story in stories:
            epic = story.get("epic", "unknown")
            status = story.get("status", "unknown")
            
            epic_counts[epic] = epic_counts.get(epic, 0) + 1
            if status in ["completed", "accepted"]:
                epic_completed[epic] = epic_completed.get(epic, 0) + 1
        
        # Calculate completion rates
        epic_completion_rates = {}
        for epic, total in epic_counts.items():
            completed = epic_completed.get(epic, 0)
            epic_completion_rates[epic] = round((completed / total) * 100, 1) if total > 0 else 0
        
        # Priority distribution
        priority_distribution = {}
        for story in stories:
            priority = story.get("priority", 99)
            if priority != 99:  # Exclude unprocessed
                priority_range = self._get_priority_range(priority)
                priority_distribution[priority_range] = priority_distribution.get(priority_range, 0) + 1
        
        return {
            "generated_at": datetime.now().isoformat(),
            "total_stories": len(stories),
            "status_breakdown": status_counts,
            "epic_breakdown": epic_counts,
            "epic_completion_rates": epic_completion_rates,
            "priority_distribution": priority_distribution,
            "top_priorities": self._get_top_priorities(stories, 10)
        }
    
    def generate_backlog_health_report(self) -> Dict[str, Any]:
        """Analyze backlog health and quality metrics."""
        stories = self.prioritization_data.get("backlog", [])
        
        # Quality metrics
        quality_issues = {
            "missing_estimates": 0,
            "missing_owners": 0,
            "missing_acceptance_criteria": 0,
            "long_titles": 0,
            "stale_stories": 0
        }
        
        # Story age analysis
        current_date = datetime.now()
        age_buckets = {"new": 0, "medium": 0, "old": 0, "stale": 0}
        
        for story in stories:
            # Check quality issues
            if not story.get("estimate") or story.get("estimate") == "TBD":
                quality_issues["missing_estimates"] += 1
            
            if not story.get("owner"):
                quality_issues["missing_owners"] += 1
            
            title = story.get("title", "")
            if len(title) > 80:
                quality_issues["long_titles"] += 1
            
            # Age analysis
            created_str = story.get("created", "")
            if created_str:
                try:
                    created_date = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                    age_days = (current_date - created_date).days
                    
                    if age_days <= 7:
                        age_buckets["new"] += 1
                    elif age_days <= 30:
                        age_buckets["medium"] += 1
                    elif age_days <= 90:
                        age_buckets["old"] += 1
                    else:
                        age_buckets["stale"] += 1
                        quality_issues["stale_stories"] += 1
                        
                except (ValueError, TypeError):
                    pass
        
        # Epic balance analysis
        epic_story_counts = {}
        for story in stories:
            epic = story.get("epic", "unknown")
            epic_story_counts[epic] = epic_story_counts.get(epic, 0) + 1
        
        # Calculate health score
        total_stories = len(stories)
        health_score = 100
        if total_stories > 0:
            health_score -= (quality_issues["missing_estimates"] / total_stories) * 20
            health_score -= (quality_issues["missing_owners"] / total_stories) * 15
            health_score -= (quality_issues["stale_stories"] / total_stories) * 25
            health_score = max(0, round(health_score, 1))
        
        return {
            "generated_at": datetime.now().isoformat(),
            "health_score": health_score,
            "quality_issues": quality_issues,
            "age_distribution": age_buckets,
            "epic_balance": epic_story_counts,
            "recommendations": self._generate_health_recommendations(quality_issues, age_buckets)
        }
    
    def generate_priority_analytics(self) -> Dict[str, Any]:
        """Analyze priority distribution and trends."""
        stories = self.prioritization_data.get("backlog", [])
        
        # Priority heat map
        priority_heatmap = {}
        for story in stories:
            priority = story.get("priority", 99)
            epic = story.get("epic", "unknown")
            
            if epic not in priority_heatmap:
                priority_heatmap[epic] = {}
            
            if priority != 99:
                priority_range = self._get_priority_range(priority)
                priority_heatmap[epic][priority_range] = priority_heatmap[epic].get(priority_range, 0) + 1
        
        # High priority analysis
        high_priority_stories = [s for s in stories if s.get("priority", 99) <= 10]
        high_priority_epics = {}
        for story in high_priority_stories:
            epic = story.get("epic", "unknown")
            high_priority_epics[epic] = high_priority_epics.get(epic, 0) + 1
        
        # Unprocessed stories
        unprocessed = [s for s in stories if s.get("priority", 99) == 99]
        unprocessed_by_epic = {}
        for story in unprocessed:
            epic = story.get("epic", "unknown")
            unprocessed_by_epic[epic] = unprocessed_by_epic.get(epic, 0) + 1
        
        return {
            "generated_at": datetime.now().isoformat(),
            "total_prioritized": len(stories) - len(unprocessed),
            "total_unprocessed": len(unprocessed),
            "priority_heatmap": priority_heatmap,
            "high_priority_distribution": high_priority_epics,
            "unprocessed_by_epic": unprocessed_by_epic,
            "priority_recommendations": self._generate_priority_recommendations(unprocessed_by_epic)
        }
    
    def generate_workflow_metrics(self) -> Dict[str, Any]:
        """Analyze workflow efficiency and automation performance."""
        stories = self.prioritization_data.get("backlog", [])
        
        # Automation metrics
        auto_created = len([s for s in stories if s.get("author") == "story-ingestor"])
        template_created = len([s for s in stories if "template" in s.get("labels", [])])
        
        # Status progression analysis
        status_progression = {
            "draft": len([s for s in stories if s.get("status") == "draft"]),
            "backlog": len([s for s in stories if s.get("status") == "backlog"]),
            "ready": len([s for s in stories if s.get("status") == "ready"]),
            "active": len([s for s in stories if s.get("status") == "active"]),
            "completed": len([s for s in stories if s.get("status") == "completed"]),
            "accepted": len([s for s in stories if s.get("status") == "accepted"])
        }
        
        # Story complexity analysis
        complexity_analysis = {
            "small": len([s for s in stories if self._get_story_size(s.get("estimate", "")) == "small"]),
            "medium": len([s for s in stories if self._get_story_size(s.get("estimate", "")) == "medium"]),
            "large": len([s for s in stories if self._get_story_size(s.get("estimate", "")) == "large"]),
            "unknown": len([s for s in stories if self._get_story_size(s.get("estimate", "")) == "unknown"])
        }
        
        return {
            "generated_at": datetime.now().isoformat(),
            "automation_adoption": {
                "auto_created_stories": auto_created,
                "template_usage": template_created,
                "automation_rate": round((auto_created / len(stories)) * 100, 1) if stories else 0
            },
            "status_progression": status_progression,
            "complexity_distribution": complexity_analysis,
            "workflow_efficiency": self._calculate_workflow_efficiency(status_progression)
        }
    
    def generate_dashboard_data(self) -> Dict[str, Any]:
        """Generate comprehensive dashboard data."""
        velocity = self.generate_velocity_report()
        health = self.generate_backlog_health_report()
        priority = self.generate_priority_analytics()
        workflow = self.generate_workflow_metrics()
        
        # Summary metrics for dashboard
        summary = {
            "total_stories": velocity["total_stories"],
            "health_score": health["health_score"],
            "prioritized_stories": priority["total_prioritized"],
            "automation_rate": workflow["automation_adoption"]["automation_rate"],
            "last_updated": datetime.now().isoformat()
        }
        
        return {
            "summary": summary,
            "velocity": velocity,
            "health": health,
            "priority": priority,
            "workflow": workflow
        }
    
    def _get_priority_range(self, priority: int) -> str:
        """Convert priority number to range label."""
        if priority <= 5:
            return "Critical (1-5)"
        elif priority <= 10:
            return "High (6-10)"
        elif priority <= 20:
            return "Medium (11-20)"
        else:
            return "Low (21+)"
    
    def _get_top_priorities(self, stories: List[Dict], count: int) -> List[Dict]:
        """Get top priority stories."""
        prioritized = [s for s in stories if s.get("priority", 99) != 99]
        prioritized.sort(key=lambda x: x.get("priority", 99))
        return prioritized[:count]
    
    def _get_story_size(self, estimate: str) -> str:
        """Categorize story size from estimate."""
        if not estimate or estimate == "TBD":
            return "unknown"
        
        # Extract numeric value
        numeric_match = re.search(r'(\d+)', str(estimate))
        if numeric_match:
            size = int(numeric_match.group(1))
            if size <= 2:
                return "small"
            elif size <= 5:
                return "medium"
            else:
                return "large"
        return "unknown"
    
    def _generate_health_recommendations(self, quality_issues: Dict, age_buckets: Dict) -> List[str]:
        """Generate actionable recommendations for backlog health."""
        recommendations = []
        
        if quality_issues["missing_estimates"] > 0:
            recommendations.append(f"Add estimates to {quality_issues['missing_estimates']} stories")
        
        if quality_issues["missing_owners"] > 5:
            recommendations.append("Assign owners to unowned stories for better accountability")
        
        if quality_issues["stale_stories"] > 0:
            recommendations.append(f"Review and update {quality_issues['stale_stories']} stale stories")
        
        if age_buckets["stale"] > age_buckets["new"]:
            recommendations.append("Focus on completing older stories to improve flow")
        
        return recommendations
    
    def _generate_priority_recommendations(self, unprocessed_by_epic: Dict) -> List[str]:
        """Generate priority management recommendations."""
        recommendations = []
        
        total_unprocessed = sum(unprocessed_by_epic.values())
        if total_unprocessed > 20:
            recommendations.append("Run auto-prioritization to process backlog efficiently")
        
        # Find epics with most unprocessed stories
        if unprocessed_by_epic:
            top_epic = max(unprocessed_by_epic.items(), key=lambda x: x[1])
            recommendations.append(f"Focus prioritization efforts on {top_epic[0]} epic ({top_epic[1]} stories)")
        
        return recommendations
    
    def _calculate_workflow_efficiency(self, status_progression: Dict) -> float:
        """Calculate workflow efficiency score."""
        total = sum(status_progression.values())
        if total == 0:
            return 0
        
        # Weight different statuses for efficiency
        efficiency = (
            status_progression.get("completed", 0) * 1.0 +
            status_progression.get("accepted", 0) * 1.0 +
            status_progression.get("active", 0) * 0.7 +
            status_progression.get("ready", 0) * 0.5 +
            status_progression.get("backlog", 0) * 0.3 +
            status_progression.get("draft", 0) * 0.1
        ) / total
        
        return round(efficiency * 100, 1)
    
    def save_report(self, report_data: Dict, report_type: str, output_format: str = "json"):
        """Save report to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = None
        
        if output_format == "json":
            filename = f"{report_type}_{timestamp}.json"
            filepath = self.reports_path / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        elif output_format == "markdown":
            filename = f"{report_type}_{timestamp}.md"
            filepath = self.reports_path / filename
            markdown_content = self._generate_markdown_report(report_data, report_type)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
        
        if filepath:
            print(f"✅ Report saved: {filepath}")
            return filepath
        else:
            print(f"❌ Unsupported format: {output_format}")
            return None
    
    def _generate_markdown_report(self, data: Dict, report_type: str) -> str:
        """Generate markdown formatted report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        md = f"# {report_type.title()} Report\n\n"
        md += f"**Generated**: {timestamp}\n\n"
        
        if report_type == "velocity":
            md += f"## Summary\n"
            md += f"- **Total Stories**: {data['total_stories']}\n"
            md += f"- **Status Breakdown**: {data['status_breakdown']}\n\n"
            
            md += f"## Epic Completion Rates\n"
            for epic, rate in data['epic_completion_rates'].items():
                md += f"- **{epic}**: {rate}%\n"
            
        elif report_type == "health":
            md += f"## Health Score: {data['health_score']}/100\n\n"
            md += f"## Quality Issues\n"
            for issue, count in data['quality_issues'].items():
                md += f"- **{issue.replace('_', ' ').title()}**: {count}\n"
            
            md += f"\n## Recommendations\n"
            for rec in data['recommendations']:
                md += f"- {rec}\n"
        
        return md


def main():
    parser = argparse.ArgumentParser(
        description="AI Sports Analytics Reporting Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all reports
  python scripts/generate_reports.py
  
  # Specific report type
  python scripts/generate_reports.py --type velocity
  
  # Output as markdown
  python scripts/generate_reports.py --type health --format markdown
  
  # Generate dashboard data
  python scripts/generate_reports.py --dashboard
        """
    )
    
    parser.add_argument("--type", choices=["velocity", "health", "priority", "workflow"],
                       help="Generate specific report type")
    parser.add_argument("--format", choices=["json", "markdown"], default="json",
                       help="Output format")
    parser.add_argument("--dashboard", action="store_true",
                       help="Generate dashboard data")
    parser.add_argument("--output", type=str,
                       help="Output directory (default: reports/)")
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = ReportGenerator()
    
    if args.dashboard:
        dashboard_data = generator.generate_dashboard_data()
        generator.save_report(dashboard_data, "dashboard", args.format)
        return
    
    if args.type:
        # Generate specific report
        data = None
        if args.type == "velocity":
            data = generator.generate_velocity_report()
        elif args.type == "health":
            data = generator.generate_backlog_health_report()
        elif args.type == "priority":
            data = generator.generate_priority_analytics()
        elif args.type == "workflow":
            data = generator.generate_workflow_metrics()
        
        if data:
            generator.save_report(data, args.type, args.format)
        else:
            print(f"❌ Unknown report type: {args.type}")
    else:
        # Generate all reports
        print("🔄 Generating comprehensive reports...")
        
        reports = {
            "velocity": generator.generate_velocity_report(),
            "health": generator.generate_backlog_health_report(),
            "priority": generator.generate_priority_analytics(),
            "workflow": generator.generate_workflow_metrics()
        }
        
        for report_type, data in reports.items():
            generator.save_report(data, report_type, args.format)
        
        # Also generate dashboard
        dashboard_data = generator.generate_dashboard_data()
        generator.save_report(dashboard_data, "dashboard", args.format)
        
        print(f"\n🎉 All reports generated in {args.format} format!")


if __name__ == "__main__":
    main()

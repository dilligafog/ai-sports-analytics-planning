#!/usr/bin/env python3
"""
GitHub Pages Dashboard Generator for AI Sports Analytics Planning

Creates interactive HTML dashboards with live metrics, charts, and 
real-time status updates for stakeholder visibility.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class DashboardGenerator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.reports_path = self.base_path / "reports"
        self.docs_path = self.base_path / "docs"
        self.docs_path.mkdir(exist_ok=True)
        
    def generate_html_dashboard(self, dashboard_data: Dict) -> str:
        """Generate complete HTML dashboard with interactive charts."""
        
        summary = dashboard_data.get("summary", {})
        velocity = dashboard_data.get("velocity", {})
        health = dashboard_data.get("health", {})
        priority = dashboard_data.get("priority", {})
        workflow = dashboard_data.get("workflow", {})
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Sports Analytics - Strategic Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 2px solid #e0e6ed;
            padding-bottom: 20px;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #6b7280;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        
        .last-updated {{
            display: inline-flex;
            align-items: center;
            background: #f3f4f6;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            color: #6b7280;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #ffffff, #f8fafc);
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }}
        
        .metric-value {{
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        
        .metric-label {{
            color: #6b7280;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .metric-subtitle {{
            color: #9ca3af;
            font-size: 0.8em;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }}
        
        .chart-container {{
            background: #ffffff;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        
        .chart-title {{
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 20px;
            color: #374151;
            text-align: center;
        }}
        
        .status-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .status-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            background: #f9fafb;
            border-radius: 8px;
            border-left: 4px solid #6366f1;
        }}
        
        .recommendations {{
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border-radius: 16px;
            padding: 24px;
            margin-top: 30px;
        }}
        
        .recommendations h3 {{
            color: #92400e;
            margin-bottom: 16px;
        }}
        
        .recommendations ul {{
            list-style: none;
        }}
        
        .recommendations li {{
            color: #a16207;
            margin-bottom: 8px;
            padding-left: 20px;
            position: relative;
        }}
        
        .recommendations li::before {{
            content: "💡";
            position: absolute;
            left: 0;
        }}
        
        .health-score {{
            background: linear-gradient(135deg, #10b981, #059669);
        }}
        
        .total-stories {{
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        }}
        
        .automation-rate {{
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
        }}
        
        .prioritized-stories {{
            background: linear-gradient(135deg, #f59e0b, #d97706);
        }}
        
        .metric-card .metric-value {{
            color: white;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }}
        
        .metric-card .metric-label,
        .metric-card .metric-subtitle {{
            color: rgba(255, 255, 255, 0.9);
        }}
        
        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .metric-value {{
                font-size: 2.5em;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🏈 AI Sports Analytics</h1>
            <div class="subtitle">Strategic Planning Dashboard</div>
            <div class="last-updated">
                🕒 Last Updated: {datetime.fromisoformat(summary.get('last_updated', '')).strftime('%Y-%m-%d %H:%M UTC') if summary.get('last_updated') else 'Unknown'}
            </div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card total-stories">
                <div class="metric-value">{summary.get('total_stories', 0)}</div>
                <div class="metric-label">Total Stories</div>
                <div class="metric-subtitle">Complete Backlog</div>
            </div>
            
            <div class="metric-card health-score">
                <div class="metric-value">{summary.get('health_score', 0)}<span style="font-size: 0.5em;">%</span></div>
                <div class="metric-label">Health Score</div>
                <div class="metric-subtitle">Backlog Quality</div>
            </div>
            
            <div class="metric-card prioritized-stories">
                <div class="metric-value">{summary.get('prioritized_stories', 0)}</div>
                <div class="metric-label">Prioritized</div>
                <div class="metric-subtitle">Ready for Dev</div>
            </div>
            
            <div class="metric-card automation-rate">
                <div class="metric-value">{summary.get('automation_rate', 0)}<span style="font-size: 0.5em;">%</span></div>
                <div class="metric-label">Automation</div>
                <div class="metric-subtitle">Auto-Generated</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-container">
                <div class="chart-title">Epic Completion Progress</div>
                <canvas id="epicChart" width="400" height="300"></canvas>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">Priority Distribution</div>
                <canvas id="priorityChart" width="400" height="300"></canvas>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-container">
                <div class="chart-title">Status Breakdown</div>
                <div class="status-grid">
                    {self._generate_status_items(velocity.get('status_breakdown', {}))}
                </div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">Workflow Efficiency</div>
                <canvas id="workflowChart" width="400" height="300"></canvas>
            </div>
        </div>
        
        {self._generate_recommendations_section(health, priority)}
        
    </div>
    
    <script>
        // Chart.js configuration
        Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
        Chart.defaults.plugins.legend.position = 'bottom';
        
        // Epic Completion Chart
        const epicData = {json.dumps(self._prepare_epic_chart_data(velocity))};
        new Chart(document.getElementById('epicChart'), {{
            type: 'doughnut',
            data: epicData,
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            usePointStyle: true,
                            padding: 15
                        }}
                    }}
                }}
            }}
        }});
        
        // Priority Distribution Chart
        const priorityData = {json.dumps(self._prepare_priority_chart_data(priority))};
        new Chart(document.getElementById('priorityChart'), {{
            type: 'bar',
            data: priorityData,
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
        
        // Workflow Efficiency Chart
        const workflowData = {json.dumps(self._prepare_workflow_chart_data(workflow))};
        new Chart(document.getElementById('workflowChart'), {{
            type: 'line',
            data: workflowData,
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        ticks: {{
                            callback: function(value) {{
                                return value + '%';
                            }}
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
        
        // Auto-refresh every 5 minutes
        setTimeout(() => {{
            location.reload();
        }}, 300000);
    </script>
</body>
</html>"""
        
        return html
    
    def _generate_status_items(self, status_breakdown: Dict) -> str:
        """Generate status grid items HTML."""
        status_colors = {
            "draft": "#6b7280",
            "backlog": "#3b82f6",
            "ready": "#10b981",
            "active": "#f59e0b",
            "completed": "#8b5cf6",
            "accepted": "#059669"
        }
        
        items = []
        for status, count in status_breakdown.items():
            color = status_colors.get(status, "#6b7280")
            items.append(f'''
                <div class="status-item" style="border-left-color: {color};">
                    <span>{status.title()}</span>
                    <strong>{count}</strong>
                </div>
            ''')
        
        return "".join(items)
    
    def _generate_recommendations_section(self, health: Dict, priority: Dict) -> str:
        """Generate recommendations section HTML."""
        all_recommendations = []
        all_recommendations.extend(health.get("recommendations", []))
        all_recommendations.extend(priority.get("priority_recommendations", []))
        
        if not all_recommendations:
            return ""
        
        recommendations_html = []
        for rec in all_recommendations[:5]:  # Limit to top 5
            recommendations_html.append(f"<li>{rec}</li>")
        
        return f'''
        <div class="recommendations">
            <h3>🎯 Strategic Recommendations</h3>
            <ul>
                {"".join(recommendations_html)}
            </ul>
        </div>
        '''
    
    def _prepare_epic_chart_data(self, velocity: Dict) -> Dict:
        """Prepare data for epic completion chart."""
        completion_rates = velocity.get("epic_completion_rates", {})
        
        if not completion_rates:
            return {"labels": [], "datasets": []}
        
        # Sort by completion rate and take top 8
        sorted_epics = sorted(completion_rates.items(), key=lambda x: x[1], reverse=True)[:8]
        
        labels = [epic.replace("_", " ").title() for epic, _ in sorted_epics]
        data = [rate for _, rate in sorted_epics]
        
        # Generate colors
        colors = [
            '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', 
            '#feca57', '#ff9ff3', '#54a0ff', '#5f27cd'
        ]
        
        return {
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": colors[:len(data)],
                "borderWidth": 0
            }]
        }
    
    def _prepare_priority_chart_data(self, priority: Dict) -> Dict:
        """Prepare data for priority distribution chart."""
        distribution = priority.get("priority_distribution", {})
        
        if not distribution:
            return {"labels": [], "datasets": []}
        
        # Define order for priority ranges
        priority_order = ["Critical (1-5)", "High (6-10)", "Medium (11-20)", "Low (21+)"]
        colors = ['#ef4444', '#f97316', '#eab308', '#22c55e']
        
        labels = []
        data = []
        backgroundColor = []
        
        for i, priority_range in enumerate(priority_order):
            if priority_range in distribution:
                labels.append(priority_range)
                data.append(distribution[priority_range])
                backgroundColor.append(colors[i])
        
        return {
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": backgroundColor,
                "borderWidth": 0
            }]
        }
    
    def _prepare_workflow_chart_data(self, workflow: Dict) -> Dict:
        """Prepare data for workflow efficiency chart."""
        efficiency = workflow.get("workflow_efficiency", 0)
        
        return {
            "labels": ["Current Efficiency"],
            "datasets": [{
                "label": "Efficiency %",
                "data": [efficiency],
                "borderColor": '#8b5cf6',
                "backgroundColor": 'rgba(139, 92, 246, 0.1)',
                "tension": 0.4,
                "fill": True
            }]
        }
    
    def generate_readme_badges(self, dashboard_data: Dict) -> str:
        """Generate README badge markdown."""
        summary = dashboard_data.get("summary", {})
        
        badges = [
            f"![Stories](https://img.shields.io/badge/Stories-{summary.get('total_stories', 0)}-blue)",
            f"![Health](https://img.shields.io/badge/Health-{summary.get('health_score', 0)}%25-{'green' if summary.get('health_score', 0) >= 80 else 'yellow' if summary.get('health_score', 0) >= 60 else 'red'})",
            f"![Prioritized](https://img.shields.io/badge/Prioritized-{summary.get('prioritized_stories', 0)}-purple)",
            f"![Automation](https://img.shields.io/badge/Automation-{summary.get('automation_rate', 0)}%25-orange)"
        ]
        
        return " ".join(badges)
    
    def save_dashboard(self, dashboard_data: Dict):
        """Save dashboard files."""
        # Generate HTML dashboard
        html_content = self.generate_html_dashboard(dashboard_data)
        
        # Save to docs/index.html for GitHub Pages
        index_path = self.docs_path / "index.html"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Save latest dashboard data as JSON
        data_path = self.docs_path / "dashboard-data.json"
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
        
        # Generate badges for README
        badges = self.generate_readme_badges(dashboard_data)
        badges_path = self.docs_path / "badges.md"
        with open(badges_path, 'w', encoding='utf-8') as f:
            f.write(badges)
        
        print(f"✅ Dashboard saved to: {index_path}")
        print(f"✅ Dashboard data saved to: {data_path}")
        print(f"✅ Badges saved to: {badges_path}")
        
        return {
            "dashboard_url": str(index_path),
            "data_url": str(data_path),
            "badges_url": str(badges_path)
        }


def main():
    import argparse
    from generate_reports import ReportGenerator
    
    parser = argparse.ArgumentParser(description="Generate GitHub Pages Dashboard")
    parser.add_argument("--data", type=str, help="Path to dashboard data JSON file")
    parser.add_argument("--live", action="store_true", help="Generate live dashboard from current data")
    
    args = parser.parse_args()
    
    dashboard_generator = DashboardGenerator()
    
    if args.data:
        # Load from specified file
        with open(args.data, 'r', encoding='utf-8') as f:
            dashboard_data = json.load(f)
    else:
        # Generate live data
        print("🔄 Generating live dashboard data...")
        report_generator = ReportGenerator()
        dashboard_data = report_generator.generate_dashboard_data()
    
    # Save dashboard
    result = dashboard_generator.save_dashboard(dashboard_data)
    
    print("\n🎉 Dashboard generated successfully!")
    print(f"🌐 View at: file://{result['dashboard_url']}")
    print("\nTo enable GitHub Pages:")
    print("1. Go to repository Settings > Pages")
    print("2. Select 'Deploy from a branch'")
    print("3. Choose 'main' branch and '/docs' folder")


if __name__ == "__main__":
    main()

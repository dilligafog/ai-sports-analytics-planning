#!/usr/bin/env python3
"""
Real Data Dashboard Generator

This script generates a professional dashboard using ONLY real project data.
No synthetic data, no fake people, no made-up metrics - just the actual project.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from collections import Counter

class RealDataDashboardGenerator:
    """Generate dashboard using only real project data."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.docs_path = self.base_path / "docs"
        
        # Load real data only
        self.prioritization_data = self._load_prioritization_data()
    
    def _load_prioritization_data(self) -> Dict[str, Any]:
        """Load real prioritization data."""
        try:
            with open(self.base_path / "backlog" / "PRIORITIZATION.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading prioritization data: {e}")
            return {}
    
    def analyze_real_data(self) -> Dict[str, Any]:
        """Analyze only real project data."""
        if not self.prioritization_data:
            return {}
        
        stories = self.prioritization_data.get("backlog", [])
        metadata = self.prioritization_data.get("metadata", {})
        
        # Real status counts
        status_counts = Counter(story.get("status", "unknown") for story in stories)
        
        # Real epic breakdown
        epic_counts = Counter(story.get("epic", "unknown") for story in stories)
        
        # Real priority distribution
        priority_dist = {}
        for story in stories:
            priority = story.get("priority", 0)
            if priority <= 5:
                key = "Critical (1-5)"
            elif priority <= 10:
                key = "High (6-10)"
            elif priority <= 20:
                key = "Medium (11-20)"
            else:
                key = "Low (21+)"
            priority_dist[key] = priority_dist.get(key, 0) + 1
        
        # Real completion rates by epic
        epic_completion = {}
        for epic in epic_counts:
            epic_stories = [s for s in stories if s.get("epic") == epic]
            completed = len([s for s in epic_stories if s.get("status") in ["accepted", "completed"]])
            total = len(epic_stories)
            epic_completion[epic] = round((completed / total * 100), 1) if total > 0 else 0
        
        # Calculate real health score based on actual data
        total_stories = len(stories)
        completed_stories = status_counts.get("accepted", 0) + status_counts.get("completed", 0)
        health_score = round((completed_stories / total_stories * 100), 1) if total_stories > 0 else 0
        
        return {
            "summary": {
                "total_stories": total_stories,
                "health_score": health_score,
                "prioritized_stories": len([s for s in stories if s.get("priority", 0) > 0]),
                "last_updated": metadata.get("last_updated", datetime.now().strftime("%Y-%m-%d")),
                "completed_count": completed_stories,
                "active_count": status_counts.get("active", 0),
                "ready_count": status_counts.get("ready", 0),
                "backlog_count": status_counts.get("backlog", 0)
            },
            "velocity": {
                "generated_at": datetime.now().isoformat(),
                "total_stories": total_stories,
                "status_breakdown": dict(status_counts),
                "epic_breakdown": dict(epic_counts),
                "epic_completion_rates": epic_completion,
                "priority_distribution": priority_dist
            },
            "quality_metrics": {
                "stories_with_estimates": len([s for s in stories if s.get("estimate")]),
                "stories_with_owners": len([s for s in stories if s.get("owner")]),
                "stories_with_dependencies": len([s for s in stories if s.get("dependencies")]),
                "average_priority": round(sum(s.get("priority", 0) for s in stories if s.get("priority", 0) > 0) / len([s for s in stories if s.get("priority", 0) > 0]), 1) if any(s.get("priority", 0) > 0 for s in stories) else 0
            }
        }
    
    def generate_real_dashboard_html(self) -> str:
        """Generate dashboard HTML using only real data."""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏈 AI Sports Analytics - Project Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #1f2937;
        }
        
        .dashboard {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }
        
        .header h1 {
            font-size: 3.5em;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        .subtitle {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.2em;
            margin-bottom: 20px;
        }
        
        .last-updated {
            display: inline-flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.9);
        }
        
        .section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .section-title {
            font-size: 1.8em;
            font-weight: 600;
            margin-bottom: 20px;
            color: #374151;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #ffffff, #f8fafc);
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 8px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-label {
            color: #6b7280;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }
        
        .chart-container {
            background: #ffffff;
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
            height: 350px;
        }
        
        .chart-title {
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 15px;
            color: #374151;
            text-align: center;
        }
        
        .chart-wrapper {
            position: relative;
            height: 280px;
            width: 100%;
        }
        
        .insights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .insight-card {
            background: linear-gradient(135deg, #f8fafc, #ffffff);
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04);
        }
        
        .insight-title {
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 10px;
            color: #374151;
        }
        
        .insight-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
            color: #059669;
        }
        
        .insight-description {
            color: #6b7280;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 2.5em;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🏈 AI Sports Analytics</h1>
            <div class="subtitle">Project Planning Dashboard</div>
            <div class="last-updated" id="lastUpdated">
                🕒 Loading...
            </div>
        </div>
        
        <!-- Project Overview -->
        <div class="section">
            <h2 class="section-title">📊 Project Overview</h2>
            <div class="metrics-grid" id="projectMetrics">
                <!-- Metrics will be populated by JavaScript -->
            </div>
        </div>
        
        <!-- Story Analytics -->
        <div class="section">
            <h2 class="section-title">📈 Story Analytics</h2>
            <div class="charts-grid">
                <div class="chart-container">
                    <h3 class="chart-title">Status Distribution</h3>
                    <div class="chart-wrapper">
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
                <div class="chart-container">
                    <h3 class="chart-title">Epic Breakdown</h3>
                    <div class="chart-wrapper">
                        <canvas id="epicChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Priority & Quality -->
        <div class="section">
            <h2 class="section-title">🎯 Priority & Quality</h2>
            <div class="charts-grid">
                <div class="chart-container">
                    <h3 class="chart-title">Priority Distribution</h3>
                    <div class="chart-wrapper">
                        <canvas id="priorityChart"></canvas>
                    </div>
                </div>
                <div class="chart-container">
                    <h3 class="chart-title">Epic Completion Rates</h3>
                    <div class="chart-wrapper">
                        <canvas id="completionChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Quality Insights -->
        <div class="section">
            <h2 class="section-title">🔍 Quality Insights</h2>
            <div class="insights-grid" id="qualityInsights">
                <!-- Quality insights will be populated by JavaScript -->
            </div>
        </div>
    </div>
    
    <script>
        // Global data variable
        let dashboardData = null;
        
        // Load and render dashboard
        async function loadDashboard() {
            try {
                const response = await fetch('real-dashboard-data.json');
                dashboardData = await response.json();
                renderDashboard();
            } catch (error) {
                console.error('Error loading dashboard data:', error);
                showError('Failed to load dashboard data.');
            }
        }
        
        function showError(message) {
            document.querySelector('.dashboard').innerHTML = `
                <div style="background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 20px; border-radius: 12px; margin: 20px;">
                    <h3>⚠️ Error</h3>
                    <p>${message}</p>
                </div>
            `;
        }
        
        function renderDashboard() {
            if (!dashboardData) return;
            
            updateLastUpdated();
            renderProjectMetrics();
            renderStatusChart();
            renderEpicChart();
            renderPriorityChart();
            renderCompletionChart();
            renderQualityInsights();
        }
        
        function updateLastUpdated() {
            const lastUpdated = new Date(dashboardData.summary?.last_updated || Date.now());
            document.getElementById('lastUpdated').textContent = 
                `🕒 Last Updated: ${lastUpdated.toLocaleDateString()}`;
        }
        
        function renderProjectMetrics() {
            const container = document.getElementById('projectMetrics');
            const { summary } = dashboardData;
            
            const metrics = [
                { value: summary?.total_stories || 0, label: 'Total Stories' },
                { value: `${summary?.health_score || 0}%`, label: 'Completion Rate' },
                { value: summary?.completed_count || 0, label: 'Completed' },
                { value: summary?.active_count || 0, label: 'Active' },
                { value: summary?.ready_count || 0, label: 'Ready' },
                { value: summary?.backlog_count || 0, label: 'Backlog' }
            ];
            
            container.innerHTML = metrics.map(metric => `
                <div class="metric-card">
                    <div class="metric-value">${metric.value}</div>
                    <div class="metric-label">${metric.label}</div>
                </div>
            `).join('');
        }
        
        function renderStatusChart() {
            const ctx = document.getElementById('statusChart').getContext('2d');
            const statusData = dashboardData.velocity.status_breakdown;
            
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(statusData),
                    datasets: [{
                        data: Object.values(statusData),
                        backgroundColor: [
                            '#22c55e', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });
        }
        
        function renderEpicChart() {
            const ctx = document.getElementById('epicChart').getContext('2d');
            const epicData = dashboardData.velocity.epic_breakdown;
            
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(epicData),
                    datasets: [{
                        label: 'Stories',
                        data: Object.values(epicData),
                        backgroundColor: '#667eea'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
        
        function renderPriorityChart() {
            const ctx = document.getElementById('priorityChart').getContext('2d');
            const priorityData = dashboardData.velocity.priority_distribution;
            
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: Object.keys(priorityData),
                    datasets: [{
                        data: Object.values(priorityData),
                        backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#6b7280']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });
        }
        
        function renderCompletionChart() {
            const ctx = document.getElementById('completionChart').getContext('2d');
            const completionData = dashboardData.velocity.epic_completion_rates;
            
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(completionData),
                    datasets: [{
                        label: 'Completion %',
                        data: Object.values(completionData),
                        backgroundColor: Object.values(completionData).map(rate => 
                            rate >= 75 ? '#22c55e' : 
                            rate >= 50 ? '#f59e0b' : '#ef4444'
                        )
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true, max: 100 }
                    }
                }
            });
        }
        
        function renderQualityInsights() {
            const container = document.getElementById('qualityInsights');
            const { quality_metrics, summary } = dashboardData;
            
            const insights = [
                {
                    title: 'Stories with Estimates',
                    value: quality_metrics?.stories_with_estimates || 0,
                    description: `${Math.round((quality_metrics?.stories_with_estimates || 0) / summary?.total_stories * 100)}% of total stories`
                },
                {
                    title: 'Stories with Owners',
                    value: quality_metrics?.stories_with_owners || 0,
                    description: `${Math.round((quality_metrics?.stories_with_owners || 0) / summary?.total_stories * 100)}% have assigned owners`
                },
                {
                    title: 'Average Priority',
                    value: quality_metrics?.average_priority || 0,
                    description: 'Lower numbers indicate higher priority'
                },
                {
                    title: 'Stories with Dependencies',
                    value: quality_metrics?.stories_with_dependencies || 0,
                    description: 'Stories that depend on other work'
                }
            ];
            
            container.innerHTML = insights.map(insight => `
                <div class="insight-card">
                    <div class="insight-title">${insight.title}</div>
                    <div class="insight-value">${insight.value}</div>
                    <div class="insight-description">${insight.description}</div>
                </div>
            `).join('');
        }
        
        // Initialize dashboard
        loadDashboard();
    </script>
</body>
</html>'''
    
    def generate_real_dashboard(self):
        """Generate the real data dashboard."""
        # Analyze real data
        dashboard_data = self.analyze_real_data()
        
        # Save real data file
        data_path = self.docs_path / "real-dashboard-data.json"
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
        
        # Generate and save HTML
        html_content = self.generate_real_dashboard_html()
        html_path = self.docs_path / "index.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Real data dashboard saved: {html_path}")
        print(f"✅ Real dashboard data saved: {data_path}")
        print(f"🌐 View dashboard at: file://{html_path.absolute()}")
        
        # Clean up any synthetic files
        self._cleanup_synthetic_files()
        
        return html_path
    
    def _cleanup_synthetic_files(self):
        """Remove synthetic data files to avoid confusion."""
        synthetic_files = [
            self.docs_path / "premium_dashboard.html",
            self.docs_path / "enhanced-dashboard-data.json",
            self.docs_path / "enhanced_index.html"
        ]
        
        for file_path in synthetic_files:
            if file_path.exists():
                file_path.unlink()
                print(f"🧹 Removed synthetic file: {file_path.name}")

def main():
    """Main function to generate real data dashboard."""
    try:
        generator = RealDataDashboardGenerator()
        dashboard_path = generator.generate_real_dashboard()
        
        print(f"\n🎯 Real Data Dashboard Generated!")
        print(f"📊 Using only actual project data:")
        print(f"   - {generator.prioritization_data.get('metadata', {}).get('total_backlog_stories', 0)} real stories")
        print(f"   - Real epic breakdown and status tracking")
        print(f"   - Actual completion rates and priorities")
        print(f"   - No synthetic data or fake people")
        
    except Exception as e:
        print(f"❌ Error generating real data dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

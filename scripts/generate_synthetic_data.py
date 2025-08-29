#!/usr/bin/env python3
"""
Synthetic Dataset Generator for AI Sports Analytics

This script generates realistic synthetic data to populate the analytics dashboard
with compelling stories and trends that demonstrate the full power of the system.
"""

import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import math

class SyntheticDataGenerator:
    """Generate realistic synthetic data for analytics demonstration."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.backlog_path = self.base_path / "backlog" / "PRIORITIZATION.json"
        self.data_path = self.base_path / "synthetic_data"
        self.data_path.mkdir(exist_ok=True)
        
        # Load current data as baseline
        with open(self.backlog_path, 'r', encoding='utf-8') as f:
            self.current_data = json.load(f)
        
        # Configure realistic parameters
        self.epic_themes = {
            "core": {"business_value": "high", "complexity": "high", "velocity": 3.2},
            "ui": {"business_value": "high", "complexity": "medium", "velocity": 4.8},
            "infrastructure": {"business_value": "medium", "complexity": "high", "velocity": 2.1},
            "social": {"business_value": "medium", "complexity": "medium", "velocity": 3.9},
            "modeling": {"business_value": "high", "complexity": "high", "velocity": 2.8},
            "ingestion": {"business_value": "medium", "complexity": "medium", "velocity": 4.2},
            "adhoc": {"business_value": "low", "complexity": "low", "velocity": 6.1}
        }
        
        self.team_members = [
            {"name": "Alex Chen", "expertise": ["core", "modeling"], "velocity": 5.2},
            {"name": "Sarah Rodriguez", "expertise": ["ui", "social"], "velocity": 4.8},
            {"name": "David Kim", "expertise": ["infrastructure", "ingestion"], "velocity": 3.9},
            {"name": "Emily Johnson", "expertise": ["core", "ui"], "velocity": 4.5},
            {"name": "Michael Zhang", "expertise": ["modeling", "infrastructure"], "velocity": 4.1},
            {"name": "Jessica Wu", "expertise": ["social", "adhoc"], "velocity": 5.0}
        ]
    
    def generate_historical_velocity(self, weeks: int = 16) -> List[Dict[str, Any]]:
        """Generate realistic historical velocity data with trends and seasonality."""
        velocity_data = []
        base_velocity = 4.2
        
        # Simulate realistic project phases
        for week in range(weeks):
            # Project phase influence
            if week < 4:  # Initial ramp-up
                phase_multiplier = 0.6 + (week * 0.1)
            elif week < 8:  # Productive phase
                phase_multiplier = 1.0 + (week - 4) * 0.05
            elif week < 12:  # Complexity phase
                phase_multiplier = 1.2 - (week - 8) * 0.03
            else:  # Optimization phase
                phase_multiplier = 1.0 + (week - 12) * 0.02
            
            # Add realistic variance
            seasonal_effect = math.sin(week * 0.3) * 0.15
            random_variance = random.gauss(0, 0.1)
            
            weekly_velocity = max(0.5, base_velocity * phase_multiplier + seasonal_effect + random_variance)
            
            # Epic breakdown for this week
            epic_completions = {}
            remaining_velocity = weekly_velocity
            
            for epic, config in self.epic_themes.items():
                epic_share = max(0, random.gauss(config["velocity"] / 30, 0.1))
                epic_completions[epic] = min(remaining_velocity, epic_share)
                remaining_velocity -= epic_completions[epic]
            
            velocity_data.append({
                "week": week + 1,
                "date": (datetime.now() - timedelta(weeks=weeks-week)).strftime("%Y-%m-%d"),
                "total_velocity": round(weekly_velocity, 1),
                "epic_breakdown": {k: round(v, 1) for k, v in epic_completions.items()},
                "cumulative_stories": round(sum(v["total_velocity"] for v in velocity_data) + weekly_velocity, 1),
                "team_capacity": round(weekly_velocity / len(self.team_members), 1)
            })
        
        return velocity_data
    
    def generate_team_performance(self) -> Dict[str, Any]:
        """Generate realistic team performance metrics."""
        team_data = {}
        
        for member in self.team_members:
            # Generate performance over time
            weekly_performance = []
            base_velocity = member["velocity"]
            
            for week in range(12):
                # Performance variance based on expertise alignment
                expertise_boost = random.choice([0.8, 1.0, 1.2, 1.0])  # Sometimes working in expertise area
                learning_curve = 0.9 + (week * 0.01)  # Slight improvement over time
                variance = random.gauss(1.0, 0.15)
                
                weekly_velocity = max(0.5, base_velocity * expertise_boost * learning_curve * variance)
                
                weekly_performance.append({
                    "week": week + 1,
                    "velocity": round(weekly_velocity, 1),
                    "stories_completed": random.randint(2, 7),
                    "epic_focus": random.choice(member["expertise"]),
                    "capacity_utilization": round(min(100, weekly_velocity / base_velocity * 100), 1)
                })
            
            team_data[member["name"]] = {
                "expertise": member["expertise"],
                "base_velocity": member["velocity"],
                "avg_velocity": round(sum(p["velocity"] for p in weekly_performance) / len(weekly_performance), 1),
                "total_stories": sum(p["stories_completed"] for p in weekly_performance),
                "performance_history": weekly_performance,
                "specialization_score": round(random.uniform(75, 95), 1),
                "collaboration_score": round(random.uniform(80, 98), 1)
            }
        
        return team_data
    
    def generate_epic_health_metrics(self) -> Dict[str, Any]:
        """Generate comprehensive epic health and progress metrics."""
        epic_health = {}
        
        for epic, config in self.epic_themes.items():
            # Current stories in this epic
            epic_stories = [s for s in self.current_data.get("backlog", []) if s.get("epic") == epic]
            total_stories = len(epic_stories)
            
            if total_stories == 0:
                continue
            
            completed = len([s for s in epic_stories if s.get("status") in ["completed", "accepted"]])
            in_progress = len([s for s in epic_stories if s.get("status") in ["active", "ready"]])
            
            # Health indicators
            completion_rate = (completed / total_stories) * 100 if total_stories > 0 else 0
            velocity_trend = random.choice(["increasing", "stable", "decreasing"])
            
            # Risk factors
            risk_factors = []
            risk_score = 0
            
            if completion_rate < 30:
                risk_factors.append("Low completion rate")
                risk_score += 20
            
            if in_progress > total_stories * 0.4:
                risk_factors.append("Too much WIP")
                risk_score += 15
            
            unestimated = len([s for s in epic_stories if not s.get("estimate")])
            if unestimated > total_stories * 0.2:
                risk_factors.append("Many unestimated stories")
                risk_score += 10
            
            # Business metrics
            estimated_business_value = random.randint(50000, 500000) if config["business_value"] == "high" else random.randint(10000, 100000)
            roi_estimate = round(estimated_business_value / max(1, total_stories * 1000), 1)
            
            epic_health[epic] = {
                "total_stories": total_stories,
                "completed_stories": completed,
                "in_progress_stories": in_progress,
                "completion_rate": round(completion_rate, 1),
                "velocity_trend": velocity_trend,
                "business_value": config["business_value"],
                "complexity_rating": config["complexity"],
                "risk_score": min(100, risk_score),
                "risk_factors": risk_factors,
                "estimated_business_value": estimated_business_value,
                "roi_estimate": roi_estimate,
                "health_score": round(max(0, 100 - risk_score), 1),
                "projected_completion": (datetime.now() + timedelta(weeks=random.randint(2, 12))).strftime("%Y-%m-%d"),
                "resource_allocation": round(random.uniform(0.8, 2.5), 1)  # FTE allocation
            }
        
        return epic_health
    
    def generate_quality_trends(self) -> Dict[str, Any]:
        """Generate quality improvement trends over time."""
        weeks = 12
        quality_history = []
        
        base_quality = 65  # Starting quality score
        
        for week in range(weeks):
            # Quality improvement trend with some variance
            improvement_rate = 2.5  # Points per week
            variance = random.gauss(0, 1.5)
            
            weekly_quality = min(100, base_quality + (week * improvement_rate) + variance)
            
            # Quality components
            components = {
                "estimates_coverage": min(100, 60 + (week * 3) + random.gauss(0, 2)),
                "acceptance_criteria": min(100, 50 + (week * 4) + random.gauss(0, 2)),
                "priority_assignment": min(100, 70 + (week * 2.5) + random.gauss(0, 1.5)),
                "owner_assignment": min(100, 80 + (week * 1.5) + random.gauss(0, 1)),
                "story_freshness": min(100, 85 + (week * 1) + random.gauss(0, 2))
            }
            
            quality_history.append({
                "week": week + 1,
                "date": (datetime.now() - timedelta(weeks=weeks-week)).strftime("%Y-%m-%d"),
                "overall_quality": round(weekly_quality, 1),
                "components": {k: round(v, 1) for k, v in components.items()},
                "improvement_actions": random.randint(2, 8),
                "quality_issues_resolved": random.randint(1, 5)
            })
        
        return {
            "quality_history": quality_history,
            "current_quality": round(quality_history[-1]["overall_quality"], 1),
            "improvement_rate": round((quality_history[-1]["overall_quality"] - quality_history[0]["overall_quality"]) / weeks, 1),
            "quality_trend": "improving",
            "target_quality": 95,
            "weeks_to_target": max(1, math.ceil((95 - quality_history[-1]["overall_quality"]) / 2.5))
        }
    
    def generate_predictive_analytics(self) -> Dict[str, Any]:
        """Generate sophisticated predictive analytics and forecasting."""
        current_stories = self.current_data.get("backlog", [])
        total_stories = len(current_stories)
        completed = len([s for s in current_stories if s.get("status") in ["completed", "accepted"]])
        
        # Monte Carlo simulation for completion forecasting
        simulations = 1000
        completion_scenarios = []
        
        for _ in range(simulations):
            # Random walk for velocity
            current_velocity = 4.2
            weeks_to_complete = 0
            remaining = total_stories - completed
            
            while remaining > 0 and weeks_to_complete < 52:  # Max 1 year
                # Velocity variance
                velocity_change = random.gauss(0, 0.3)
                current_velocity = max(0.5, current_velocity + velocity_change)
                
                # Complete stories this week
                completed_this_week = min(remaining, max(0, int(random.expovariate(1/current_velocity))))
                remaining -= completed_this_week
                weeks_to_complete += 1
            
            completion_scenarios.append(weeks_to_complete)
        
        # Statistical analysis
        completion_scenarios.sort()
        p50 = completion_scenarios[len(completion_scenarios) // 2]
        p80 = completion_scenarios[int(len(completion_scenarios) * 0.8)]
        p95 = completion_scenarios[int(len(completion_scenarios) * 0.95)]
        
        # Risk analysis
        risks = [
            {
                "type": "velocity_decline",
                "probability": 25,
                "impact": "2-4 week delay",
                "mitigation": "Increase team capacity or reduce scope"
            },
            {
                "type": "scope_creep",
                "probability": 40,
                "impact": "10-20% more stories",
                "mitigation": "Strict change control process"
            },
            {
                "type": "technical_debt",
                "probability": 30,
                "impact": "Velocity reduction 15-25%",
                "mitigation": "Dedicate sprint to technical debt"
            }
        ]
        
        # Success factors
        success_factors = {
            "team_stability": round(random.uniform(85, 95), 1),
            "requirement_clarity": round(random.uniform(75, 90), 1),
            "technical_feasibility": round(random.uniform(80, 95), 1),
            "stakeholder_engagement": round(random.uniform(70, 90), 1),
            "resource_availability": round(random.uniform(80, 95), 1)
        }
        
        overall_success_probability = sum(success_factors.values()) / len(success_factors)
        
        return {
            "completion_forecast": {
                "most_likely_weeks": p50,
                "conservative_weeks": p80,
                "pessimistic_weeks": p95,
                "confidence_intervals": {
                    "50%": [p50 - 1, p50 + 1],
                    "80%": [completion_scenarios[int(len(completion_scenarios) * 0.1)], p80],
                    "95%": [completion_scenarios[int(len(completion_scenarios) * 0.05)], p95]
                }
            },
            "risk_analysis": risks,
            "success_factors": success_factors,
            "overall_success_probability": round(overall_success_probability, 1),
            "monte_carlo_runs": simulations,
            "model_accuracy": round(random.uniform(82, 94), 1)
        }
    
    def generate_business_intelligence(self) -> Dict[str, Any]:
        """Generate business intelligence and ROI analysis."""
        
        # Cost analysis
        team_cost_per_week = sum(member["velocity"] * 2000 for member in self.team_members)  # $2000 per story point
        total_project_cost = team_cost_per_week * 16  # 16 weeks of work
        
        # Value analysis by epic
        epic_values = {}
        total_business_value = 0
        
        for epic, config in self.epic_themes.items():
            if config["business_value"] == "high":
                value = random.randint(200000, 800000)
            elif config["business_value"] == "medium":
                value = random.randint(50000, 300000)
            else:
                value = random.randint(10000, 100000)
            
            epic_values[epic] = {
                "estimated_value": value,
                "implementation_cost": random.randint(20000, 150000),
                "roi_percentage": round(((value - epic_values.get(epic, {}).get("implementation_cost", 50000)) / max(1, epic_values.get(epic, {}).get("implementation_cost", 50000))) * 100, 1),
                "payback_period_months": random.randint(3, 18),
                "risk_adjusted_value": round(value * random.uniform(0.7, 0.95), 0)
            }
            
            total_business_value += value
        
        # Market analysis
        market_impact = {
            "user_acquisition": {
                "projected_new_users": random.randint(5000, 50000),
                "user_retention_improvement": round(random.uniform(5, 25), 1),
                "engagement_increase": round(random.uniform(10, 40), 1)
            },
            "revenue_impact": {
                "projected_annual_revenue": random.randint(500000, 2000000),
                "revenue_per_user_increase": round(random.uniform(5, 35), 1),
                "market_share_gain": round(random.uniform(0.5, 5), 1)
            },
            "competitive_advantage": {
                "time_to_market_advantage": f"{random.randint(2, 8)} months",
                "feature_differentiation": random.randint(3, 8),
                "patent_opportunities": random.randint(0, 3)
            }
        }
        
        return {
            "cost_analysis": {
                "total_project_cost": total_project_cost,
                "cost_per_story": round(total_project_cost / len(self.current_data.get("backlog", [])), 0),
                "team_cost_per_week": team_cost_per_week,
                "burn_rate": round(team_cost_per_week / 7, 0)
            },
            "value_analysis": {
                "total_business_value": total_business_value,
                "epic_breakdown": epic_values,
                "overall_roi": round(((total_business_value - total_project_cost) / total_project_cost) * 100, 1),
                "npv_analysis": round(total_business_value * 0.85 - total_project_cost, 0)
            },
            "market_impact": market_impact,
            "investment_metrics": {
                "irr_percentage": round(random.uniform(25, 65), 1),
                "payback_period_months": random.randint(8, 24),
                "break_even_users": random.randint(2000, 15000)
            }
        }
    
    def generate_comprehensive_dataset(self) -> Dict[str, Any]:
        """Generate the complete synthetic dataset."""
        return {
            "generated_at": datetime.now().isoformat(),
            "data_version": "1.0",
            "baseline_info": {
                "total_stories": len(self.current_data.get("backlog", [])),
                "team_size": len(self.team_members),
                "project_duration_weeks": 16
            },
            "historical_velocity": self.generate_historical_velocity(),
            "team_performance": self.generate_team_performance(),
            "epic_health": self.generate_epic_health_metrics(),
            "quality_trends": self.generate_quality_trends(),
            "predictive_analytics": self.generate_predictive_analytics(),
            "business_intelligence": self.generate_business_intelligence()
        }
    
    def save_dataset(self) -> Path:
        """Save the comprehensive synthetic dataset."""
        dataset = self.generate_comprehensive_dataset()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"synthetic_analytics_dataset_{timestamp}.json"
        filepath = self.data_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        
        # Also save as latest
        latest_path = self.data_path / "latest_dataset.json"
        with open(latest_path, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Synthetic dataset saved: {filepath}")
        print(f"✅ Latest dataset saved: {latest_path}")
        
        # Generate summary
        self._generate_dataset_summary(dataset)
        
        return filepath
    
    def _generate_dataset_summary(self, dataset: Dict[str, Any]):
        """Generate a human-readable summary of the dataset."""
        summary = [
            "# Synthetic Analytics Dataset Summary",
            f"Generated: {dataset['generated_at']}",
            "",
            "## Dataset Overview",
            f"- **Total Stories**: {dataset['baseline_info']['total_stories']}",
            f"- **Team Size**: {dataset['baseline_info']['team_size']} members",
            f"- **Project Duration**: {dataset['baseline_info']['project_duration_weeks']} weeks",
            "",
            "## Historical Data",
            f"- **Velocity History**: {len(dataset['historical_velocity'])} weeks of data",
            f"- **Team Performance**: Individual metrics for {len(dataset['team_performance'])} team members",
            f"- **Quality Trends**: {len(dataset['quality_trends']['quality_history'])} weeks of improvement data",
            "",
            "## Analytics Included",
            "- 📈 **Velocity Analytics**: Historical trends, epic breakdowns, team capacity",
            "- 👥 **Team Performance**: Individual velocity, expertise alignment, collaboration scores",
            "- 🎯 **Epic Health**: Business value, completion rates, risk factors",
            "- 📊 **Quality Metrics**: Improvement trends, component analysis",
            "- 🔮 **Predictive Analytics**: Monte Carlo forecasting, risk analysis",
            "- 💰 **Business Intelligence**: ROI analysis, market impact, investment metrics",
            "",
            "## Key Insights",
            f"- **Current Quality Score**: {dataset['quality_trends']['current_quality']}%",
            f"- **Success Probability**: {dataset['predictive_analytics']['overall_success_probability']}%",
            f"- **Project ROI**: {dataset['business_intelligence']['value_analysis']['overall_roi']}%",
            f"- **Completion Forecast**: {dataset['predictive_analytics']['completion_forecast']['most_likely_weeks']} weeks",
            "",
            "## Usage",
            "This dataset powers the enterprise analytics dashboard with realistic,",
            "compelling data that demonstrates advanced project management capabilities."
        ]
        
        summary_path = self.data_path / "dataset_summary.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary))
        
        print(f"📋 Dataset summary saved: {summary_path}")

def main():
    """Main function to generate synthetic datasets."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic analytics datasets")
    parser.add_argument("--output", help="Output directory for datasets")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    try:
        generator = SyntheticDataGenerator()
        
        if args.output:
            generator.data_path = Path(args.output)
            generator.data_path.mkdir(exist_ok=True)
        
        filepath = generator.save_dataset()
        
        if args.verbose:
            print(f"\n📊 Synthetic dataset generation complete!")
            print(f"🎯 Dataset includes:")
            print(f"   - 16 weeks of historical velocity data")
            print(f"   - 6 team member performance profiles") 
            print(f"   - Epic health metrics for all epics")
            print(f"   - 12 weeks of quality improvement trends")
            print(f"   - Monte Carlo completion forecasting")
            print(f"   - Comprehensive business intelligence")
            print(f"📁 Files created in: {generator.data_path}")
        
    except Exception as e:
        print(f"❌ Error generating synthetic dataset: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test and validate the AI Sports Analytics reporting system.

Runs comprehensive tests on data integrity, report generation,
and dashboard functionality before deployment.
"""

import json
import sys
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

def test_data_files() -> Tuple[bool, str]:
    """Test that required data files exist and are valid."""
    try:
        base_path = Path(".")
        
        # Check PRIORITIZATION.json
        prioritization_file = base_path / "backlog" / "PRIORITIZATION.json"
        if not prioritization_file.exists():
            return False, "PRIORITIZATION.json not found"
        
        with open(prioritization_file, 'r', encoding='utf-8') as f:
            prioritization_data = json.load(f)
        
        if "backlog" not in prioritization_data:
            return False, "PRIORITIZATION.json missing 'backlog' key"
        
        # Check COMPLETE_BACKLOG.json
        backlog_file = base_path / "backlog" / "COMPLETE_BACKLOG.json"
        if not backlog_file.exists():
            return False, "COMPLETE_BACKLOG.json not found"
        
        with open(backlog_file, 'r', encoding='utf-8') as f:
            backlog_data = json.load(f)
        
        if "backlog" not in backlog_data:
            return False, "COMPLETE_BACKLOG.json missing 'backlog' key"
        
        return True, f"Data files valid: {len(prioritization_data['backlog'])} prioritized stories, {len(backlog_data['backlog'])} total stories"
        
    except Exception as e:
        return False, f"Data file validation error: {str(e)}"

def test_report_generation() -> Tuple[bool, str]:
    """Test report generation functionality."""
    try:
        # Import and test report generator
        sys.path.append('scripts')
        from generate_reports import ReportGenerator
        
        generator = ReportGenerator()
        
        # Test velocity report
        velocity_report = generator.generate_velocity_report()
        if "total_stories" not in velocity_report:
            return False, "Velocity report missing total_stories"
        
        # Test health report
        health_report = generator.generate_backlog_health_report()
        if "health_score" not in health_report:
            return False, "Health report missing health_score"
        
        # Test priority report
        priority_report = generator.generate_priority_analytics()
        if "total_prioritized" not in priority_report:
            return False, "Priority report missing total_prioritized"
        
        # Test workflow report
        workflow_report = generator.generate_workflow_metrics()
        if "automation_adoption" not in workflow_report:
            return False, "Workflow report missing automation_adoption"
        
        # Test dashboard data generation
        dashboard_data = generator.generate_dashboard_data()
        if "summary" not in dashboard_data:
            return False, "Dashboard data missing summary"
        
        return True, f"All report types generated successfully (velocity, health, priority, workflow, dashboard)"
        
    except Exception as e:
        return False, f"Report generation error: {str(e)}"

def test_dashboard_generation() -> Tuple[bool, str]:
    """Test dashboard HTML generation."""
    try:
        # Import and test dashboard generator
        sys.path.append('scripts')
        from generate_dashboard import DashboardGenerator
        from generate_reports import ReportGenerator
        
        # Generate test data
        report_generator = ReportGenerator()
        dashboard_data = report_generator.generate_dashboard_data()
        
        # Generate dashboard
        dashboard_generator = DashboardGenerator()
        html_content = dashboard_generator.generate_html_dashboard(dashboard_data)
        
        # Basic HTML validation
        if "<html" not in html_content:
            return False, "Generated HTML missing html tag"
        
        if "AI Sports Analytics" not in html_content:
            return False, "Generated HTML missing title"
        
        if "Chart.js" not in html_content:
            return False, "Generated HTML missing Chart.js"
        
        # Test badge generation
        badges = dashboard_generator.generate_readme_badges(dashboard_data)
        if "Stories" not in badges:
            return False, "Badge generation failed"
        
        return True, f"Dashboard HTML generated successfully ({len(html_content)} characters)"
        
    except Exception as e:
        return False, f"Dashboard generation error: {str(e)}"

def test_script_execution() -> Tuple[bool, str]:
    """Test that scripts can be executed directly."""
    try:
        import subprocess
        import os
        
        # Test report generation script
        result = subprocess.run([
            sys.executable, "scripts/generate_reports.py", "--type", "velocity"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode != 0:
            return False, f"Report script execution failed: {result.stderr}"
        
        # Test dashboard generation script
        result = subprocess.run([
            sys.executable, "scripts/generate_dashboard.py", "--live"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode != 0:
            return False, f"Dashboard script execution failed: {result.stderr}"
        
        return True, "Scripts execute successfully"
        
    except Exception as e:
        return False, f"Script execution error: {str(e)}"

def test_output_validation() -> Tuple[bool, str]:
    """Test that generated outputs are valid."""
    try:
        reports_path = Path("reports")
        docs_path = Path("docs")
        
        # Check if reports directory exists and has content
        if not reports_path.exists():
            return False, "Reports directory not created"
        
        # Check for generated report files
        json_reports = list(reports_path.glob("*.json"))
        if not json_reports:
            return False, "No JSON reports generated"
        
        # Validate JSON format
        for report_file in json_reports[:3]:  # Check first 3
            with open(report_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
            
            if "generated_at" not in report_data:
                return False, f"Report {report_file.name} missing generated_at timestamp"
        
        # Check dashboard output
        if docs_path.exists():
            index_file = docs_path / "index.html"
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                if len(html_content) < 1000:
                    return False, "Generated dashboard HTML too short"
        
        return True, f"Output validation passed: {len(json_reports)} reports generated"
        
    except Exception as e:
        return False, f"Output validation error: {str(e)}"

def run_comprehensive_test() -> Dict[str, Any]:
    """Run all tests and return results."""
    tests = [
        ("Data Files", test_data_files),
        ("Report Generation", test_report_generation),
        ("Dashboard Generation", test_dashboard_generation),
        ("Script Execution", test_script_execution),
        ("Output Validation", test_output_validation)
    ]
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": [],
        "summary": {
            "total": len(tests),
            "passed": 0,
            "failed": 0
        }
    }
    
    print("🧪 Running AI Sports Analytics Reporting System Tests\n")
    
    for test_name, test_func in tests:
        print(f"🔍 Testing: {test_name}...")
        
        try:
            passed, message = test_func()
            status = "✅ PASS" if passed else "❌ FAIL"
            
            test_result = {
                "name": test_name,
                "passed": passed,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            
            results["tests"].append(test_result)
            
            if passed:
                results["summary"]["passed"] += 1
                print(f"   {status}: {message}")
            else:
                results["summary"]["failed"] += 1
                print(f"   {status}: {message}")
                
        except Exception as e:
            test_result = {
                "name": test_name,
                "passed": False,
                "message": f"Test execution error: {str(e)}",
                "error": traceback.format_exc(),
                "timestamp": datetime.now().isoformat()
            }
            
            results["tests"].append(test_result)
            results["summary"]["failed"] += 1
            print(f"   ❌ FAIL: {str(e)}")
        
        print()
    
    # Print summary
    total = results["summary"]["total"]
    passed = results["summary"]["passed"]
    failed = results["summary"]["failed"]
    
    print("📊 Test Summary:")
    print(f"   Total Tests: {total}")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print(f"   Success Rate: {(passed/total)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! Reporting system is ready for deployment.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review and fix issues before deployment.")
    
    return results

def main():
    """Main test execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test AI Sports Analytics Reporting System")
    parser.add_argument("--save-results", action="store_true", help="Save test results to file")
    parser.add_argument("--exit-on-failure", action="store_true", help="Exit with error code if tests fail")
    
    args = parser.parse_args()
    
    # Run tests
    results = run_comprehensive_test()
    
    # Save results if requested
    if args.save_results:
        results_file = Path("reports") / f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results_file.parent.mkdir(exist_ok=True)
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Test results saved to: {results_file}")
    
    # Exit with appropriate code
    if args.exit_on_failure and results["summary"]["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test Case Manager for CDT Code Mapper
Tracks which test cases pass both accuracy and consistency tests.
Allows focused testing on cases that need refinement.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from test_reference import TEST_CASES, get_test_cases_by_category, get_all_categories
from test_cases import run_comprehensive_tests
from test_consistency import parallel_test_consistency
from config import OLLAMA_URL, OLLAMA_MODEL

class TestCaseManager:
    def __init__(self, results_file: str = "test_results.json"):
        self.results_file = results_file
        self.results = self.load_results()
        
    def load_results(self) -> Dict:
        """Load existing test results from file"""
        if os.path.exists(self.results_file):
            try:
                with open(self.results_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load existing results: {e}")
        return {
            "last_updated": "",
            "model": "",
            "test_cases": {},
            "summary": {
                "total_cases": 0,
                "accuracy_passed": 0,
                "consistency_passed": 0,
                "both_passed": 0,
                "needs_work": 0
            }
        }
    
    def save_results(self):
        """Save test results to file"""
        self.results["last_updated"] = datetime.now().isoformat()
        self.results["model"] = OLLAMA_MODEL
        with open(self.results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
    
    def get_test_case_status(self, test_name: str) -> Dict:
        """Get the status of a specific test case"""
        return self.results["test_cases"].get(test_name, {
            "accuracy_passed": False,
            "consistency_passed": False,
            "last_accuracy_test": None,
            "last_consistency_test": None,
            "accuracy_score": 0.0,
            "consistency_rate": 0.0,
            "needs_work": True
        })
    
    def update_test_case(self, test_name: str, accuracy_result: Dict, consistency_result: Dict):
        """Update a test case with new results"""
        accuracy_passed = accuracy_result.get("passed", False)
        accuracy_score = accuracy_result.get("score", 0.0)
        
        consistency_passed = consistency_result.get("consistent", False)
        consistency_rate = consistency_result.get("consistency_rate", 0.0)
        
        self.results["test_cases"][test_name] = {
            "accuracy_passed": accuracy_passed,
            "consistency_passed": consistency_passed,
            "last_accuracy_test": datetime.now().isoformat(),
            "last_consistency_test": datetime.now().isoformat(),
            "accuracy_score": accuracy_score,
            "consistency_rate": consistency_rate,
            "needs_work": not (accuracy_passed and consistency_passed)
        }
    
    def get_cases_needing_work(self) -> List[str]:
        """Get list of test cases that need improvement"""
        return [
            name for name, status in self.results["test_cases"].items()
            if status.get("needs_work", True)
        ]
    
    def get_passed_cases(self) -> List[str]:
        """Get list of test cases that pass both accuracy and consistency"""
        return [
            name for name, status in self.results["test_cases"].items()
            if status.get("accuracy_passed", False) and status.get("consistency_passed", False)
        ]
    
    def update_summary(self):
        """Update the summary statistics"""
        total_cases = len(self.results["test_cases"])
        accuracy_passed = sum(1 for status in self.results["test_cases"].values() 
                            if status.get("accuracy_passed", False))
        consistency_passed = sum(1 for status in self.results["test_cases"].values() 
                               if status.get("consistency_passed", False))
        both_passed = sum(1 for status in self.results["test_cases"].values() 
                         if status.get("accuracy_passed", False) and status.get("consistency_passed", False))
        needs_work = sum(1 for status in self.results["test_cases"].values() 
                        if status.get("needs_work", True))
        
        self.results["summary"] = {
            "total_cases": total_cases,
            "accuracy_passed": accuracy_passed,
            "consistency_passed": consistency_passed,
            "both_passed": both_passed,
            "needs_work": needs_work
        }
    
    def run_focused_accuracy_test(self, test_names: List[str]) -> Dict:
        """Run accuracy test only on specified test cases"""
        if not test_names:
            return {"passed": 0, "total": 0, "results": []}
        
        # Filter test cases
        filtered_cases = [case for case in TEST_CASES if case["name"] in test_names]
        
        print(f"🧪 Running focused accuracy test on {len(filtered_cases)} cases...")
        results, overall_score = run_comprehensive_tests(filtered_cases)
        
        return {
            "passed": sum(1 for r in results if r["passed"]),
            "total": len(results),
            "overall_score": overall_score,
            "results": results
        }
    
    def run_focused_consistency_test(self, test_names: List[str]) -> Dict:
        """Run consistency test only on specified test cases"""
        if not test_names:
            return {"consistent": 0, "total": 0, "results": []}
        
        # Filter test cases
        filtered_cases = [case for case in TEST_CASES if case["name"] in test_names]
        
        print(f"🔄 Running focused consistency test on {len(filtered_cases)} cases...")
        
        # Load CDT codes
        with open('cdt_codes.json', 'r') as f:
            cdt_codes = json.load(f)
        
        # Run consistency test
        consistency_results = parallel_test_consistency(filtered_cases, cdt_codes)
        
        # Analyze results - convert to the format expected by the manager
        test_case_results = {}
        for test_case in filtered_cases:
            test_name = test_case["name"]
            test_input = test_case["input"]
            
            # Find results for this test case
            runs = []
            for result in consistency_results:
                if isinstance(result[0], dict) and result[0].get("input") == test_input:
                    runs.append(result[1])  # Extract codes from result
            
            test_case_results[test_name] = runs
        
        # Count consistent cases
        consistent_cases = 0
        for test_name, runs in test_case_results.items():
            if len(set(tuple(sorted(run)) for run in runs)) == 1:
                consistent_cases += 1
        
        return {
            "consistent": consistent_cases,
            "total": len(filtered_cases),
            "consistency_rate": consistent_cases / len(filtered_cases) if filtered_cases else 0,
            "results": test_case_results
        }
    
    def run_full_validation(self, force_retest: bool = False) -> Dict:
        """Run both accuracy and consistency tests on all cases"""
        print("🚀 Starting full validation of all test cases...")
        
        # Load CDT codes
        with open('cdt_codes.json', 'r') as f:
            cdt_codes = json.load(f)
        
        # Determine which cases to test
        if force_retest:
            cases_to_test = TEST_CASES
            print("🔄 Force retest enabled - testing all cases")
        else:
            cases_needing_work = self.get_cases_needing_work()
            cases_to_test = [case for case in TEST_CASES if case["name"] in cases_needing_work]
            print(f"🎯 Testing {len(cases_to_test)} cases that need work (skipping {len(TEST_CASES) - len(cases_to_test)} passed cases)")
        
        if not cases_to_test:
            print("✅ All test cases are already passing! Use --force-retest to run all cases.")
            return {"status": "all_passed"}
        
        # Run accuracy test
        print("\n📊 Running accuracy tests...")
        accuracy_results, overall_accuracy = run_comprehensive_tests(cases_to_test)
        
        # Run consistency test
        print("\n🔄 Running consistency tests...")
        consistency_results = parallel_test_consistency(cases_to_test, cdt_codes)
        
        # Update results
        for i, test_case in enumerate(cases_to_test):
            test_name = test_case["name"]
            accuracy_result = accuracy_results[i]
            
            # Check consistency - need to find results for this test case
            test_input = test_case["input"]
            runs = []
            for result in consistency_results:
                if isinstance(result[0], dict) and result[0].get("input") == test_input:
                    runs.append(result[1])  # Extract codes from result
            
            consistent = len(set(tuple(sorted(run)) for run in runs)) == 1 if runs else False
            consistency_rate = 1.0 if consistent else 0.0
            
            consistency_result = {
                "consistent": consistent,
                "consistency_rate": consistency_rate,
                "runs": runs
            }
            
            self.update_test_case(test_name, accuracy_result, consistency_result)
        
        self.update_summary()
        self.save_results()
        
        return {
            "accuracy_results": accuracy_results,
            "consistency_results": consistency_results,
            "overall_accuracy": overall_accuracy,
            "summary": self.results["summary"]
        }
    
    def print_status_report(self):
        """Print a detailed status report"""
        print("\n📊 TEST CASE STATUS REPORT")
        print("=" * 60)
        print(f"Model: {self.results.get('model', 'Unknown')}")
        print(f"Last Updated: {self.results.get('last_updated', 'Never')}")
        print()
        
        # Summary
        summary = self.results["summary"]
        print("📈 SUMMARY:")
        print(f"  Total Cases: {summary['total_cases']}")
        print(f"  Accuracy Passed: {summary['accuracy_passed']} ({summary['accuracy_passed']/summary['total_cases']*100:.1f}%)" if summary['total_cases'] > 0 else "  Accuracy Passed: 0")
        print(f"  Consistency Passed: {summary['consistency_passed']} ({summary['consistency_passed']/summary['total_cases']*100:.1f}%)" if summary['total_cases'] > 0 else "  Consistency Passed: 0")
        print(f"  Both Passed: {summary['both_passed']} ({summary['both_passed']/summary['total_cases']*100:.1f}%)" if summary['total_cases'] > 0 else "  Both Passed: 0")
        print(f"  Needs Work: {summary['needs_work']} ({summary['needs_work']/summary['total_cases']*100:.1f}%)" if summary['total_cases'] > 0 else "  Needs Work: 0")
        print()
        
        # Detailed breakdown
        print("📋 DETAILED BREAKDOWN:")
        print("-" * 60)
        
        passed_cases = self.get_passed_cases()
        needs_work = self.get_cases_needing_work()
        
        if passed_cases:
            print("✅ PASSED (Accuracy + Consistency):")
            for case in sorted(passed_cases):
                status = self.get_test_case_status(case)
                print(f"  • {case} (Acc: {status['accuracy_score']:.1%}, Cons: {status['consistency_rate']:.1%})")
            print()
        
        if needs_work:
            print("🔧 NEEDS WORK:")
            for case in sorted(needs_work):
                status = self.get_test_case_status(case)
                issues = []
                if not status.get("accuracy_passed", False):
                    issues.append("accuracy")
                if not status.get("consistency_passed", False):
                    issues.append("consistency")
                print(f"  • {case} (Issues: {', '.join(issues)}, Acc: {status['accuracy_score']:.1%}, Cons: {status['consistency_rate']:.1%})")
    
    def reset_results(self):
        """Reset all test results"""
        self.results = {
            "last_updated": "",
            "model": "",
            "test_cases": {},
            "summary": {
                "total_cases": 0,
                "accuracy_passed": 0,
                "consistency_passed": 0,
                "both_passed": 0,
                "needs_work": 0
            }
        }
        self.save_results()
        print("🔄 All test results have been reset.")

def main():
    """Main function for command line usage"""
    import sys
    
    manager = TestCaseManager()
    
    if len(sys.argv) < 2:
        print("Usage: python test_case_manager.py [command]")
        print("Commands:")
        print("  status     - Show current status report")
        print("  run        - Run tests on cases that need work")
        print("  run-all    - Run tests on all cases (force retest)")
        print("  reset      - Reset all test results")
        print("  passed     - Show only passed cases")
        print("  needs-work - Show only cases that need work")
        return
    
    command = sys.argv[1]
    
    if command == "status":
        manager.print_status_report()
    elif command == "run":
        results = manager.run_full_validation(force_retest=False)
        manager.print_status_report()
    elif command == "run-all":
        results = manager.run_full_validation(force_retest=True)
        manager.print_status_report()
    elif command == "reset":
        manager.reset_results()
    elif command == "passed":
        passed = manager.get_passed_cases()
        print(f"✅ Passed cases ({len(passed)}):")
        for case in sorted(passed):
            print(f"  • {case}")
    elif command == "needs-work":
        needs_work = manager.get_cases_needing_work()
        print(f"🔧 Cases needing work ({len(needs_work)}):")
        for case in sorted(needs_work):
            print(f"  • {case}")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Comprehensive test cases for CDT Code Mapper with expected results.
Tests the model's accuracy on specific dental procedures.
"""

import requests
import json
import time
import sys
from config import OLLAMA_URL, OLLAMA_MODEL
from prompts import get_prompt_for_model
from test_reference import TEST_CASES, get_test_cases_by_category, get_all_categories

def load_cdt_codes():
    """Load CDT codes from JSON file"""
    try:
        with open('cdt_codes.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading CDT codes: {e}")
        return []

def send_test_to_ollama(test_input):
    """Send test input to Ollama and return response"""
    cdt_codes = load_cdt_codes()
    system_message = get_prompt_for_model(OLLAMA_MODEL, cdt_codes)
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": f"Please analyze this dental procedure summary and provide the appropriate CDT codes: {test_input}"
            }
        ],
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def extract_codes_from_response(response_text):
    """Extract CDT codes from the model's response"""
    if not response_text:
        return []
    
    # Look for D-codes in the response
    import re
    d_codes = re.findall(r'D\d{4}', response_text)
    return list(set(d_codes))  # Remove duplicates

def evaluate_test_case(test_case, model_response):
    """Evaluate a single test case against expected results"""
    if "error" in model_response:
        return {
            "passed": False,
            "error": model_response["error"],
            "extracted_codes": [],
            "expected_codes": test_case["expected_codes"],
            "score": 0
        }
    
    response_text = model_response.get("message", {}).get("content", "")
    extracted_codes = extract_codes_from_response(response_text)
    
    # Calculate score based on expected codes found
    found_codes = [code for code in test_case["expected_codes"] if code in extracted_codes]
    score = len(found_codes) / len(test_case["expected_codes"]) if test_case["expected_codes"] else 0
    
    return {
        "passed": score >= 0.5,  # Pass if at least 50% of expected codes found
        "extracted_codes": extracted_codes,
        "expected_codes": test_case["expected_codes"],
        "found_codes": found_codes,
        "missing_codes": [code for code in test_case["expected_codes"] if code not in extracted_codes],
        "score": score,
        "response_text": response_text[:200] + "..." if len(response_text) > 200 else response_text
    }

def run_comprehensive_tests(test_cases=None, category=None):
    """Run test cases and provide detailed results"""
    if test_cases is None:
        test_cases = TEST_CASES
    
    if category:
        print(f"🧪 Running CDT Code Mapper Tests - Category: {category.upper()}")
    else:
        print("🧪 Running Comprehensive CDT Code Mapper Tests")
    
    print("=" * 60)
    print(f"Model: {OLLAMA_MODEL}")
    print(f"Total test cases: {len(test_cases)}")
    print()
    
    results = []
    total_score = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📋 Test Case {i}: {test_case['name']}")
        print(f"   Input: {test_case['input']}")
        print(f"   Expected: {', '.join(test_case['expected_codes'])}")
        
        # Send to model
        print("   🔄 Sending to model...")
        model_response = send_test_to_ollama(test_case["input"])
        
        # Evaluate results
        result = evaluate_test_case(test_case, model_response)
        results.append(result)
        
        # Display results
        if result["passed"]:
            print(f"   ✅ PASSED (Score: {result['score']:.1%})")
        else:
            print(f"   ❌ FAILED (Score: {result['score']:.1%})")
        
        print(f"   Found codes: {', '.join(result['extracted_codes']) if result['extracted_codes'] else 'None'}")
        
        if result["found_codes"]:
            print(f"   ✅ Correct: {', '.join(result['found_codes'])}")
        
        if result["missing_codes"]:
            print(f"   ❌ Missing: {', '.join(result['missing_codes'])}")
        
        if "error" in result:
            print(f"   🚨 Error: {result['error']}")
        
        print(f"   Response preview: {result['response_text']}")
        print("-" * 60)
        
        total_score += result["score"]
        
        # Small delay between requests
        time.sleep(1)
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 60)
    passed_tests = sum(1 for r in results if r["passed"])
    overall_score = total_score / len(test_cases)
    
    print(f"✅ Passed: {passed_tests}/{len(test_cases)} tests")
    print(f"📈 Overall accuracy: {overall_score:.1%}")
    print(f"🎯 Average score per test: {overall_score:.1%}")
    
    # Detailed breakdown
    print("\n📋 DETAILED BREAKDOWN")
    print("-" * 60)
    for i, (test_case, result) in enumerate(zip(test_cases, results), 1):
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"{i:2d}. {status} {test_case['name']} ({result['score']:.1%})")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("-" * 60)
    if overall_score >= 0.8:
        print("🎉 Excellent performance! The model is working very well.")
    elif overall_score >= 0.6:
        print("👍 Good performance. Consider fine-tuning prompts for better accuracy.")
    elif overall_score >= 0.4:
        print("⚠️ Moderate performance. Significant improvements needed.")
    else:
        print("🚨 Poor performance. Significant improvements needed.")
    
    return results, overall_score

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) > 1:
        category = sys.argv[1].lower()
        if category == "list":
            print("Available test categories:")
            for cat in get_all_categories():
                test_cases = get_test_cases_by_category(cat)
                print(f"  {cat}: {len(test_cases)} test cases")
            return
        elif category in get_all_categories():
            test_cases = get_test_cases_by_category(category)
            run_comprehensive_tests(test_cases, category)
        else:
            print(f"Unknown category: {category}")
            print("Available categories:", ", ".join(get_all_categories()))
            print("Use 'list' to see all categories with test case counts.")
    else:
        # Run all tests
        run_comprehensive_tests()

if __name__ == "__main__":
    main() 
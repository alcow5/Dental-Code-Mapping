#!/usr/bin/env python3
"""
Comprehensive test cases for CDT Code Mapper with expected results.
Tests the model's accuracy on specific dental procedures.
"""

import requests
import json
import time
from config import OLLAMA_URL, OLLAMA_MODEL, SYSTEM_MESSAGE

# Test cases with expected results
TEST_CASES = [
    {
        "name": "Standard Adult Checkup + Cleaning",
        "input": "Patient came in for a routine dental checkup. We did a full oral exam and a cleaning. No radiographs needed.",
        "expected_codes": ["D0120", "D1110"],
        "expected_descriptions": [
            "Periodic oral evaluation - established patient",
            "Prophylaxis - adult"
        ]
    },
    {
        "name": "Pediatric Sealants + Fluoride",
        "input": "Applied fluoride varnish and sealants on molars for an 8-year-old patient during a preventive visit.",
        "expected_codes": ["D1206", "D1351"],
        "expected_descriptions": [
            "Topical application of fluoride varnish",
            "Sealant - per tooth"
        ]
    },
    {
        "name": "Bitewing X-rays and Composite Filling",
        "input": "Patient had decay on the lower left molar. We took two bitewing X-rays and placed a composite restoration on one surface.",
        "expected_codes": ["D0272", "D2391"],
        "expected_descriptions": [
            "Bitewings – two radiographic images",
            "Resin-based composite – one surface, posterior"
        ]
    },
    {
        "name": "Root Canal – Premolar",
        "input": "Completed root canal on upper premolar due to chronic pain. Patient was advised to return for crown placement.",
        "expected_codes": ["D3320"],
        "expected_descriptions": [
            "Endodontic therapy, bicuspid tooth (excluding final restoration)"
        ]
    },
    {
        "name": "Tooth Extraction",
        "input": "Extracted an erupted tooth with forceps under local anesthesia. Simple procedure.",
        "expected_codes": ["D7140"],
        "expected_descriptions": [
            "Extraction, erupted tooth or exposed root (elevation and/or forceps removal)"
        ]
    },
    {
        "name": "Scaling and Root Planing (SRP)",
        "input": "Patient diagnosed with periodontal disease. SRP performed on lower left quadrant affecting four teeth.",
        "expected_codes": ["D4341"],
        "expected_descriptions": [
            "Periodontal scaling and root planing – four or more teeth per quadrant"
        ]
    },
    {
        "name": "Full Denture Delivery",
        "input": "Delivered a complete upper denture to the patient after impressions were made last visit.",
        "expected_codes": ["D5110"],
        "expected_descriptions": [
            "Complete denture – maxillary"
        ]
    },
    {
        "name": "Limited Emergency Exam",
        "input": "Patient presented with severe toothache. Limited exam focused on the area of pain.",
        "expected_codes": ["D0140"],
        "expected_descriptions": [
            "Limited oral evaluation – problem focused"
        ]
    },
    {
        "name": "Panoramic Radiograph for Assessment",
        "input": "Took a panoramic X-ray to assess jaw and sinus structure prior to implant evaluation.",
        "expected_codes": ["D0330"],
        "expected_descriptions": [
            "Panoramic radiographic image"
        ]
    },
    {
        "name": "Fluoride Treatment + Hygiene Instruction",
        "input": "Applied fluoride varnish after cleaning. Reviewed brushing technique and flossing with the patient.",
        "expected_codes": ["D1206", "D1330"],
        "expected_descriptions": [
            "Topical application of fluoride varnish",
            "Oral hygiene instructions"
        ]
    },
    {
        "name": "Anterior Composite – Two Surfaces",
        "input": "Placed composite restoration on two surfaces of tooth #8. Patient chipped the incisal edge and had decay interproximally.",
        "expected_codes": ["D2331"],
        "expected_descriptions": [
            "Resin-based composite – two surfaces, anterior"
        ]
    },
    {
        "name": "Resin Crown Placement",
        "input": "Delivered an indirect resin crown on lower right second premolar after prior root canal.",
        "expected_codes": ["D2710"],
        "expected_descriptions": [
            "Crown – resin (indirect)"
        ]
    },
    {
        "name": "Incision and Drainage",
        "input": "Patient presented with facial swelling and pain. Performed extraoral incision and drainage of abscess.",
        "expected_codes": ["D7520"],
        "expected_descriptions": [
            "Incision and drainage of abscess – extraoral soft tissue"
        ]
    },
    {
        "name": "Full Mouth Debridement",
        "input": "Heavy calculus present. Full mouth debridement performed to allow better diagnostic evaluation on next visit.",
        "expected_codes": ["D4355"],
        "expected_descriptions": [
            "Full mouth debridement to enable a comprehensive periodontal evaluation and diagnosis on a subsequent visit"
        ]
    },
    {
        "name": "Stainless Steel Crown on Child",
        "input": "Placed a preformed stainless steel crown on primary molar with deep decay.",
        "expected_codes": ["D2930"],
        "expected_descriptions": [
            "Prefabricated stainless steel crown – primary tooth"
        ]
    },
    {
        "name": "Biteguard Delivery",
        "input": "Delivered a hard full-arch nightguard for bruxism. Patient has history of grinding and TMJ discomfort.",
        "expected_codes": ["D9944"],
        "expected_descriptions": [
            "Occlusal guard – hard appliance, full arch"
        ]
    },
    {
        "name": "Post and Core with Crown",
        "input": "Placed a cast post and core on tooth #19, followed by porcelain fused to metal crown.",
        "expected_codes": ["D2954", "D2750"],
        "expected_descriptions": [
            "Prefabricated post and core in addition to crown",
            "Crown – porcelain fused to high noble metal"
        ]
    },
    {
        "name": "Emergency Palliative Treatment",
        "input": "Provided palliative care for severe tooth pain, including temporary dressing and occlusal adjustment.",
        "expected_codes": ["D9110"],
        "expected_descriptions": [
            "Palliative treatment of dental pain – per visit"
        ]
    }
]

def send_test_to_ollama(test_input):
    """Send test input to Ollama and return response"""
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_MESSAGE
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

def run_comprehensive_tests():
    """Run all test cases and provide detailed results"""
    print("🧪 Running Comprehensive CDT Code Mapper Tests")
    print("=" * 60)
    print(f"Model: {OLLAMA_MODEL}")
    print(f"Total test cases: {len(TEST_CASES)}")
    print()
    
    results = []
    total_score = 0
    
    for i, test_case in enumerate(TEST_CASES, 1):
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
    overall_score = total_score / len(TEST_CASES)
    
    print(f"✅ Passed: {passed_tests}/{len(TEST_CASES)} tests")
    print(f"📈 Overall accuracy: {overall_score:.1%}")
    print(f"🎯 Average score per test: {overall_score:.1%}")
    
    # Detailed breakdown
    print("\n📋 DETAILED BREAKDOWN")
    print("-" * 60)
    for i, (test_case, result) in enumerate(zip(TEST_CASES, results), 1):
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
        print("⚠️  Moderate performance. Review system prompt and test cases.")
    else:
        print("🚨 Poor performance. Significant improvements needed.")
    
    return results

if __name__ == "__main__":
    run_comprehensive_tests() 
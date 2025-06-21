#!/usr/bin/env python3
"""
Demo mode for CDT Code Mapper - simulates AI responses for testing
"""

import json
import random
from datetime import datetime

def load_cdt_codes():
    """Load CDT codes from JSON file"""
    try:
        with open('cdt_codes.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading CDT codes: {e}")
        return []

def get_demo_response(procedure_summary, cdt_codes):
    """Generate a demo response based on the procedure summary"""
    
    # Simple keyword matching for demo purposes
    procedure_lower = procedure_summary.lower()
    
    demo_responses = {
        "cleaning": {
            "cdt_codes": [
                {
                    "code": "D1120",
                    "description": "Prophylaxis – child",
                    "confidence": "high"
                }
            ],
            "explanation": "This appears to be a routine dental cleaning procedure."
        },
        "exam": {
            "cdt_codes": [
                {
                    "code": "D0120",
                    "description": "Periodic oral evaluation - established patient",
                    "confidence": "high"
                }
            ],
            "explanation": "This is a standard oral evaluation for an established patient."
        },
        "extraction": {
            "cdt_codes": [
                {
                    "code": "D7210",
                    "description": "Extraction, erupted tooth or exposed root (elevation and/or forceps removal)",
                    "confidence": "high"
                }
            ],
            "explanation": "This is a simple extraction of an erupted tooth."
        },
        "root canal": {
            "cdt_codes": [
                {
                    "code": "D3330",
                    "description": "Endodontic therapy, molar tooth (excluding final restoration)",
                    "confidence": "high"
                }
            ],
            "explanation": "This is a root canal treatment on a molar tooth."
        },
        "crown": {
            "cdt_codes": [
                {
                    "code": "D2740",
                    "description": "Crown – porcelain/ceramic",
                    "confidence": "medium"
                }
            ],
            "explanation": "This appears to be a crown procedure, likely porcelain/ceramic based on common usage."
        },
        "filling": {
            "cdt_codes": [
                {
                    "code": "D2391",
                    "description": "Resin-based composite – one surface, posterior",
                    "confidence": "medium"
                }
            ],
            "explanation": "This is a composite filling, assumed to be one surface on a posterior tooth."
        },
        "x-ray": {
            "cdt_codes": [
                {
                    "code": "D0210",
                    "description": "Intraoral – complete series of radiographic images",
                    "confidence": "high"
                }
            ],
            "explanation": "This is a complete series of intraoral x-rays."
        }
    }
    
    # Find matching keywords
    matched_response = None
    for keyword, response in demo_responses.items():
        if keyword in procedure_lower:
            matched_response = response
            break
    
    # If no specific match, return a generic evaluation
    if not matched_response:
        matched_response = {
            "cdt_codes": [
                {
                    "code": "D0150",
                    "description": "Comprehensive oral evaluation - new or established patient",
                    "confidence": "low"
                }
            ],
            "explanation": "This appears to be a dental evaluation, but the specific procedure type is unclear. Please provide more details for better code matching."
        }
    
    # Add timestamp for demo purposes
    matched_response["demo_timestamp"] = datetime.now().isoformat()
    matched_response["demo_mode"] = True
    
    return matched_response

def main():
    """Demo mode main function"""
    print("🎭 CDT Code Mapper - Demo Mode")
    print("=" * 50)
    
    cdt_codes = load_cdt_codes()
    if not cdt_codes:
        print("❌ Could not load CDT codes")
        return
    
    print(f"✅ Loaded {len(cdt_codes)} CDT codes")
    print("\n📝 Demo Examples:")
    print("1. Patient came in for routine cleaning and exam")
    print("2. Extracted upper right molar due to severe decay")
    print("3. Root canal treatment on tooth #14")
    print("4. Crown preparation and temporary crown placement")
    print("5. Two-surface composite filling on posterior tooth")
    
    while True:
        print("\n" + "-" * 50)
        procedure = input("\nEnter a dental procedure summary (or 'quit' to exit): ")
        
        if procedure.lower() in ['quit', 'exit', 'q']:
            break
        
        if not procedure.strip():
            print("⚠️ Please enter a procedure summary")
            continue
        
        print("\n🔍 Analyzing procedure summary...")
        
        # Simulate processing time
        import time
        time.sleep(1)
        
        response = get_demo_response(procedure, cdt_codes)
        
        print("\n📊 Results:")
        print(f"✅ Successfully parsed response!")
        
        print("\n🦷 CDT Codes Found:")
        for i, code_info in enumerate(response['cdt_codes'], 1):
            confidence_emoji = {
                "high": "🟢",
                "medium": "🟡", 
                "low": "🔴"
            }.get(code_info.get('confidence', 'unknown'), "⚪")
            
            print(f"{confidence_emoji} Code {i}: {code_info.get('code', 'N/A')}")
            print(f"   Description: {code_info.get('description', 'N/A')}")
            print(f"   Confidence: {code_info.get('confidence', 'N/A')}")
        
        print(f"\n💡 Explanation:")
        print(f"   {response['explanation']}")
        
        if response.get('demo_mode'):
            print(f"\n🎭 Demo Mode - Timestamp: {response.get('demo_timestamp', 'N/A')}")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Test script to verify CDT codes database
"""

import json
import sys

def test_cdt_codes():
    """Test if CDT codes can be loaded"""
    try:
        with open('cdt_codes.json', 'r') as f:
            cdt_codes = json.load(f)
        
        print(f"✅ CDT codes loaded successfully: {len(cdt_codes)} codes")
        
        # Show some sample codes
        print("\n📋 Sample CDT codes:")
        for i, code in enumerate(cdt_codes[:5]):
            print(f"  {code['code']}: {code['description']}")
        
        if len(cdt_codes) > 5:
            print(f"  ... and {len(cdt_codes) - 5} more codes")
        
        # Check categories
        categories = {
            "Oral Evaluations": len([c for c in cdt_codes if c['code'].startswith('D01')]),
            "Radiographic": len([c for c in cdt_codes if c['code'].startswith('D02') or c['code'].startswith('D03') or c['code'].startswith('D07')]),
            "Preventive": len([c for c in cdt_codes if c['code'].startswith('D11') or c['code'].startswith('D13')]),
            "Restorations": len([c for c in cdt_codes if c['code'].startswith('D21') or c['code'].startswith('D23') or c['code'].startswith('D25') or c['code'].startswith('D26')]),
            "Crowns": len([c for c in cdt_codes if c['code'].startswith('D27')]),
            "Endodontics": len([c for c in cdt_codes if c['code'].startswith('D31') or c['code'].startswith('D33')]),
            "Extractions": len([c for c in cdt_codes if c['code'].startswith('D71') or c['code'].startswith('D72')]),
            "Surgical": len([c for c in cdt_codes if c['code'].startswith('D74') or c['code'].startswith('D75')])
        }
        
        print("\n📊 Code categories:")
        for category, count in categories.items():
            if count > 0:
                print(f"  {category}: {count} codes")
        
        return True
        
    except FileNotFoundError:
        print("❌ CDT codes file not found: cdt_codes.json")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing CDT codes JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing CDT Codes Database...")
    print("=" * 50)
    
    success = test_cdt_codes()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 CDT codes database is ready!")
    else:
        print("❌ CDT codes database has issues.")
    
    sys.exit(0 if success else 1) 
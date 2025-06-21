import json
from test_reference import TEST_CASES

with open('cdt_codes.json', 'r') as f:
    cdt_codes = json.load(f)
    cdt_code_set = set(code['code'] for code in cdt_codes)

missing_codes = set()
for tc in TEST_CASES:
    for code in tc['expected_codes']:
        if code not in cdt_code_set:
            missing_codes.add(code)

if missing_codes:
    print('Missing codes in cdt_codes.json:')
    for code in sorted(missing_codes):
        print(' ', code)
else:
    print('All expected codes in test cases are present in cdt_codes.json!') 
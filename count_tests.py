from test_reference import TEST_CASES

print(f"Total test cases: {len(TEST_CASES)}")
print("\nTest cases with indices:")
for i, tc in enumerate(TEST_CASES):
    print(f"{i:2d}: {tc['name']}") 
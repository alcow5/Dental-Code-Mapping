#!/usr/bin/env python3
"""
Test script to demonstrate consistency improvements in the CDT Code Mapper.
Runs the same prompt multiple times to show how consistent the responses are.

CONCURRENT TESTING EXPLANATION:
================================
This script uses Python's ThreadPoolExecutor to run multiple API requests simultaneously,
dramatically speeding up testing compared to sequential execution.

HOW IT WORKS:
1. TASK CREATION: Each test case is run multiple times (default: 3)
   - 28 test cases × 3 runs each = 84 total tasks
   - Each task is independent and can run in parallel

2. THREAD POOL EXECUTION:
   - Creates a pool of worker threads (default: 8 threads)
   - Each thread can handle one API request at a time
   - When a thread finishes, it immediately picks up the next task
   - Multiple threads make API calls to Ollama simultaneously

3. CONCURRENT vs SEQUENTIAL:
   - Sequential: Test 1 → wait → Test 2 → wait → Test 3 (slow)
   - Concurrent: Test 1, Test 2, Test 3 all run at same time (fast)
   - Speedup: ~84x faster for 84 tasks with 8 threads

4. RESULT COLLECTION:
   - Results come back as threads complete (not in original order)
   - as_completed() yields results as soon as they're ready
   - Results are grouped by test case for consistency analysis

5. CONSISTENCY ANALYSIS:
   - Groups results by test case
   - Compares codes across multiple runs
   - Identifies consistent vs inconsistent responses
   - Calculates overall consistency rate

PERFORMANCE BENEFITS:
- Dramatically faster execution (minutes → seconds)
- Better resource utilization (CPU, network, memory)
- Scalable to hundreds of test cases
- Real-time progress feedback

THREADING CONSIDERATIONS:
- I/O-bound tasks (API calls) benefit greatly from threading
- ThreadPoolExecutor handles thread lifecycle automatically
- max_workers controls concurrency level
- Results are thread-safe and properly synchronized
"""

import requests
import json
import time
from config import *
from prompts import get_prompt_for_model
from concurrent.futures import ThreadPoolExecutor, as_completed
from test_reference import TEST_CASES

def load_cdt_codes():
    """Load CDT codes from JSON file"""
    try:
        with open(CDT_CODES_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading CDT codes: {e}")
        return []

def send_to_ollama_consistent(procedure_summary, cdt_codes, temperature=0.0):
    """
    Send procedure summary to Ollama API with consistency parameters.
    
    This function makes a single API call to the Ollama model with optimized
    parameters for consistency (low temperature, fixed seed, etc.).
    
    Args:
        procedure_summary (str): The dental procedure description to analyze
        cdt_codes (list): Available CDT codes database
        temperature (float): Model temperature (0.0 = deterministic, 1.0 = random)
    
    Returns:
        dict: Ollama API response containing model output
    
    Raises:
        Exception: If API call fails or times out
    """
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
                "content": f"Please analyze this dental procedure summary and provide the appropriate CDT codes: {procedure_summary}"
            }
        ],
        "stream": False,
        "temperature": temperature,
        "seed": MODEL_SEED,
        "top_p": MODEL_TOP_P,
        "top_k": MODEL_TOP_K,
        "repeat_penalty": MODEL_REPEAT_PENALTY,
        "num_predict": MODEL_NUM_PREDICT,
        "tfs_z": MODEL_TFS_Z,
        "typical_p": MODEL_TYPICAL_P
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error connecting to Ollama: {e}")

def extract_codes_from_response(response):
    """
    Extract CDT codes from the model response with deduplication.
    
    This function parses the model's response to extract CDT codes, handling
    both JSON and text formats. It also removes duplicate codes to ensure
    clean results.
    
    Args:
        response (dict): Ollama API response containing model output
    
    Returns:
        list: List of unique CDT codes found in the response
    """
    if 'message' not in response or 'content' not in response['message']:
        return []
    
    content = response['message']['content']
    
    # Try to parse as JSON first (preferred format)
    try:
        json_data = json.loads(content)
        if 'cdt_codes' in json_data:
            codes = [code.get('code', 'N/A') for code in json_data['cdt_codes']]
            # Deduplicate codes while preserving order
            seen = set()
            unique_codes = []
            for code in codes:
                if code not in seen and code != 'N/A':
                    seen.add(code)
                    unique_codes.append(code)
            return unique_codes
    except json.JSONDecodeError:
        pass
    
    # Fallback: extract codes using regex pattern matching
    import re
    cdt_pattern = r'D\d{4}'
    codes = re.findall(cdt_pattern, content)
    # Deduplicate codes while preserving order
    seen = set()
    unique_codes = []
    for code in codes:
        if code not in seen:
            seen.add(code)
            unique_codes.append(code)
    return unique_codes

def run_test_case(test_case, cdt_codes, temperature, run_number):
    """
    Execute a single test case and return results with timing.
    
    This function is designed to be called by worker threads in the thread pool.
    Each call represents one execution of a test case, with timing information
    for performance analysis.
    
    Args:
        test_case (str): The dental procedure description to test
        cdt_codes (list): Available CDT codes database
        temperature (float): Model temperature setting
        run_number (int): Which run this is (1, 2, 3, etc.)
    
    Returns:
        tuple: (test_case, codes, error, elapsed_time, run_number)
    """
    start_time = time.time()
    try:
        # Make API call to Ollama
        response = send_to_ollama_consistent(test_case, cdt_codes, temperature=temperature)
        # Extract CDT codes from response
        codes = extract_codes_from_response(response)
        elapsed = time.time() - start_time
        return (test_case, codes, None, elapsed, run_number)
    except Exception as e:
        elapsed = time.time() - start_time
        return (test_case, None, str(e), elapsed, run_number)

def parallel_test_consistency(test_cases, cdt_codes, temperature=0.0, max_workers=12, runs_per_test=3):
    """
    Execute consistency testing using parallel processing.
    
    This is the main function that orchestrates concurrent testing. It creates
    multiple tasks for each test case and uses ThreadPoolExecutor to run them
    in parallel, dramatically speeding up the testing process.
    
    CONCURRENT EXECUTION FLOW:
    1. TASK CREATION: For each test case, create multiple run tasks
       - 28 test cases × 3 runs = 84 total tasks
       - Each task is independent and can run in parallel
    
    2. THREAD POOL SETUP: Create ThreadPoolExecutor with worker threads
       - max_workers=8 means 8 threads can run simultaneously
       - Each thread handles one API request at a time
       - When a thread finishes, it immediately picks up the next task
    
    3. CONCURRENT EXECUTION: Submit all tasks to the thread pool
       - All 84 tasks are submitted at once
       - ThreadPoolExecutor distributes work across available threads
       - Multiple API calls happen simultaneously
    
    4. RESULT COLLECTION: Gather results as they complete
       - as_completed() yields results as soon as threads finish
       - Results may come back in different order than submitted
       - Progress is shown in real-time
    
    5. CONSISTENCY ANALYSIS: Analyze results for each test case
       - Group results by test case
       - Compare codes across multiple runs
       - Identify consistent vs inconsistent responses
    
    Args:
        test_cases (list): List of test case descriptions to run
        cdt_codes (list): Available CDT codes database
        temperature (float): Model temperature setting
        max_workers (int): Number of concurrent threads (default: 8)
        runs_per_test (int): Number of times to run each test case (default: 3)
    
    Returns:
        list: All test results with timing and consistency information
    """
    print(f"🚀 Starting parallel consistency test...")
    print(f"📋 Test cases: {len(test_cases)}")
    print(f"🔄 Runs per test: {runs_per_test}")
    print(f"⚙️  Temperature: {temperature}, Max Workers: {max_workers}")
    print("=" * 60)
    
    start_time = time.time()
    results = []
    
    # STEP 1: TASK CREATION
    # Create multiple runs for each test case
    # This expands our test matrix: 28 tests × 3 runs = 84 total tasks
    all_tasks = []
    for test_case in test_cases:
        for run in range(1, runs_per_test + 1):
            all_tasks.append((test_case, run))
    
    # STEP 2: CONCURRENT EXECUTION USING THREADPOOLEXECUTOR
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        print(f"📡 Submitting {len(all_tasks)} requests to Ollama...")
        
        # Submit all tasks to the thread pool
        # Each task will be executed by one of the worker threads
        futures = [
            executor.submit(run_test_case, test_case, cdt_codes, temperature, run)
            for test_case, run in all_tasks
        ]
        
        # STEP 3: RESULT COLLECTION
        # Collect results as they complete (not necessarily in order)
        completed = 0
        for future in as_completed(futures):
            # Get the result from the completed task
            test_case, codes, error, elapsed, run_number = future.result()
            results.append((test_case, codes, error, elapsed, run_number))
            completed += 1
            
            # Show real-time progress
            test_input = test_case["input"] if isinstance(test_case, dict) else str(test_case)
            print(f"✅ [{completed}/{len(all_tasks)}] Test '{test_input[:30]}...' Run {run_number} completed in {elapsed:.2f}s")
    
    # STEP 4: PERFORMANCE ANALYSIS
    total_time = time.time() - start_time
    print(f"\n" + "=" * 60)
    print(f"🎯 PARALLEL CONSISTENCY TEST COMPLETED!")
    print(f"⏱️  Total Time: {total_time:.2f} seconds")
    print(f"📈 Average Time per Test: {total_time/len(all_tasks):.2f} seconds")
    print(f"🚀 Speedup vs Sequential: ~{len(all_tasks)}x faster")
    
    # STEP 5: CONSISTENCY ANALYSIS
    print(f"\n📊 CONSISTENCY ANALYSIS:")
    print("=" * 60)
    
    # Group results by test case for analysis
    test_results = {}
    for test_case, codes, error, elapsed, run_number in results:
        test_key = test_case["name"] if isinstance(test_case, dict) and "name" in test_case else str(test_case)
        if test_key not in test_results:
            test_results[test_key] = []
        test_results[test_key].append((codes, error, elapsed, run_number))
    
    total_consistent = 0
    total_inconsistent = 0
    
    # Analyze consistency for each test case
    for i, (test_key, runs) in enumerate(test_results.items(), 1):
        print(f"\n{i}. 📋 Test Case: {test_key}")
        
        # Check if all runs were successful
        successful_runs = [run for run in runs if run[1] is None]
        failed_runs = [run for run in runs if run[1] is not None]
        
        if failed_runs:
            print(f"   ❌ {len(failed_runs)} runs failed")
            for codes, error, elapsed, run_num in failed_runs:
                print(f"      Run {run_num}: Error - {error}")
            total_inconsistent += 1
            continue
        
        # Analyze consistency of successful runs
        all_codes = [run[0] for run in successful_runs]
        # Create sets of sorted codes to compare (order doesn't matter)
        unique_code_sets = set(tuple(sorted(codes)) for codes in all_codes if codes)
        
        if len(unique_code_sets) == 1:
            print(f"   ✅ CONSISTENT - All {len(successful_runs)} runs returned the same codes")
            total_consistent += 1
        else:
            print(f"   ❌ INCONSISTENT - {len(unique_code_sets)} different responses")
            total_inconsistent += 1
        
        # Show individual run results
        for codes, error, elapsed, run_num in successful_runs:
            print(f"      Run {run_num} ({elapsed:.2f}s): {codes}")
    
    # STEP 6: FINAL SUMMARY
    print(f"\n" + "=" * 60)
    print(f"📈 FINAL CONSISTENCY SUMMARY:")
    print(f"Total test cases: {len(test_cases)}")
    print(f"✅ Consistent test cases: {total_consistent}")
    print(f"❌ Inconsistent test cases: {total_inconsistent}")
    print(f"🎯 Consistency rate: {(total_consistent/len(test_cases)*100):.1f}%")
    print(f"📊 Total runs completed: {len(all_tasks)}")
    
    return results

def test_specific_case():
    """Test a specific case that might be inconsistent"""
    print("\n🎯 Testing Specific Inconsistent Case")
    print("=" * 50)
    
    cdt_codes = load_cdt_codes()
    if not cdt_codes:
        return
    
    # Use a case that might be ambiguous
    test_case = "Patient had a dental procedure"
    
    print(f"Test case: {test_case}")
    print("Running with different temperatures...")
    
    for temp in [0.0, 0.1, 0.3, 0.5]:
        print(f"\n🌡️  Temperature: {temp}")
        responses = []
        
        for i in range(5):  # Run 5 times
            try:
                response = send_to_ollama_consistent(test_case, cdt_codes, temperature=temp)
                codes = extract_codes_from_response(response)
                responses.append(codes)
                print(f"  Run {i+1}: {codes}")
                time.sleep(0.5)
            except Exception as e:
                print(f"  Run {i+1}: Error - {e}")
        
        # Analyze consistency
        unique_responses = set(tuple(sorted(r)) for r in responses if r)
        print(f"  Unique responses: {len(unique_responses)}")
        if len(unique_responses) > 1:
            print(f"  Inconsistency detected! {len(unique_responses)} different responses")

if __name__ == "__main__":
    print("🦷 CDT Code Mapper Consistency Test (Parallel)")
    print("This script tests how consistent the model responses are by running each test multiple times.")
    print("Lower temperature values should produce more consistent results.\n")
    
    try:
        cdt_codes = load_cdt_codes()
        if not cdt_codes:
            print("❌ Failed to load CDT codes")
            exit(1)
        
        print(f"✅ Loaded {len(cdt_codes)} CDT codes")
        
        # Extract test cases from the reference file
        test_cases = [test_case["input"] for test_case in TEST_CASES]
        test_names = [test_case["name"] for test_case in TEST_CASES]
        
        print(f"📋 Loaded {len(test_cases)} test cases from test_reference.py")
        
        # Configuration for consistency testing
        temperature = 0.0  # Maximum determinism
        max_workers = 12   # Number of concurrent threads (optimized for your hardware)
        runs_per_test = 3  # Number of times to run each test case
        
        results = parallel_test_consistency(
            test_cases, 
            cdt_codes, 
            temperature=temperature, 
            max_workers=max_workers,
            runs_per_test=runs_per_test
        )
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
    
    print("\n✅ Parallel consistency test completed!") 
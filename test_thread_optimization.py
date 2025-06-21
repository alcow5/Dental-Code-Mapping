#!/usr/bin/env python3
"""
Thread optimization test for CDT Code Mapper.
Tests different thread counts to find optimal performance for your hardware.
"""

import time
import psutil
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import *
from prompts import get_prompt_for_model

def get_system_info():
    """Get system information for optimization"""
    cpu_count = psutil.cpu_count()
    cpu_count_logical = psutil.cpu_count(logical=True)
    memory = psutil.virtual_memory()
    
    print("🖥️  SYSTEM INFORMATION:")
    print(f"   Physical CPU cores: {cpu_count}")
    print(f"   Logical CPU threads: {cpu_count_logical}")
    print(f"   Total RAM: {memory.total / (1024**3):.1f} GB")
    print(f"   Available RAM: {memory.available / (1024**3):.1f} GB")
    print()

def send_test_request(cdt_codes):
    """Send a single test request to measure baseline performance"""
    system_message = get_prompt_for_model(OLLAMA_MODEL, cdt_codes)
    
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": "Patient came in for routine cleaning and examination."}
        ],
        "stream": False,
        "temperature": 0.0,
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
    except Exception as e:
        raise Exception(f"Test request failed: {e}")

def test_thread_count(thread_count, cdt_codes, num_requests=10):
    """Test performance with a specific thread count"""
    print(f"🧪 Testing {thread_count} threads with {num_requests} requests...")
    
    start_time = time.time()
    completed = 0
    errors = 0
    
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [
            executor.submit(send_test_request, cdt_codes)
            for _ in range(num_requests)
        ]
        
        for future in as_completed(futures):
            try:
                future.result()
                completed += 1
            except Exception as e:
                errors += 1
                print(f"   ❌ Error: {e}")
    
    total_time = time.time() - start_time
    avg_time = total_time / num_requests if num_requests > 0 else 0
    requests_per_second = completed / total_time if total_time > 0 else 0
    
    return {
        'thread_count': thread_count,
        'total_time': total_time,
        'avg_time': avg_time,
        'requests_per_second': requests_per_second,
        'completed': completed,
        'errors': errors,
        'success_rate': (completed / num_requests * 100) if num_requests > 0 else 0
    }

def load_cdt_codes():
    """Load CDT codes from JSON file"""
    try:
        with open(CDT_CODES_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading CDT codes: {e}")
        return []

def main():
    print("🚀 Thread Optimization Test for CDT Code Mapper")
    print("=" * 60)
    
    # Get system information
    get_system_info()
    
    # Load CDT codes
    cdt_codes = load_cdt_codes()
    if not cdt_codes:
        print("❌ Failed to load CDT codes")
        return
    
    print(f"✅ Loaded {len(cdt_codes)} CDT codes")
    
    # Test baseline performance
    print("\n🔍 Testing baseline performance...")
    try:
        start_time = time.time()
        send_test_request(cdt_codes)
        baseline_time = time.time() - start_time
        print(f"   Baseline request time: {baseline_time:.2f} seconds")
    except Exception as e:
        print(f"   ❌ Baseline test failed: {e}")
        return
    
    # Test different thread counts
    thread_counts = [1, 2, 4, 8, 12, 16, 20, 24, 32]
    results = []
    
    print(f"\n🧪 Testing thread counts: {thread_counts}")
    print("=" * 60)
    
    for thread_count in thread_counts:
        result = test_thread_count(thread_count, cdt_codes, num_requests=10)
        results.append(result)
        
        print(f"   ✅ {thread_count:2d} threads: {result['total_time']:.2f}s total, "
              f"{result['avg_time']:.2f}s avg, {result['requests_per_second']:.2f} req/s, "
              f"{result['success_rate']:.1f}% success")
        
        # Add delay between tests to avoid overwhelming the system
        time.sleep(2)
    
    # Find optimal thread count
    best_result = max(results, key=lambda x: x['requests_per_second'])
    
    print(f"\n" + "=" * 60)
    print(f"🎯 OPTIMAL THREAD COUNT ANALYSIS:")
    print(f"Best performance: {best_result['thread_count']} threads")
    print(f"Requests per second: {best_result['requests_per_second']:.2f}")
    print(f"Average response time: {best_result['avg_time']:.2f} seconds")
    print(f"Success rate: {best_result['success_rate']:.1f}%")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    cpu_count = psutil.cpu_count(logical=True)
    
    if best_result['thread_count'] <= cpu_count:
        print(f"   ✅ Optimal thread count ({best_result['thread_count']}) is within your CPU thread count ({cpu_count})")
    else:
        print(f"   ⚠️  Optimal thread count ({best_result['thread_count']}) exceeds your CPU thread count ({cpu_count})")
        print(f"   💡 This is normal for I/O-bound tasks like API calls")
    
    print(f"   🚀 Use {best_result['thread_count']} threads for maximum performance")
    print(f"   🛡️  Use {min(best_result['thread_count'], cpu_count)} threads for conservative approach")
    
    # Show all results
    print(f"\n📊 ALL RESULTS:")
    print("Threads | Total Time | Avg Time | Req/s | Success Rate")
    print("-" * 55)
    for result in results:
        print(f"{result['thread_count']:7d} | {result['total_time']:9.2f}s | {result['avg_time']:7.2f}s | "
              f"{result['requests_per_second']:5.2f} | {result['success_rate']:11.1f}%")

if __name__ == "__main__":
    main() 
import json
import random
from datetime import datetime, timedelta
from copy import deepcopy

def vary_metric(value, variation=0.1):
    """Add random variation of ±10% to a value."""
    delta = value * variation
    return value + random.uniform(-delta, delta)

def generate_variant(base_data, run_id, timestamp, commit):
    """Generate a variant of the base data with modified metrics."""
    variant = deepcopy(base_data)
    
    # Update fixed fields
    variant["run_id"] = run_id
    variant["timestamp"] = timestamp
    variant["commit"] = commit
    
    # Add variations to metrics
    variant["meanLatency"] = vary_metric(float(variant["meanLatency"]))
    variant["p99Latency"] = vary_metric(float(variant["p99Latency"]))
    variant["qps"] = vary_metric(float(variant["qps"]))
    variant["recall"] = vary_metric(float(variant["recall"]))
    
    return variant

# Read the base file
with open("results/results_1.json", "r") as f:
    base_results = json.load(f)

# Base timestamp and values
base_timestamp = datetime.strptime("2024-12-23T12:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
base_commit = "1234567890"
base_run_id = 28
number_of_files = 10

# Generate 10 new files
for i in range(number_of_files):
    new_results = []
    
    # Calculate new values
    new_timestamp = (base_timestamp + timedelta(minutes=(i+2)*10)).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_commit = str(int(base_commit) + (i+2)*10)
    new_run_id = f"main_{base_run_id + i + 2:03d}"
    
    # Generate variants for each entry
    for entry in base_results:
        new_entry = generate_variant(entry, new_run_id, new_timestamp, new_commit)
        new_results.append(new_entry)
    
    # Write to new file
    output_file = f"results/results_{i+3}.json"
    with open(output_file, "w") as f:
        json.dump(new_results, f, indent=2)

print("Generated 10 new benchmark result files with variations") 
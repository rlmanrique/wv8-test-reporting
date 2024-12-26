import json
import os
import argparse
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from dateutil import parser


def load_json_results(file_path):
    results = []
    for file in os.listdir(file_path):
        if file.endswith('.json'):
            with open(os.path.join(file_path, file)) as f:
                print(f"Processing file: {file}")
                results.extend(json.load(f))
    return results


def connect_to_database(url, token, org):
    return InfluxDBClient(
        url=url,
        token=token,
        org=org
    )


def prepare_data_points(results, bucket):
    data_points = []
    for result in results:
        point = {
            "measurement": "benchmark_results",
            "tags": {
                "run_id": result['run_id'],
                "branch": result['branch'],
                "commit": result['commit'],
                "ef": result['ef']
            },
            "fields": {
                "mean_latency": float(result['meanLatency']),
                "p99_latency": float(result['p99Latency']),
                "qps": float(result['qps']),
                "recall": float(result['recall'])
            },
            "time": parser.parse(result['timestamp'])
        }
        data_points.append(point)
    return data_points


def write_results(client, data_points, bucket, org):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    for point in data_points:
        try:
            write_api.write(
                bucket=bucket,
                org=org,
                record=point
            )
            print(f"Inserted {point['tags']['run_id']} into InfluxDB")
        except Exception as e:
            print(f"Error inserting point: {e}")
    
    write_api.close()


def main():
    parser = argparse.ArgumentParser(description='Store benchmark results in InfluxDB.')
    parser.add_argument('--url', required=True, help='InfluxDB URL (e.g., http://localhost:8086)')
    parser.add_argument('--token', required=True, help='InfluxDB authentication token')
    parser.add_argument('--org', required=True, help='InfluxDB organization')
    parser.add_argument('--bucket', required=True, help='InfluxDB bucket')
    parser.add_argument('--file_path', required=True, help='Path to the results files')

    args = parser.parse_args()

    results = load_json_results(args.file_path)
    
    client = connect_to_database(args.url, args.token, args.org)
    data_points = prepare_data_points(results, args.bucket)
    write_results(client, data_points, args.bucket, args.org)
    
    client.close()


if __name__ == "__main__":
    main() 
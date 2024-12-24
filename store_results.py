import json
import psycopg2
import os
import argparse


def load_json_results(file_path):
    results = []
    for file in os.listdir(file_path):
        if file.endswith('.json'):
            with open(os.path.join(file_path, file)) as f:
                print(f"Processing file: {file}")
                results.extend(json.load(f))
    return results


def connect_to_database(db_name, db_user, db_password, db_host, db_port):
    return psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )


def create_table(cur):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS benchmark_results (
        id SERIAL PRIMARY KEY,
        run_id VARCHAR(255),
        ef INTEGER,
        mean_latency FLOAT,
        p99_latency FLOAT,
        qps FLOAT,
        recall FLOAT,
        timestamp TIMESTAMP,
        branch VARCHAR(255),
        commit VARCHAR(255)
    )
    '''
    cur.execute(create_table_query)


def insert_results(cur, results):
    insert_query = '''
    INSERT INTO benchmark_results (run_id, ef, mean_latency, p99_latency, qps, recall, timestamp, branch, commit)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    for result in results:
        cur.execute(insert_query, (
            result['run_id'],
            result['ef'],
            result['meanLatency'],
            result['p99Latency'],
            result['qps'],
            result['recall'],
            result['timestamp'],
            result['branch'],
            result['commit']
        ))
        print(f"Inserted {result['run_id']} into the database")


def main():
    parser = argparse.ArgumentParser(description='Store benchmark results in a database.')
    parser.add_argument('--db_name', required=True, help='Name of the database')
    parser.add_argument('--db_user', required=True, help='Database user')
    parser.add_argument('--db_password', required=True, help='Database password')
    parser.add_argument('--db_host', required=True, help='Database host')
    parser.add_argument('--db_port', required=True, help='Database port')
    parser.add_argument('--file_path', required=True, help='Path to the results files')

    args = parser.parse_args()

    results = load_json_results(args.file_path)
    
    conn = connect_to_database(args.db_name, args.db_user, args.db_password, args.db_host, args.db_port)
    cur = conn.cursor()
    
    create_table(cur)
    insert_results(cur, results)
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
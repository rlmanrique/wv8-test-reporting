# wv8-test-reporting

Experimental repo to play with reporting of test results at WV8, store them in a database and query them.

## Requirements

- Python 3.10+
- PostgreSQL
- Grafana

### PostgreSQL

```bash
cd postgres-docker
docker compose up -d
```

## Usage

```bash
python store_results.py --db_name my_database --db_user postgres --db_password mysecretpassword --db_host localhost --db_port 5432 --file_path results/
```

## Test data

The data has been generated using `generate_benchmark_results.py` for have random variations of the results for a PoC.

To run it:

```bash
python generate_benchmark_results.py
```

# Microservices for Kafka and Spark Stream Processing

## Overview

This project implements a microservices-based architecture for stream processing using Kafka and Spark. It provides endpoints for real-time data processing, analysis, and transformation. The microservices are containerized using Docker and deployed using Kubernetes, with support for distributed data pipelines.

## Features
- Real-time stream processing using Apache Spark and Kafka.
- Comprehensive logging for monitoring and debugging.
- Containerized microservices for portability and scalability.
- Load testing using Locust to ensure reliability and stability.
- Quantitative assessment of system performance (latency, throughput).

## Requirements
1. Install **Docker** and **Kubernetes**:
   - Follow the official [Docker installation guide](https://docs.docker.com/get-docker/) and [Kubernetes installation guide](https://kubernetes.io/docs/tasks/tools/).
2. Install **Helm** to deploy Kafka and Spark:
   - Kafka: [Bitnami Kafka Chart](https://github.com/bitnami/charts/tree/main/bitnami/kafka)
   - Spark: [Bitnami Spark Chart](https://github.com/bitnami/charts/tree/main/bitnami/spark)
3. Install **Locust** for load testing:
   ```bash
   pip install locust
   ```

## Setting up the Kubernetes Cluster
1. Start Minikube:
   ```bash
   minikube start
   ```
2. Deploy Kafka and Spark using Helm:
   ```bash
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm install kafka bitnami/kafka
   helm install spark bitnami/spark
   ```
3. Verify deployment:
   ```bash
   kubectl get all
   ```
   
## Running the Microservices
1. Build the Docker image:
   ```bash
   docker build -t microservice .
   ```
2. Run the container:
   ```bash
   docker run -p 5000:5000 microservice
   ```
3. Test the `/process` endpoint:
   ```bash
   curl -X POST http://localhost:5000/process \
        -H "Content-Type: application/json" \
        -d '[{"id": 1, "gender": "M", "salary": 5000}, {"id": 2, "gender": "F", "salary": 6000}]'
   ```

## Load Testing
1. Run the load test using Locust:
   ```bash
   locust -f src/load_test.py --headless -u 100 -r 10 --run-time 1m --host http://localhost:5000
   ```
2. Sample results (excerpt):
   ```
   Requests: 727
   Avg Latency: 7121ms
   Min Latency: 4906ms
   Max Latency: 15603ms
   Median Latency: 6400ms
   Percentiles (95th): 11000ms
   ```

## Quantitative Assessment
The system was tested with 100 concurrent users and a ramp-up rate of 10 users per second. Below are the key metrics from the load tests:

| Metric              | Value                |
|---------------------|----------------------|
| Total Requests      | 727                 |
| Average Latency     | 7121ms              |
| Minimum Latency     | 4906ms              |
| Maximum Latency     | 15603ms             |
| Median Latency      | 6400ms              |
| 95th Percentile     | 11000ms             |
| Error Rate          | 0% (0 failures)     |

### Observations
- The average latency increased with the number of concurrent requests but remained under acceptable limits for most cases.
- No failures were recorded, indicating good reliability.
- Optimization opportunities exist to reduce peak latencies (e.g., refactoring Spark jobs or optimizing Kafka configurations).

## Limitations
1. **Latency**: Average latency increases with high concurrency, especially for complex Spark jobs.
2. **Scalability**: Currently limited to a single-node Kafka and Spark setup.
3. **Monitoring**: Requires integration with tools like Prometheus or Grafana for better performance visualization.

## Potential Areas for Improvement
1. **Scaling**: Move to a multi-node cluster to improve scalability and reduce bottlenecks.
2. **Caching**: Use distributed caching (e.g., Redis) to speed up frequently accessed computations.
3. **Advanced Metrics**: Collect more detailed performance metrics using monitoring tools.
4. **CI/CD**: Extend the GitHub Actions pipeline to include integration tests and deployment to Kubernetes.

## AI Pair Programming Tools Used
1. **GitHub Copilot**:
   - Assisted in generating initial code for Kafka-Spark integration.
   - Suggested efficient ways to group and aggregate data streams.
2. **TabNine**:
   - Provided code completions for Flask APIs and Spark transformations.
   - Enhanced the quality of SQL-like Spark operations.

## Directory Structure
```
project-root/
│
├── .devcontainer/             # Docker configuration for GitHub Codespaces
│   ├── Dockerfile
│   ├── devcontainer.json
│
├── src/                       # Source code for microservices
│   ├── app.py                 # Flask API for data processing
│   ├── load_test.py           # Locust script for load testing
│   ├── count_gender.py        # Spark job: Count records by gender
│   ├── count_month.py         # Spark job: Count records by birth month
│   ├── final_analysis.py      # Spark job: Comprehensive analysis
│   ├── read_emp_data.py       # Spark job: Read employee data
│   ├── read_json_from_topic.py # Spark job: Read data from Kafka
│
├── data/                      # Sample data for testing
│   ├── emp_data.json
│   ├── json_topic.json
│
├── images/                    # Helm chart specifications for Kafka and Spark
│   ├── kafka.yml
│   ├── spark.yml
│
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
```

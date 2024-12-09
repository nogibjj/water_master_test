## **Commands for Kafka and Spark**

### **1. Running Kafka Producer**
Produce messages to a Kafka topic:
```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic <TOPIC_NAME>
```
Example:
```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test
```

### **2. Running Kafka Consumer**
Consume messages from a Kafka topic:
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic <TOPIC_NAME> --from-beginning
```
Example:
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```

### **3. Running Kafka Key-Value Pair Producer**
Produce key-value pairs to a Kafka topic:
```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic <TOPIC_NAME> --property "parse.key=true" --property "key.separator=:"
```
Example:
```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test_topic --property "parse.key=true" --property "key.separator=:"
```

### **4. Submitting Spark Jobs**
Run a Spark job using `spark-submit`:

- General command:
  ```bash
  spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 <SCRIPT_PATH>
  ```

- Example: Running `read_test_stream.py`:
  ```bash
  spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 src/read_test_stream.py
  ```

### **5. Kafka Utilities**

#### **5.1 List Kafka Topics**
List all available Kafka topics:
```bash
kafka-topics.sh --list --bootstrap-server localhost:9092
```

#### **5.2 Describe Kafka Topic**
View details about a specific Kafka topic:
```bash
kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic <TOPIC_NAME>
```

### **6. Kubernetes Commands**

#### **6.1 Copy Files to Kubernetes Pods**
Copy a file from your local machine to a Kubernetes pod:
```bash
kubectl cp <SOURCE_PATH> <POD_NAME>:/<DESTINATION_PATH>
```
Example:
```bash
kubectl cp data/emp_data.json my-release-spark-worker-0:/tmp
```

#### **6.2 View Running Pods**
Check the status of all running pods in the cluster:
```bash
kubectl get pods
```

#### **6.3 Access Pod Logs**
View logs of a specific pod:
```bash
kubectl logs <POD_NAME>
```

### **7. Microservice API Testing**
#### **7.1 Test Microservice Endpoint**
Send a POST request to the `/process` endpoint:
```bash
curl -X POST http://localhost:5000/process \
     -H "Content-Type: application/json" \
     -d '[{"id": 1, "gender": "M", "salary": 5000}, {"id": 2, "gender": "F", "salary": 6000}]'
```

### **8. Load Testing**
Run load tests with Locust:
```bash
locust -f src/load_test.py --headless -u <USERS> -r <SPAWN_RATE> --run-time <DURATION> --host http://localhost:5000
```
Example:
```bash
locust -f src/load_test.py --headless -u 100 -r 10 --run-time 1m --host http://localhost:5000
```

### **9. Additional Notes**
- Ensure that Kafka and Spark services are running before executing any commands.
- Replace `<TOPIC_NAME>` or `<POD_NAME>` with the actual topic or pod names used in your setup.
- Use `kubectl get all` to verify the status of Kubernetes resources.

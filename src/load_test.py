from locust import HttpUser, task, between

class LoadTest(HttpUser):
    wait_time = between(0.001, 0.002)  # Minimal wait time for high throughput

    @task
    def post_data(self):
        data = [
            {"id": 1, "gender": "M", "salary": 5000},
            {"id": 2, "gender": "F", "salary": 6000},
            {"id": 3, "gender": "M", "salary": 5500},
        ]
        self.client.post("/process", json=data)

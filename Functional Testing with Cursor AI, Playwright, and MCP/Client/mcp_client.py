# mcp_client.py
import requests
import json

class MCPClient:
    def __init__(self, server_url):
        self.server_url = server_url

    def list_tests(self):
        return requests.get(f"{self.server_url}/tests").json()

    def generate_test(self, requirement):
        payload = {"requirement": requirement}
        return requests.post(f"{self.server_url}/tests", json=payload).json()

    def run_test(self, test_id, browser="chromium"):
        payload = {"browser": browser}
        return requests.post(f"{self.server_url}/tests/{test_id}/run", json=payload).json()

    def get_run_status(self, run_id):
        return requests.get(f"{self.server_url}/runs/{run_id}").json()

    def get_artifacts(self, run_id):
        return requests.get(f"{self.server_url}/runs/{run_id}/artifacts").json()

    def download_artifact(self, run_id, artifact_id, save_path):
        resp = requests.get(f"{self.server_url}/runs/{run_id}/artifact/{artifact_id}")
        with open(save_path, "wb") as f:
            f.write(resp.content)
        return save_path


if __name__ == "__main__":
    client = MCPClient("http://localhost:8000")
    print(client.list_tests())

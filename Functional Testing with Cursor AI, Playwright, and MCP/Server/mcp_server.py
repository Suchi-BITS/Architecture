# mcp_server.py
from fastapi import FastAPI, HTTPException
from typing import List
import uuid
import os
from playwright_runner import run_playwright_test, generate_test_code

app = FastAPI()

# In-memory test store for simplicity
tests_db = {}
runs_db = {}

@app.get("/tests")
async def list_tests():
    return [{"test_id": tid, "description": t["description"]} for tid, t in tests_db.items()]

@app.post("/tests")
async def generate_test(requirement: dict):
    test_id = str(uuid.uuid4())
    test_code = generate_test_code(requirement.get("requirement"))
    tests_db[test_id] = {"description": requirement.get("requirement"), "code": test_code}
    return {"test_id": test_id, "test_code": test_code}

@app.get("/tests/{test_id}")
async def get_test(test_id: str):
    if test_id not in tests_db:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"test_id": test_id, "test_code": tests_db[test_id]["code"], "description": tests_db[test_id]["description"]}

@app.delete("/tests/{test_id}")
async def delete_test(test_id: str):
    if test_id not in tests_db:
        raise HTTPException(status_code=404, detail="Test not found")
    del tests_db[test_id]
    return {"status": "deleted"}

@app.post("/tests/{test_id}/run")
async def run_test(test_id: str, payload: dict):
    if test_id not in tests_db:
        raise HTTPException(status_code=404, detail="Test not found")
    browser = payload.get("browser", "chromium")
    run_id = str(uuid.uuid4())
    runs_db[run_id] = {"status": "running"}
    result = run_playwright_test(tests_db[test_id]["code"], browser)
    runs_db[run_id] = result
    return {"run_id": run_id, "status": result["status"]}

@app.get("/runs/{run_id}")
async def get_run(run_id: str):
    if run_id not in runs_db:
        raise HTTPException(status_code=404, detail="Run not found")
    return runs_db[run_id]

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# playwright_runner.py
import subprocess
import uuid
import os

PLAYWRIGHT_TESTS_DIR = "./tests"

def generate_test_code(requirement: str) -> str:
    # In real case, call Cursor AI or an LLM to generate Playwright code
    return f"""
import {{ test, expect }} from '@playwright/test';

test('{requirement}', async {{ page }} => {{
    await page.goto('https://example.com');
    await expect(page).toHaveTitle(/Example/);
}});
"""

def run_playwright_test(test_code: str, browser: str = "chromium") -> dict:
    if not os.path.exists(PLAYWRIGHT_TESTS_DIR):
        os.makedirs(PLAYWRIGHT_TESTS_DIR)
    test_id = str(uuid.uuid4())
    test_file_path = os.path.join(PLAYWRIGHT_TESTS_DIR, f"{test_id}.spec.ts")

    with open(test_file_path, "w") as f:
        f.write(test_code)

    result = {"status": "failed", "logs": ""}

    try:
        proc = subprocess.run(
            ["npx", "playwright", "test", test_file_path, f"--browser={browser}", "--reporter=json"],
            capture_output=True,
            text=True,
            check=True
        )
        result["status"] = "passed"
        result["logs"] = proc.stdout
    except subprocess.CalledProcessError as e:
        result["logs"] = e.stdout + "\n" + e.stderr

    return result

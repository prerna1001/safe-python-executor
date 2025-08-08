import subprocess
import os
import json
import textwrap
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def run_in_jail(script: str):
    # Ensure /scripts directory exists at runtime
    os.makedirs("/scripts", exist_ok=True)

    # Dedent user script (remove any leading indentation)
    user_code = textwrap.dedent(script).strip()

    # Write a wrapped version of the user's script to /scripts/sandboxed.py
    with open("/scripts/sandboxed.py", "w") as f:
        f.write(f"{user_code}\n\n")
        f.write(textwrap.dedent("""
        if __name__ == "__main__":
            import json
            result = main()
            print("##RESULT##" + json.dumps(result), flush=True)
        """))

    # Execute it inside nsjail
    try:
        result = subprocess.run(
            ["nsjail", "--config", "/app/nsjail.cfg"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        stdout = result.stdout.decode()
        stderr = result.stderr.decode()curl -X POST https://safe-python-executor-r3bafn6d3a-uc.a.run.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    import numpy as np\n    arr = np.array([1, 2, 3])\n    return {\"sum\": int(np.sum(arr)), \"mean\": float(np.mean(arr))}"}'


        logger.debug("Subprocess stdout:\n%s", stdout)
        logger.debug("Subprocess stderr:\n%s", stderr)

        result_value = None
        for line in stdout.splitlines():
            if line.startswith("##RESULT##"):
                try:
                    result_value = json.loads(line[len("##RESULT##"):])
                except Exception:
                    result_value = line[len("##RESULT##"):]

        stderr = result.stderr.decode()
        
        return {
            "result": result_value,
            "stdout": stdout
        }

    except subprocess.TimeoutExpired:
        logger.error("Subprocess timed out")
        return {
            "result": None,
            "stdout": "",
        }

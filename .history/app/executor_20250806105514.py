import subprocess
import uuid
import os

NSJAIL_CONFIG = "/app/nsjail.cfg"

def run_in_jail(code: str):
    # Save code to a temp file
    temp_path = f"/tmp/{uuid.uuid4().hex}.py"
    with open(temp_path, "w") as f:
        f.write(code)

    cmd = [
        "nsjail",
        "--config", NSJAIL_CONFIG,
        "--",
        "python3", temp_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, timeout=5, text=True)
        output = result.stdout
        error = result.stderr
    except subprocess.TimeoutExpired:
        output = ""
        error = "Execution timed out"
        result = subprocess.CompletedProcess(cmd, returncode=124)
    finally:
        os.remove(temp_path)

    return {
        "stdout": output,
        "stderr": error,
        "exit_code": result.returncode
    }

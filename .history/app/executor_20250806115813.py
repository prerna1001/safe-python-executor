import subprocess

def run_in_jail(code: str):
    # Step 1: Write code to /scripts/sandboxed.py
    with open("/scripts/sandboxed.py", "w") as f:
        f.write(code)

    # Step 2: Run the code inside nsjail using the config
    try:
        result = subprocess.run(
            [
                "nsjail",
                "--config",
                "/app/nsjail.cfg"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        return {
            "stdout": result.stdout.decode(),
            "stderr": result.stderr.decode(),
            "exit_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Execution timed out",
            "exit_code": -1
        }

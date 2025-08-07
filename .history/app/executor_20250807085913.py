import subprocess
import os
import json
import textwrap

def run_in_jail(script: str):
    # Ensure /scripts directory exists at runtime
    os.makedirs("/scripts", exist_ok=True)

    #dedent user scrpit (remove any leading indentation)
    user_code = textwrap.dedent(script).strip()

    #Write a wrapped version of the user's script to /scripts/sandboxed.py
    with open("scripts/sandbox.py", "w") as f:
        f.write()

    # Execute it inside nsjail
    try:
        result = subprocess.run(
            ["nsjail", "--config", "/app/nsjail.cfg"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        stdout = result.stdout.decode()
        result_value = None
        for line in stdout.splitlines():
            print("DEBUG LINE:", line)
            if line.startswith("##RESULT##"):
                try:
                    result_value = json.loads(line[len("##RESULT##"):])
                except Exception:
                    result_value = line[len("##RESULT##"):]

        stderr = result.stderr.decode()
        print("DEBUG STDOUT >>>")
        print(stdout)
        print("<<< END DEBUG STDOUT")
        print("DEBUG STDERR >>>")
        print(stderr)
        print("<<< END DEBUG STDERR")
        return {
            "result": result_value,
            "stdout": stdout
        }
        

    except subprocess.TimeoutExpired:
        return {
            "result": None,
            "stdout": "",
        }

import subprocess
import os
import json
import textwrap

def run_in_jail(script: str):
    # ✅ Ensure /scripts directory exists at runtime
    os.makedirs("/scripts", exist_ok=True)

    # ✅ Write a wrapped version of the user's code to /scripts/sandboxed.py
    wrapped_code = textwrap.dedent(f"""
    {code}

    if __name__ == "__main__":
        import json
        result = main()
        print("##RESULT##" + json.dumps(result))
    """)

    with open("/scripts/sandboxed.py", "w") as f:
        f.write(wrapped_code)

    # ✅ Execute it inside nsjail
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
            if line.startswith("##RESULT##"):
                try:
                    result_value = json.loads(line[len("##RESULT##"):])
                except Exception:
                    result_value = line[len("##RESULT##"):]

        return {
            "result": result_value,
            "stdout": stdout,
            "stderr": result.stderr.decode()
}
                
    except subprocess.TimeoutExpired:
        return {
            "result": None,
            "stdout": "",
            "stderr": "Execution timed out"
        }

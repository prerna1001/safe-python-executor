import subprocess
import os
import json
import textwrap


def run_in_jail(script: str):
    # Ensure /tmp directory exists at runtime
    os.makedirs("/tmp", exist_ok=True)

    # Dedent user script (remove any leading indentation)
    user_code = textwrap.dedent(script).strip()

    # Write a wrapped version of the user's script to /tmp/sandboxed.py
    with open("/tmp/sandboxed.py", "w") as f:
        f.write(f"{user_code}\n\n")
        f.write(textwrap.dedent("""
        if __name__ == "__main__":
            import json
            result = main()
            print("##RESULT##" + json.dumps(result))
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
        stderr = result.stderr.decode()

        logger.debug("Subprocess stdout:\n%s", stdout)
        logger.debug("Subprocess stderr:\n%s", stderr)

        result_value = None
        for line in stdout.splitlines():
            if line.startswith("##RESULT##"):
                try:
                    result_value = json.loads(line[len("##RESULT##"):])
                except Exception:
                    result_value = line[len("##RESULT##"):]
        
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

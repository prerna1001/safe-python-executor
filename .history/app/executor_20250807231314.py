import subprocess
import os
import json
import textwrap

def run_in_jail(script: str):
    # Ensure /scripts directory exists at runtime
    os.makedirs("/scripts", exist_ok=True)

    # Dedent user script (remove any leading indentation)
    user_code = textwrap.dedent(script).strip()

    # Write a wrapped version of the user's script to /scripts/sandboxed.py
    print("DEBUG /scripts/sandboxed.py content:")
    with open("/scripts/sandboxed.py", "w") as f:
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

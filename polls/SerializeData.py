import os
import tempfile
import subprocess


def isSerializable(data):
    # 1) Serialize your data into lines
    serialized = [str(item) for item in data]

    # 2) Write to a temp file
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, prefix="evt_", suffix=".sh"
    ) as tmp:
        for item in serialized:
            tmp.write(item + "\n")
        tmp_path = tmp.name

    os.chmod(tmp_path, 0o700)

    # 3) Only run the script if it exists
    wrapper = "/tmp/script.sh"
    wrapper = "/usr/local/scripts/script.sh"
    if os.path.exists(wrapper):
        subprocess.run(["bash", wrapper, tmp_path], check=True)
    # else: do nothing

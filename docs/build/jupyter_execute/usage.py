import subprocess
print(subprocess.run(["assumptions", "-h"], capture_output=True).stdout.decode())
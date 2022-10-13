import os, sys
import shutil

try:
    action = sys.argv[1]
except:
    print("[!] ERROR: Specify Clean, Build or Upload")
    exit(1)

if action.lower() == "clean":
    shutil.rmtree("bin", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    exit(0)
elif action.lower() == "build":
    os.system("python .\setup.py sdist bdist_wheel")
elif action.lower() == "upload":
    os.system("twine upload dist/*")
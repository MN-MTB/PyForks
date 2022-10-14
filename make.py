import os, sys
import shutil

try:
    action = sys.argv[1]
except:
    print("[!] ERROR: Specify Clean, Build, Upload, Docs")
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
elif action.lower() == "docs":
    os.system("pdoc --html --template-dir ./doc/templates/light_theme/ -o ./doc/ --force PyForks")
    base_dir = "./doc/PyForks"
    to_dir = "./doc"
    for file in os.listdir(base_dir):
        try:
            shutil.move(f"{base_dir}/{file}", to_dir)
        except shutil.Error as e:
            os.remove(f"{to_dir}/{file}")
            shutil.move(f"{base_dir}/{file}", to_dir)
    shutil.rmtree("./doc/PyForks")
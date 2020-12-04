## created by sanyabeast <a.gvrnsk@gmail.com>\
## 05 dec 2020
## ! uses PYTHON 3.8.3

import subprocess
import sys
import shutil 
from pathlib import Path
import shlex
import argparse

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def rmtree_s(p):
    try: shutil.rmtree(p)
    except Exception as e: print(str(e))

def log(text):
    print(f"[TOOL] [i] {str(text)}")

def run_shell(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, shell=True)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            log(f"[{command}] {output}")
            pass
    rc = process.poll()

def get_args(help="", params=[]):
    parser = argparse.ArgumentParser(description=help)
    for o in params:
        parser.add_argument(f"--{o[0]}", type=o[1], default=o[2])
    args = parser.parse_args()
    return args    

## tasks
def commit(commit_text="some misterious tweaks"):
    run_shell(command="git add -A")
    run_shell(command=f"git commit -m \"{args.git_commit_text}\""),

args = get_args("packaing tool", [
    ["git-commit", str2bool, False],
    ["git-commit-text", str, "some misteriuos tweaks"],
])


if args.git_commit:
    commit(args.git_commit_text)
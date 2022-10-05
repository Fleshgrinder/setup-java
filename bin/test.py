#!/usr/bin/env python3
from os import environ
from subprocess import call, STDOUT

env = ""
for k, v in environ.items():
    if "java" in k.lower():
        env += f"\033[32m{k}\033[0m=\033[33m{v}\033[0m\n"
print(env)

failed = False
ec = call(["java", "-version"], stderr=STDOUT, timeout=60)
if ec != 0:
    print(f"::error::`java -version` failed with exit code: {ec}")

if "JAVA_HOME" not in environ:
    failed = True
    print("::error::Missing required environment variable 'JAVA_HOME'.")
if "JAVA_VERSION" not in environ:
    failed = True
    print("::error::Missing required environment variable 'JAVA_VERSION'.")
elif environ["JAVA_VERSION"] != environ["JAVA_VERSION_LATEST"]:
    failed = True
    print(f"::error::Expected 'JAVA_VERSION' to match 'JAVA_VERSION_LATEST', but: {environ['JAVA_VERSION']} != {environ['JAVA_VERSION_LATEST']}")
if failed is True:
    exit(1)

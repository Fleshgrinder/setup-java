#!/usr/bin/env python3
import json
from os import environ
from pathlib import Path
from time import sleep
from urllib.error import HTTPError
from urllib.request import urlopen, Request

if "GITHUB_ENV" not in environ:
    print("::error::Missing required 'GITHUB_ENV' environment variable, make sure it exists.")
    exit(1)

request = Request(
    "https://api.adoptium.net/v3/info/available_releases",
    headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (+https://github.com/fleshgrinder/setup-java)",
    },
)

retries = 5
for i in range(1, retries):
    try:
        with urlopen(request) as response:
            latest = int(json.loads(response.read())["available_lts_releases"][-1])
            with Path(environ["GITHUB_ENV"]).open("a") as env:
                env.write(f"JAVA_VERSION_LATEST={latest}")
            print(f"Latest Java version: \033[32m{latest}\033[0m")
            exit(0)
    except HTTPError as e:
        debug_info = ""
        for k, v in e.headers.items():
            debug_info += f"{k}: {v}\n"
        debug_info += "\n"
        debug_info += e.read().decode().rstrip()
        debug_info += "\n"
        print(debug_info)
        s = 1 * i
        print(f"::warning::Request failed, retrying after {s} second(s)...")
        sleep(s)

print(f"::error::Request failed, giving up...")
exit(1)

from glob import glob
from functools import cmp_to_key
import os
import re
import zipfile
import subprocess

import requests
import semver

response = requests.get('https://api.github.com/repos/szymonbultrowicz/esp32-soil-moisture-sensor/releases')
if response.status_code > 399:
    raise ValueError(f'Got response status {response.status_code} when fetching releases')
tag_name = response.json()[0]['tag_name']
latest_version = re.search('\d+\.\d+\.\d+$', tag_name).group(0)
new_version = semver.bump_patch(latest_version)

try:
    cmd = ['gh', 'release', 'create', new_version, 'app/*', '-n', '""']
    print(' '.join(cmd))
    subprocess.run(cmd, check=True, capture_output=True)
except subprocess.CalledProcessError as exc:
    print("Status : FAIL", exc.returncode, exc.output)
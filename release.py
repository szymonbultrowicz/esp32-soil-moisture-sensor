from glob import glob
from functools import cmp_to_key
import os
import re
import zipfile
import subprocess

import requests
import semver

release_dir = 'dist'
sources_dir = 'app'

response = requests.get('https://api.github.com/repos/szymonbultrowicz/esp32-soil-moisture-sensor/releases')
if response.status_code > 399:
    raise ValueError(f'Got response status {response.status_code} when fetching releases')
tag_name = response.json()[0]['tag_name']
latest_version = re.search('\d+\.\d+\.\d+$', tag_name).group(0)
new_version = semver.bump_patch(latest_version)

def zip_sources(out_file):
    with zipfile.ZipFile(out_file, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write('main.py')
        for root, dirs, files in os.walk(sources_dir):
            for file in files:
                zip_file.write(os.path.join(root, file))

new_release_file = f'{release_dir}/v{new_version}.zip'
zip_sources(new_release_file)
subprocess.run(['gh', 'release', 'create', new_version, new_release_file, '-n', ''], check=True)

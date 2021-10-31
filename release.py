from glob import glob
from functools import cmp_to_key
import os
import re
import zipfile
import semver

releases_dir = 'dist'
sources_dir = 'src'
last_release = '0.0.0'

existing_release_files = glob(f'./{releases_dir}/v*.zip')
if len(existing_release_files) > 0:
    all_versions = [re.search("(\d+\.\d+\.\d+)\.zip$", v).group(1) for v in existing_release_files]
    last_release = sorted(all_versions, key=cmp_to_key(semver.compare), reverse=True)[0]
    print(last_release)
new_version = semver.bump_patch(last_release)

def zip_sources(version):
    with zipfile.ZipFile(f'{releases_dir}\\v{version}.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(sources_dir):
            for file in files:
                zip_file.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), sources_dir))

zip_sources(new_version)

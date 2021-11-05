import secrets
from app.ota_updater import OTAUpdater

updater = OTAUpdater(secrets.github_url, main_dir='app', headers={'Authorization': f'token {secrets.github_token}'})
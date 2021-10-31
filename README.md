# Plant soil moisture sensor

## How to prepare to upload

1. Create `secrets.py` file with
   ```
   wifi_ssid = ...
   wifi_password = ...
   ```
1. Create and upload `ota` directory containing files from [micropython-ota-updater](https://github.com/rdehuyss/micropython-ota-updater/tree/master/app)
1. Create and upload `umqtt` directory containing files from [umqtt.robust](https://github.com/micropython/micropython-lib/tree/master/micropython/umqtt.robust/umqtt) and [umqtt.simple](https://github.com/micropython/micropython-lib/tree/master/micropython/umqtt.simple/umqtt)